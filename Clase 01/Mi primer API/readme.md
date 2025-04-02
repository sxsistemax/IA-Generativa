# Configuración para usar Groq API

## 1. Crear una cuenta en Groq
- Ir a [console.groq.com](https://console.groq.com) y registrarse.

## 2. Obtener una API Key
- Dentro de la consola de Groq, navegar a la sección de **API Keys**.
- Crear una nueva clave.
- **¡Copiarla y guardarla de forma segura!**

## 3. Añadir la API Key como variable de entorno usando un archivo `.env`
1. Crear un archivo llamado `.env` en el directorio raíz de tu proyecto.
2. Añadir la siguiente línea al archivo `.env`:
   GROQ_API_KEY=tu_api_key_aquí


#  Configurar el entorno de Python
## En Windows:
python -m venv venv

## En macOS/Linux:
python3 -m venv venv


# Activar el entorno virtual:
## En Windows:
.\venv\Scripts\activate

## En macOS/Linux:
source venv/bin/activate

# Instalar las librerías necesarias:
pip install groq python-dotenv

# Verificar que las librerías se instalaron correctamente:
pip list
