
import os
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTENEDOR = os.getenv("AZURE_STORAGE_CONTAINER", "factura1")
TABLA = "Facturas"


def subir_factura(nombre_archivo, contenido):
    if not CONNECTION_STRING:
        raise ValueError("Falta la cadena de conexión en .env")

    servicio = BlobServiceClient.from_connection_string(
        CONNECTION_STRING
    )

    contenedor = servicio.get_container_client(CONTENEDOR)

    nombre_limpio = os.path.basename(nombre_archivo)
    nombre_blob = f"{uuid.uuid4().hex}_{nombre_limpio}"

    blob = contenedor.get_blob_client(nombre_blob)
    blob.upload_blob(contenido, overwrite=False)

    return nombre_blob


def guardar_en_tabla(factura):
    if not CONNECTION_STRING:
        raise ValueError("Falta la cadena de conexión en .env")

    servicio = TableServiceClient.from_connection_string(
        conn_str=CONNECTION_STRING
    )

    tabla = servicio.get_table_client(table_name=TABLA)

    entidad = {
        "PartitionKey": "Facturas",
        "RowKey": str(uuid.uuid4()),
        "proveedor": str(factura.get("proveedor", "")),
        "fecha": str(factura.get("fecha", "")),
        "folio": str(factura.get("folio", "")),
        "subtotal": str(factura.get("subtotal", "")),
        "impuestos": str(factura.get("impuestos", "")),
        "total": str(factura.get("total", "")),
        "responsable_aprobacion": str(
            factura.get("responsable_aprobacion", "")
        ),
        "fecha_hora_aprobacion": str(
            factura.get("fecha_hora_aprobacion", "")
        ),
        "archivo_azure": str(factura.get("archivo_azure", ""))
    }

    tabla.create_entity(entity=entidad)

    return entidad["RowKey"]
