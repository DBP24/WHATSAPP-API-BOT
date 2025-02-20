import os
from dotenv import load_dotenv
from django.conf import settings
import openai
import json

load_dotenv()
openai.api_key = os.getenv("OPEN_IA_KEY")

def get_Yape_Payments():  # Agregamos el parámetro pero lo hacemos opcional
    try:

        # No necesitamos usar data_clients pero lo mantenemos para compatibilidad
        
        url_imagen = "https://www.datocms-assets.com/56886/1723236973-novedades-home-01.png"
        telefono ="941840053"
        titular ="Diego Bonatti Pajuelo"
        return  f"datos de la forma de pago: titular {titular}, numero : {telefono}, codigo qr {url_imagen}"
    except Exception as e:
        print("errororrrrrrrrrrrrrrrr") 
        # print(f"Error al obtener la imagen de pago: {e}")
        return "error"

# Mensajes iniciales
messages = [
    {
        "role": "system",
        "content": "Te llamas LOIA. Cuando los usuarios pregunten por pagos, indica que aceptas Yape y muestra la información de pago correspondiente. Sé concisa y clara."
    },
    {
        "role": "user",
        "content": "necesito que me vendas un polo talla M"
    }
]

# Definición de funciones
functions = [
    {
        "type": "function",
        "function": {
            "name": "get_Yape_Payments",
            "description": "Obtiene la imagen con la información de pago Yape"
        }
    }
]

try:
    # Primera llamada a la API
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=functions,
        max_tokens=100,
        temperature=0.7
    )
    
    assistant_message = response.choices[0].message
    
    if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            if tool_call.type == "function":
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                if function_name == "get_Yape_Payments":
                    # print("Obteniendo información de pago Yape...")
                    yape_info = get_Yape_Payments()
                    
                    messages.append(assistant_message)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": yape_info if yape_info else "Error al obtener la imagen"
                    })

    # Segunda llamada a la API
    second_response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=100,
        temperature=0.7
    )
    
    final_reply = second_response.choices[0].message.content
    print( final_reply)

except Exception as e:
    print(f"Error en la función OpenAI: {str(e)}")
