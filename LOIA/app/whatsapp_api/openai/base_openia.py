import os
from dotenv import load_dotenv
import openai
load_dotenv()


openai.api_key = os.getenv("OPEN_IA_KEY")
# client = OpenAI(api_key=os.getenv("OPEN_IA_KEY"))

# response =  client.chat.completions.create(
response =  openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role" : "system",
            "content" : "Te llamas LOIA,una bot capas de adaptarse a cualquier negocio, presentate como tal"
        },
        {
            "role" : "user",
            "content" : "Hola"
        }
    ],
    max_tokens=100,
    temperature=0.7
)


# print(response.choices[0].message)
print(response.choices[0].message.content)