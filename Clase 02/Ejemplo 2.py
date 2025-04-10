# -*- coding: utf-8 -*-
# Archivo: langchain_gemini_local.py

import os
from dotenv import load_dotenv

# --- Importaciones Clave de LangChain ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

print("Cargando configuración y librerías...")

# Carga la API Key desde el archivo .env
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

llm = None # Inicializa la variable del LLM

if not google_api_key:
    print("Error: GOOGLE_API_KEY no encontrada en el entorno.")
    print("Asegúrate de tener un archivo .env con tu clave.")
else:
    try:
        # --- 1. Instanciar el Modelo LLM ---
        # Usamos el wrapper de LangChain para Gemini
        # Puedes añadir 'temperature', 'max_output_tokens', etc. aquí
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest", # O "gemini-1.5-pro-latest"
            google_api_key=google_api_key, # Langchain puede usar la variable de entorno o pasarla directamente
            temperature=0.7,
            # Opcional: Configuración de seguridad más permisiva si enfrentas bloqueos
            # safety_settings={
            #     HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            #     HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            # } # Necesitarías importar HarmCategory y HarmBlockThreshold de google.generativeai.types
        )
        print("Modelo ChatGoogleGenerativeAI instanciado correctamente.")

    except ImportError:
         print("Error: Parece que 'google.generativeai' no está instalado correctamente.")
         print("Ejecuta: pip install google-generativeai")
    except Exception as e:
        print(f"Error al instanciar ChatGoogleGenerativeAI: {e}")


# Solo proceder si el LLM se instanció correctamente
if llm:
    try:
        # --- 2. Crear la Plantilla de Prompt ---
        # Define la estructura del prompt con variables entre llaves {}
        template_string = """Eres un asistente experto en {area_conocimiento}.
        Tu tarea es explicar el concepto de '{concepto}' de una manera muy simple y clara,
        como si hablaras con alguien que no sabe nada del tema.
        Usa 2-3 frases como máximo."""

        prompt_template = ChatPromptTemplate.from_template(template_string)
        print("Plantilla de Prompt creada.")

        # --- 3. Crear el Parser de Salida ---
        # StrOutputParser simplemente extrae el contenido de texto de la respuesta del LLM
        output_parser = StrOutputParser()
        print("Parser de Salida (StrOutputParser) creado.")

        # --- 4. Construir la Cadena (Chain) usando LCEL (|) ---
        # Conectamos los componentes en secuencia
        chain = prompt_template | llm | output_parser
        print("Cadena LangChain (LCEL) construida: template | llm | parser")

        # --- 5. Invocar la Cadena ---
        print("\n--- Invocando la cadena ---")
        # Proporcionamos los valores para las variables del prompt template
        input_data = {
            "area_conocimiento": "programación",
            "concepto": "API (Interfaz de Programación de Aplicaciones)"
        }
        print(f"Entrada: {input_data}")

        # .invoke ejecuta la cadena completa
        response = chain.invoke(input_data)

        print("\n--- Respuesta de la Cadena ---")
        print(response)
        print(f"Tipo de la respuesta: {type(response)}") # Debería ser <class 'str'>

        # --- Otro ejemplo de invocación ---
        print("\n--- Invocando la cadena con otros datos ---")
        input_data_2 = {
            "area_conocimiento": "finanzas personales",
            "concepto": "interés compuesto"
        }
        print(f"Entrada: {input_data_2}")
        response_2 = chain.invoke(input_data_2)
        print("\n--- Respuesta de la Cadena ---")
        print(response_2)

    except Exception as e:
        print(f"\nOcurrió un error durante la ejecución de la cadena LangChain: {e}")

else:
    print("\nNo se puede continuar porque el modelo LLM (Gemini) no se inicializó correctamente.")

print("\n--- Fin del script ---")