import os
import json
import requests
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import asyncio
import aiohttp


# Obtener credenciales desde .env
WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')
API_TOKEN = os.getenv('API_TOKEN')
BUSINESS_PHONE = os.getenv('BUSINESS_PHONE')
API_VERSION = os.getenv('API_VERSION')

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        # Registro de mensajes entrantes
        body = json.loads(request.body)
        # print(f"Mensaje webhook entrante: {json.dumps(body, indent=2)}")

        try:
            message = body['entry'][0]['changes'][0]['value']['messages'][0]
        except (KeyError, IndexError):
            return HttpResponse(status=200)

        if message.get('type') == 'text':
            
            # Enviar mensaje de respuesta
            asyncio.run(send_message(
                to_number=message['from'],
                message_body=f"Echo: {message['text']['body']}",
                message_id=message['id']
            ))

            # Marcar mensaje como leído
            asyncio.run(mark_message_as_read(
                message_id=message['id']
            ))

        return HttpResponse(status=200)

   



# envio de mensajes
async def send_message(to_number, message_body, message_id):
   
   try:

       url = f"https://graph.facebook.com/{API_VERSION}/{BUSINESS_PHONE}/messages"
       headers = {
           'Authorization': f'Bearer {API_TOKEN}',
           'Content-Type': 'application/json'
       }
       payload = {
           'messaging_product': 'whatsapp',
           'to': to_number,
           'text': {'body': message_body},
           'context': {
               'message_id': message_id
           }
       }
       
       async with aiohttp.ClientSession() as session:
           async with session.post(url, json=payload, headers=headers) as response:
               response.raise_for_status()
               return await response.json()
       
               
   except aiohttp.ClientError as e:
       print(f"Error de aiohttp: {e}")
       raise
   except Exception as e:
       print(f"Error sending message: {e}")
       raise


# marcar como leído

async def mark_message_as_read(message_id):
    try:
        if not message_id:
            raise ValueError("El message_id no puede estar vacío.")

        url = f"https://graph.facebook.com/{API_VERSION}/{BUSINESS_PHONE}/messages"
        headers = {
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        }
        payload = {
            'messaging_product': 'whatsapp',
            'status': 'read',
            'message_id': message_id
        }
   
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response.raise_for_status()  # Lanza una excepción si el estado no es 2xx
                response_data = await response.json()
                print(f"Mensaje marcado como leído: {response_data}")
                return response_data
            
    except aiohttp.ClientError as e:
        print(f"Error de aiohttp al marcar el mensaje como leído: {e}")
        raise
    except Exception as e:
        print(f"Error inesperado al marcar el mensaje como leído: {e}")
        raise