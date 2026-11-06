# 📄 Río Claro Facturas

## Descripción del proyecto

Río Claro Facturas es una aplicación web desarrollada con Python y Streamlit para automatizar el análisis, revisión y aprobación de facturas comerciales mediante servicios de inteligencia artificial de Microsoft Azure.

El sistema permite cargar documentos, extraer automáticamente información financiera, realizar una revisión humana, consultar un asistente inteligente y registrar las facturas aprobadas en servicios de almacenamiento de Azure.

## Objetivo

Desarrollar un sistema inteligente que facilite la gestión de facturas comerciales, reduzca errores de captura, identifique posibles documentos duplicados y permita mantener un proceso de aprobación con supervisión humana.

## Funcionalidades principales

1. **Carga de facturas:** permite cargar documentos PDF e imágenes.
2. **Extracción automática:** identifica proveedor, fecha, folio, subtotal, impuestos y total.
3. **Revisión humana:** permite verificar y corregir los datos extraídos.
4. **Asistente inteligente:** analiza la coherencia de los importes y señala posibles inconsistencias.
5. **Aprobación:** registra el nombre de la persona responsable.
6. **Detección de duplicados:** evita registrar nuevamente una factura existente.
7. **Almacenamiento en Azure:** guarda los documentos y sus datos.

## Tecnologías utilizadas

- Python 3.13.
- Streamlit.
- Microsoft Azure Document Intelligence.
- Microsoft Foundry.
- Azure Blob Storage.
- Azure Table Storage.
- Azure App Service.
- Azure Identity.
- Azure SDK for Python.

## Estructura del proyecto

```text
rio-claro-facturas/
│
├── app.py
├── extractor.py
├── storage.py
├── duplicados.py
├── foundry_agent.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Requisitos

- Python instalado.
- Cuenta de Microsoft Azure.
- Servicios de Azure configurados.
- Dependencias del proyecto instaladas.

## Configuración general

Crear un archivo `.env` en la carpeta principal del proyecto con las siguientes variables:

```env
DOCINT_ENDPOINT=
DOCINT_KEY=

AZURE_STORAGE_CONNECTION_STRING=
AZURE_STORAGE_CONTAINER=factura1

PROJECT_ENDPOINT=
FOUNDRY_AGENT_NAME=rio-claro-asistente
```

Las credenciales deben configurarse localmente y mantenerse privadas. No deben publicarse en GitHub.

## Instrucciones de ejecución local

1. Abrir la carpeta del proyecto en Visual Studio Code.
2. Crear y activar el entorno virtual.
3. Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

4. Ejecutar la aplicación:

```powershell
python -m streamlit run app.py
```

5. Abrir la dirección local que proporciona Streamlit, normalmente:

```text
http://localhost:8501
```

## Despliegue en Azure

La aplicación web se ha creado en Microsoft Azure mediante Azure App Service, utilizando Linux y Python 3.12.

**Dirección web del servicio:**

https://rio-claro-facturas-web-fwgkepcscehhhzbc.westus3-01.azurewebsites.net

El servicio está creado y en ejecución. La publicación del código de Streamlit y la configuración de sus dependencias y variables de entorno son pasos pendientes.

## Seguridad

- Las claves y cadenas de conexión se almacenan en variables de entorno.
- No se deben compartir credenciales en repositorios públicos.
- La aprobación final de las facturas corresponde a una persona responsable.

## Autores

Proyecto: Río Claro Facturas  
Organización: Distribuidora Río Claro

## Estado del proyecto

Aplicación desarrollada y probada localmente, con integración de servicios de inteligencia artificial y almacenamiento de Microsoft Azure. Actualmente se encuentra en proceso de publicación web.
