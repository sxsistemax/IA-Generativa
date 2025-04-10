# Requisitos
## Python Instalado: Igual que antes, necesitas Python (3.9+ recomendado para la librería de Gemini).
## Cuenta de Google y API Key para Gemini:
   Ve a Google AI Studio.
   Inicia sesión con tu cuenta de Google.
   Haz clic en "Get API key" -> "Create API key in new project".
   Copia la clave API generada y guárdala de forma segura.
## Entorno Virtual: Sigue los mismos pasos que en el ejemplo de Groq para crear y activar un entorno virtual si lo deseas.

## Crear entorno virtual (ej. llamado .venv)
python -m venv venv
## Activar el entorno virtual
## Windows (cmd.exe):
.\venv\Scripts\activate
## Windows (PowerShell):
.\venv\Scripts\Activate.ps1
## Linux/macOS:
source venv/bin/activate


# Instalar Librerías: Abre tu terminal (con el entorno virtual activado si usas uno) y ejecuta:
## pip install google-generativeai python-dotenv
*   `google-generativeai`: La librería oficial de Google para interactuar con modelos Gemini.
*   `python-dotenv`: Para cargar la API key desde un archivo `.env`.

# Crear archivo .env: 
## En la misma carpeta donde guardarás tu script de Python, crea un archivo llamado .env. Dentro de este archivo, añade tu API key de Google así:

## Archivo: .env
GOOGLE_API_KEY=TuClaveApiDeGoogleAqui

# Crear el Script de Python: 
## Guarda el siguiente código en un archivo, por ejemplo, gemini_local_test.py, en la misma carpeta que tu archivo .env.

# -*- coding: utf-8 -*-
# Archivo: gemini_local_test.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Configuración Inicial ---
print("Cargando configuración de Google Gemini...")

# Carga las variables del archivo .env
load_dotenv()

# Intenta obtener la API key desde las variables de entorno
google_api_key = os.getenv("GOOGLE_API_KEY")

configured = False  # Bandera para saber si la configuración fue exitosa

if not google_api_key:
    print("Error: La variable de entorno GOOGLE_API_KEY no está configurada.")
    print("Asegúrate de tener un archivo .env en la misma carpeta con GOOGLE_API_KEY=tu_clave")
else:
    try:
        # Configura la API Key globalmente para la librería de Gemini
        genai.configure(api_key=google_api_key)
        print("Cliente de Google Gemini configurado exitosamente.")
        configured = True
    except Exception as e:
        print(f"Ocurrió un error inesperado durante la configuración del cliente Gemini: {e}")

# --- Función para hacer la llamada al modelo Gemini ---
def generar_respuesta_gemini(prompt_usuario, modelo="gemini-1.5-flash-latest"):
    """
    Función para enviar un prompt a la API de Gemini y obtener una respuesta.

    Args:
        prompt_usuario (str): La pregunta o instrucción del usuario.
        modelo (str): El ID del modelo a usar (ej. 'gemini-1.5-flash-latest', 'gemini-1.5-pro-latest').

    Returns:
        str: La respuesta generada por el modelo o un mensaje de error.
    """
    if not configured:
        return "Error: El cliente de Gemini no está configurado. Revisa la API Key o errores previos."

    print(f"\nEnviando prompt al modelo '{modelo}': '{prompt_usuario}'")
    try:
        # Selecciona el modelo
        model = genai.GenerativeModel(modelo)

        # Configuración de generación (opcional, puedes ajustar)
        generation_config = genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=250  # Ajusta según necesites
        )

        # Genera el contenido
        response = model.generate_content(
            prompt_usuario,
            generation_config=generation_config
        )

        # Verifica si la respuesta fue bloqueada por seguridad
        if not response.parts:
            block_reason = "No especificada"
            try:
                block_reason = response.prompt_feedback.block_reason.name
            except Exception:
                pass
            print(f"Respuesta bloqueada por seguridad. Razón: {block_reason}")
            return f"Error: La respuesta fue bloqueada por la configuración de seguridad (Razón: {block_reason})."

        # Extrae el texto de la respuesta
        respuesta_texto = response.text
        print("Respuesta recibida.")
        return respuesta_texto

    except Exception as e:
        print(f"Ocurrió un error inesperado durante la llamada a Gemini: {e}")
        return f"Error inesperado: {e}"

# --- Ejemplos de Uso ---
if configured:  # Solo ejecuta si el cliente se configuró bien
    # Ejemplo 1: Pregunta simple
    prompt1 = "¿Qué es la Inteligencia Artificial Generativa?"
    respuesta1 = generar_respuesta_gemini(prompt1)
    print("\n--- Respuesta 1 (Gemini Flash) ---")
    print(respuesta1)
    
    # Ejemplo 2: Pregunta compleja
    prompt2 = "¿Cuáles son las diferencias entre la IA generativa y la IA tradicional?" 
    respuesta2 = generar_respuesta_gemini(prompt2)
    print("\n--- Respuesta 2 (Gemini Flash) ---")
    print(respuesta2)

    # Ejemplo 3: Petición con formato específico
    prompt3 = "Genera una lista con viñetas de 4 planetas del sistema solar."
    respuesta3 = generar_respuesta_gemini(prompt3)
    print("\n--- Respuesta 3 (Gemini Flash) ---")
    print(respuesta3)

else:
    print("\nNo se pueden ejecutar los ejemplos porque el cliente de Gemini no se inicializó correctamente.")

print("\n--- Fin del script ---")

