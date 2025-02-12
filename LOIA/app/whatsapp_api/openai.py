import os
from dotenv import load_dotenv
import openai
load_dotenv()



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
