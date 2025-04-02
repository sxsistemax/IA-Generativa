import openai
import os
from dotenv import load_dotenv  # Para cargar variables desde el archivo .env

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configura tu API Key desde las variables de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

def generar_respuesta(modelo, mensajes):
    """
    Genera una respuesta utilizando la API de OpenAI.

    Args:
        modelo (str): El modelo de OpenAI a utilizar (por ejemplo, 'gpt-4o').
        mensajes (list): Lista de mensajes en formato [{"role": "system", "content": "..."}, ...]

    Returns:
        str: Respuesta generada por el modelo.
    """
    try:
        response = openai.ChatCompletion.create(
            model=modelo,
            messages=mensajes
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ocurrió un error: {e}"

if __name__ == "__main__":
    # Ejemplo de uso
    modelo = "gpt-4o"  # Modelo a utilizar
    mensajes = [
        {"role": "system", "content": "Eres un asistente muy creativo."},
        {"role": "user", "content": "Escribe un haiku sobre el amanecer en la ciudad."}
    ]

    respuesta = generar_respuesta(modelo, mensajes)
    print(respuesta)