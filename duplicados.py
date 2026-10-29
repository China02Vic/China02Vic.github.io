
import json
import os

ARCHIVO_REGISTRO = "facturas.json"


def cargar_facturas():
    if not os.path.exists(ARCHIVO_REGISTRO):
        return []

    with open(ARCHIVO_REGISTRO, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def es_duplicada(factura):
    facturas = cargar_facturas()

    proveedor = str(factura.get("proveedor") or "").strip().casefold()
    folio = str(factura.get("folio") or "").strip().casefold()
    total = str(factura.get("total") or "").strip()

    if not proveedor or not folio or not total:
        return False

    for registrada in facturas:
        mismo_proveedor = (
            str(registrada.get("proveedor") or "").strip().casefold()
            == proveedor
        )
        mismo_folio = (
            str(registrada.get("folio") or "").strip().casefold()
            == folio
        )
        mismo_total = (
            str(registrada.get("total") or "").strip() == total
        )

        if mismo_proveedor and mismo_folio and mismo_total:
            return True

    return False


def guardar_factura(factura):
    if es_duplicada(factura):
        return False

    facturas = cargar_facturas()
    facturas.append(factura)

    with open(ARCHIVO_REGISTRO, "w", encoding="utf-8") as archivo:
        json.dump(facturas, archivo, ensure_ascii=False, indent=4)

    return True
