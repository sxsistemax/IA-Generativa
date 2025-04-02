import groq
import os
from dotenv import load_dotenv  # Para cargar variables desde el archivo .env

# --- Configuración Inicial ---
print("Configurando cliente de Groq...")
try:
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener la API Key desde las variables de entorno
    groq_api_key = os.getenv('GROQ_API_KEY')

    if not groq_api_key:
        raise ValueError("API Key de Groq no encontrada en las variables de entorno. "
                         "Por favor, asegúrate de definir GROQ_API_KEY en tu archivo .env.")

    # Crea el cliente de Groq
    client = groq.Groq(api_key=groq_api_key)
    print("Cliente de Groq configurado exitosamente.")

except ValueError as ve:
    print(f"Error de configuración: {ve}")
    client = None  # Indica que el cliente no se pudo crear
except Exception as e:
    print(f"Ocurrió un error inesperado durante la configuración: {e}")
    client = None

# --- Función para hacer la llamada al modelo ---
def generar_respuesta_groq(prompt_usuario, modelo="llama3-8b-8192"):
    """
    Función para enviar un prompt a la API de Groq y obtener una respuesta.

    Args:
        prompt_usuario (str): La pregunta o instrucción del usuario.
        modelo (str): El ID del modelo a usar en Groq (ej. 'llama3-8b-8192', 'mixtral-8x7b-32768').

    Returns:
        str: La respuesta generada por el modelo o un mensaje de error.
    """
    if not client:
        return "Error: El cliente de Groq no está configurado. Revisa la API Key."

    print(f"\nEnviando prompt al modelo '{modelo}': '{prompt_usuario}'")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Eres un asistente útil y conciso."  # Puedes ajustar el rol del sistema
                },
                {
                    "role": "user",
                    "content": prompt_usuario,
                }
            ],
            model=modelo,
            temperature=0.7,  # Puedes experimentar con este valor (0.0 a 1.0+)
            max_tokens=150,  # Límite de tokens en la respuesta
            # top_p=1,         # Otros parámetros opcionales
            # stop=None,
            # stream=False,    # Poner True para recibir la respuesta palabra por palabra (más avanzado)
        )
        respuesta = chat_completion.choices[0].message.content
        print("Respuesta recibida.")
        return respuesta

    except groq.APIError as e:
        print(f"Error de la API de Groq: {e}")
        return f"Error de API: {e}"
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return f"Error inesperado: {e}"

# --- Ejemplos de Uso ---
if client:  # Solo ejecuta si el cliente se configuró bien
    # Ejemplo 1: Pregunta simple
    prompt1 = "¿Qué es la Inteligencia Artificial Generativa?"
    respuesta1 = generar_respuesta_groq(prompt1)
    print("\n--- Respuesta 1 ---")
    print(respuesta1)

    # Ejemplo 2: Petición creativa (usando Mixtral, si está disponible y quieres probar otro modelo)
    # Nota: Revisa los modelos disponibles en la documentación de Groq o en su consola.
    prompt2 = "Escribe 3 ideas para un nombre de una tienda de plantas exóticas."
    respuesta2 = generar_respuesta_groq(prompt2, modelo="mixtral-8x7b-32768")  # Cambia si prefieres Llama3 u otro
    print("\n--- Respuesta 2 ---")
    print(respuesta2)

    # Ejemplo 3: Petición con formato específico
    prompt3 = "Genera una lista con viñetas de 4 planetas del sistema solar."
    respuesta3 = generar_respuesta_groq(prompt3)
    print("\n--- Respuesta 3 ---")
    print(respuesta3)

else:
    print("\nNo se pueden ejecutar los ejemplos porque el cliente de Groq no se inicializó correctamente.")