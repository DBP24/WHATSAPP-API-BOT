import os
from dotenv import load_dotenv
# from openai import OpenAI
import openai
import json
import requests

load_dotenv()

# client = OpenAI(api_key=os.getenv("OPEN_IA_KEY"))  # cuando esta en la misma base del proyecto
openai.api_key = os.getenv("OPEN_IA_KEY")



messages = [
    {
    "role" : "system",
    "content" : "eres un asistente que entrega datos del  clima"
    },
    {
    "role" : "user",
    "content" : "cual es el clima en vegueta - huacho Perú"
    },
]



def get_clima(latitud:float, longitud:float) -> str:
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&current_weather=true"
    response = requests.get(url)
    clima = response.json()
    return json.dumps(clima)

functions = [
    {
        "type": "function",
        "function":{
            "name":"get_clima",
            "description": "usa esta funcion para obtener información referente al clima",
            "parameters" : {
                "type" : "object",
                "properties":{
                    "latitud":{
                        "type" : "number",
                        "description" : "Latitud de la ubicación"
                    },
                    "longitud":{
                        "type" : "number",
                        "description" : "longitud de la ubicación"
                    }
                },

                "required" : ["latitud" , "longitud"]
            },
            "output" : {
                "type" : "string",
                "description":"clima de la ubicacion pedida por el usuario"
            }
        }
    }
]

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=messages,
    # paso 5 : declarar tools
    tools=functions,


    max_tokens=100,
    temperature=0.7
)

assistant_message = response.choices[0].message

print("respuesta del asistente")
print(assistant_message)

if assistant_message.tool_calls:
    for tool_call in assistant_message.tool_calls:
        if tool_call.type == "function":
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            if function_name == "get_clima":
                print(f"El asistente está llamando a la función get_clima")
                weather_info = get_clima(
                    latitud=function_args.get("latitud"),
                    longitud=function_args.get("longitud")
                )

                messages.append(assistant_message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": weather_info
                })

second_response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=messages,
    max_tokens=100,
    temperature=0.7
)

final_reply = second_response.choices[0].message.content

print("Respuesta final del asistent")
print(final_reply)