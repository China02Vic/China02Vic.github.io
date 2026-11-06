# 📄 Río Claro Facturas

## Descripción del proyecto

Río Claro Facturas es una aplicación web desarrollada con Python y Streamlit para automatizar el análisis, revisión y aprobación de facturas comerciales mediante servicios de inteligencia artificial de Microsoft Azure.

El sistema permite cargar documentos, extraer automáticamente información financiera, realizar una revisión humana, consultar un asistente inteligente y registrar las facturas aprobadas en servicios de almacenamiento de Azure.

La aplicación se encuentra desplegada y funcionando en Microsoft Azure, por lo que puede utilizarse mediante una dirección web pública.

## Objetivo

Desarrollar un sistema inteligente que facilite la gestión de facturas comerciales, reduzca errores de captura, identifique posibles documentos duplicados y permita mantener un proceso de aprobación con supervisión humana.

## Funcionalidades principales

1. **Carga de facturas:** permite cargar documentos PDF e imágenes.
2. **Extracción automática:** identifica proveedor, fecha, folio, subtotal, impuestos y total mediante Azure Document Intelligence.
3. **Revisión humana:** permite verificar y corregir los datos extraídos.
4. **Asistente inteligente:** analiza la información de las facturas y señala posibles inconsistencias.
5. **Aprobación:** registra el nombre de la persona responsable de aprobar la factura.
6. **Detección de duplicados:** evita registrar nuevamente una factura existente.
7. **Almacenamiento en Azure:** guarda los documentos y sus datos mediante Azure Blob Storage y Azure Table Storage.
8. **Acceso web:** permite utilizar la aplicación desde un navegador mediante Azure App Service.

## Tecnologías utilizadas

- Python 3.13 (desarrollo local).
- Python 3.11 (entorno de Azure App Service).
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
- Credenciales y variables de entorno configuradas.

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

En el entorno de Azure, las variables de configuración se establecen desde las opciones de configuración de Azure App Service.

## Instrucciones de ejecución local

1. Abrir la carpeta del proyecto en Visual Studio Code.
2. Crear y activar un entorno virtual.
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

La aplicación web está desplegada en Microsoft Azure mediante Azure App Service, utilizando Linux y Python 3.11.

**Dirección web de la aplicación:**

https://rio-claro-facturas-web-fwgkepcscehhhzbc.westus3-01.azurewebsites.net/

La aplicación se encuentra publicada y disponible para su acceso desde un navegador web.

## Seguridad

- Las claves y cadenas de conexión se almacenan en variables de entorno.
- No se deben compartir credenciales en repositorios públicos.
- El archivo `.env` se mantiene fuera del repositorio público.
- La aprobación final de las facturas corresponde a una persona responsable.

## Pruebas realizadas

Se realizaron pruebas de funcionamiento para verificar los principales componentes del sistema:

- Carga y análisis de facturas comerciales.
- Extracción automática de información mediante Azure Document Intelligence.
- Respuesta del asistente inteligente de Microsoft Foundry.
- Revisión y corrección de datos por una persona responsable.
- Aprobación y registro de facturas.
- Almacenamiento de documentos y datos en los servicios de Azure.
- Identificación y bloqueo de facturas duplicadas.
- Acceso a la aplicación web desplegada en Azure.

Las pruebas confirmaron el funcionamiento de estos procesos.

## Autores

**Proyecto:** Río Claro Facturas  
**Organización:** Distribuidora Río Claro

## Estado del proyecto

**Proyecto desarrollado, desplegado y probado satisfactoriamente.**

La aplicación se encuentra funcionando en Microsoft Azure e integra servicios de inteligencia artificial, revisión humana, aprobación de facturas, detección de duplicados y almacenamiento en la nube.