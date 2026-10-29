
import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

load_dotenv()


def extraer_factura(ruta_archivo):
    endpoint = os.getenv("DOCINT_ENDPOINT")
    key = os.getenv("DOCINT_KEY")

    if not endpoint or not key:
        raise ValueError("Faltan las credenciales de Azure en el archivo .env")

    if not os.path.isfile(ruta_archivo):
        raise FileNotFoundError("No se encontró el archivo de la factura.")

    extension = os.path.splitext(ruta_archivo)[1].lower()

    if extension not in [".pdf", ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp"]:
        raise ValueError("El archivo debe ser PDF o una imagen compatible.")

    client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    with open(ruta_archivo, "rb") as archivo:
        resultado = client.begin_analyze_document(
            "prebuilt-invoice",
            body=archivo,
            content_type="application/pdf" if extension == ".pdf" else "application/octet-stream"
        ).result()

    if not resultado.documents:
        raise ValueError("Azure no pudo identificar una factura en el archivo.")

    campos = resultado.documents[0].fields

    def obtener_campo(nombre):
        campo = campos.get(nombre)

        if campo is None:
            return {"valor": None, "confianza": None}

        return {
            "valor": campo.content,
            "confianza": campo.confidence
        }

    return {
        "proveedor": obtener_campo("VendorName"),
        "fecha": obtener_campo("InvoiceDate"),
        "folio": obtener_campo("InvoiceId"),
        "subtotal": obtener_campo("SubTotal"),
        "impuestos": obtener_campo("TotalTax"),
        "total": obtener_campo("InvoiceTotal")
    }
