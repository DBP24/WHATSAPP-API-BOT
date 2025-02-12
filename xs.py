from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os
import json

# Cargar variables de entorno
WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')
API_TOKEN = os.getenv('API_TOKEN')
BUSINESS_PHONE = os.getenv('BUSINESS_PHONE')
API_VERSION = os.getenv('API_VERSION')

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        try:
            # Obtener los datos JSON del cuerpo de la solicitud
            body = request.body.decode('utf-8')  # Decodificar el cuerpo de la solicitud
            data = json.loads(body)  # Convertir el JSON en un diccionario de Python

            # Log incoming messages
            print("Incoming webhook message:", json.dumps(data, indent=2))

            # Check if the webhook request contains a message
            message = data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('messages', [{}])[0]
            print(message.get(type))
            # Check if the incoming message contains text
            # if message.get('type') == 'text':
            if True:
                print("entroiooooooo al if")
                # Extract the business number to send the reply from it
                business_phone_number_id = data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('metadata', {}).get('phone_number_id')

                # Send a reply message
                reply_url = f'https://graph.facebook.com/{API_VERSION}/{BUSINESS_PHONE}/messages'
                headers = {
                    'Authorization': f'Bearer {API_TOKEN}',
                }
                reply_data = {
                    'messaging_product': 'whatsapp',
                    'to': message.get('from'),
                    'text': {'body': 'Echo: ' + message.get('text', {}).get('body')},
                    'context': {
                        'message_id': message.get('id'),  # Shows the message as a reply to the original user message
                    },
                }
                requests.post(reply_url, headers=headers, json=reply_data)

                # Mark incoming message as read
                read_data = {
                    'messaging_product': 'whatsapp',
                    'status': 'read',
                    'message_id': message.get('id'),
                }
                requests.post(reply_url, headers=headers, json=read_data)

            return HttpResponse(status=200)

        except json.JSONDecodeError:
            return HttpResponse('Invalid JSON', status=400)
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return HttpResponse(status=500)

    elif request.method == 'GET':
        # Verificación del webhook (GET request)
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
            print("Webhook verified successfully!")
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse(status=403)

    return HttpResponse(status=405)  # Método no permitido


