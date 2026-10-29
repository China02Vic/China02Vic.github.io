
from extractor import extraer_factura

archivo = "Factura Comercial Ficticia - Río Claro.pdf"

try:
    datos = extraer_factura(archivo)

    print("\n--- DATOS DE LA FACTURA ---")

    for nombre, informacion in datos.items():
        print(f"{nombre}: {informacion['valor']}")
        print(f"Confianza: {informacion['confianza']}")

except Exception as error:
    print("Error:", error)
