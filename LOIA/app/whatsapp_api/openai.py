import os
from dotenv import load_dotenv
import openai
import json
load_dotenv()

from .function import FuctionAPI

class FunctionOpenAI :
    openai.api_key = os.getenv("OPEN_IA_KEY")

    def __init__(self):
        pass

    @classmethod
    def baseOpenai(self, prompt):
       
        consulta = prompt
        response =  openai.ChatCompletion.create(
        model = "gpt-4o-mini",
      
        messages=[
            {
                "role" : "system",
                "content" : "Te llamas LOIA,una bot capas de adaptarse a cualquier negocio, presentate como tal"
            },
            {
                "role" : "user",
                "content" : consulta
            }
        ],
        max_tokens=100,
        temperature=0.7
        )
        respuesta = response.choices[0].message.content
        return respuesta
    

    @classmethod
    def function_openai(self, prompt):
       
        consulta = prompt
        # traemos la funciones a usar
        functionAPI = FuctionAPI()
        # mesajes
        messages=[
            {
                "role" : "system",
                "content" : "Te llamas LOIA,una bot capas de adaptarse a cualquier negocio, presentate como tal"
            },
            {
                "role" : "user",
                "content" : consulta
            }
        ]

      

