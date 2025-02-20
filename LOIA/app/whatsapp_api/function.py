# funciones generales en la API

import os 
from dotenv import load_dotenv

load_dotenv()


class FuctionAPI :

    def __init__(self):
        pass

    def get_ApiReniec(self, dni):
        pass

    def get_Document(self, nombre):
        pass

    def get_Add_Appointments(self,fecha):
        pass

    def get_Yape_Payments(self):
        try:
            url_image_yape = os.getenv("URL_IMAGE_YAPE")
            name_usuaario = os.getenv("NAME_USUARIO")
            phone_yape = os.getenv("PHONE_YAPE")
            return  f"datos de la forma de pago: titular {name_usuaario}, numero : {phone_yape}, codigo qr {url_image_yape}"
        except Exception as e:
            print("errororrrrrrrrrrrrrrrr")
            # print(f"Error al obtener la imagen de pago: {e}")
            return "error"
        