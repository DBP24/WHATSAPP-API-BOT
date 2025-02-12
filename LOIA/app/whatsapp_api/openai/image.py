
'''
trabaja con la version : pip install openai==0.28 
'''


import os
from dotenv import load_dotenv
import openai  # Asegúrate de usar el cliente correcto
import base64

# Cargar las variables de entorno
load_dotenv()

# Establecer la clave de la API
openai.api_key = os.getenv("OPEN_IA_KEY")

# Función para codificar la imagen en base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Preparar los mensajes (contenido)
messages = [
    {
        "role": "system",
        "content": "Eres un asistente que analiza las imágenes a gran detalle."
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Hola, ¿puedes analizar esta imagen?"
            },    
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://jumboalacarta.com.ar/wp-content/uploads/2019/06/shutterstock_521741356.jpg"
                    }  
            }
        ]
      
    }
]

# Hacer la solicitud a la API de OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",  # Asegúrate de usar un modelo disponible (como gpt-4 o cualquier otro)
    messages=messages,
    #max_tokens=100  # Puedes ajustar esto según lo que necesites
)

# Imprimir la respuesta
print("Respuesta del análisis de la imagen:")
print(response['choices'][0]['message']['content'].strip())
