import os
import json
import requests
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import asyncio
import aiohttp

from . import whatsapp
from .openai import FunctionOpenAI
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
            body.clear()
            print(body)
            # traer mensaje
            function_openai = FunctionOpenAI()
            responseOpenai = function_openai.baseOpenai(message['text']['body'])
             
            # ACTUALIZO EL BODY
            message['text']['body'] = responseOpenai
            print(f"ID DE CADA USUARIO: {message['id']}")
        except (KeyError, IndexError):
            return HttpResponse(status=200)

        if message.get('type') == 'text':
            
            # Enviar mensaje de respuesta
            payload_go_message ={
                'messaging_product': 'whatsapp',
                'to': message['from'],
                # 'text': {'body': f"{responseOpenai}"},
                'text': {'body': f"{message['text']['body']}"},
                'context': {
                    'message_id': message['id']
                    }
            }

            # marcar mensaje leido
            payload_mark_message = {
                'messaging_product': 'whatsapp',
                'status': 'read',
                'message_id': message['id']
            }

            asyncio.run(whatsapp.send_general(payload_go_message,"envio de mensaje"))
            asyncio.run(whatsapp.send_general(payload_mark_message,"marcar leido"))

         
        return HttpResponse(status=200)

   

