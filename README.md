# Río Claro Facturas

Aplicación web para procesar facturas de la Distribuidora Río Claro.

## Funciones principales

- Extracción automática de datos mediante Azure AI Document Intelligence.
- Revisión y corrección manual de los datos extraídos.
- Detección de posibles facturas duplicadas.
- Aprobación de facturas por una persona responsable.
- Almacenamiento de documentos en Azure Blob Storage.
- Registro de información en Azure Table Storage.

## Tecnologías utilizadas

- Python
- Streamlit
- Azure AI Document Intelligence
- Azure Blob Storage
- Azure Table Storage

## Ejecución local

1. Instalar las dependencias con:

   pip install -r requirements.txt

2. Configurar las variables de entorno en un archivo .env.

3. Ejecutar la aplicación con:

   streamlit run app.py

## Seguridad

No se deben publicar claves de Azure, cadenas de conexión, archivos .env ni facturas reales.
