import asyncio
import aiohttp
import os

# Obtener credenciales desde .env
WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')
API_TOKEN = os.getenv('API_TOKEN')
BUSINESS_PHONE = os.getenv('BUSINESS_PHONE')
API_VERSION = os.getenv('API_VERSION')

async def send_general(payload, message_error="error"):
   
   try:

       url = f"https://graph.facebook.com/{API_VERSION}/{BUSINESS_PHONE}/messages"
       headers = {
           'Authorization': f'Bearer {API_TOKEN}',
           'Content-Type': 'application/json'
       }
       
       async with aiohttp.ClientSession() as session:
           async with session.post(url, json=payload, headers=headers) as response:
               response.raise_for_status()
               return await response.json()
       
               
   except aiohttp.ClientError as e:
       print(f"Error de aiohttp: {e}")
       raise
   except Exception as e:
       print(f"{message_error} {e}")
       raise
