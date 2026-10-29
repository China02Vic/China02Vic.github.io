
from duplicados import guardar_factura, es_duplicada
from storage import subir_factura, guardar_en_tabla
from datetime import datetime
import streamlit as st
import tempfile
import os
from extractor import extraer_factura

st.set_page_config(
    page_title="Río Claro Facturas",
    page_icon="📄",
    layout="centered"
)

st.title("Procesador inteligente de facturas")
st.subheader("Distribuidora Río Claro")

st.write(
    "Sube una factura en PDF o imagen para extraer "
    "sus datos automáticamente."
)

if "datos_factura" not in st.session_state:
    st.session_state["datos_factura"] = None

if "resultado_aprobacion" not in st.session_state:
    st.session_state["resultado_aprobacion"] = None

if "revision_confirmada" not in st.session_state:
    st.session_state["revision_confirmada"] = False

archivo = st.file_uploader(
    "Selecciona una factura",
    type=["pdf", "jpg", "jpeg", "png", "tif", "tiff", "bmp"]
)

if archivo is not None:
    st.write("Archivo seleccionado:", archivo.name)

    if st.button("Analizar factura"):
        ruta_temporal = None

        try:
            extension = os.path.splitext(archivo.name)[1].lower()

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=extension
            ) as temporal:
                contenido = archivo.getvalue()
                temporal.write(contenido)
                ruta_temporal = temporal.name

            with st.spinner("Analizando factura..."):
                datos = extraer_factura(ruta_temporal)

            st.session_state["datos_factura"] = datos
            st.session_state["archivo_nombre"] = archivo.name
            st.session_state["archivo_contenido"] = contenido
            st.session_state["resultado_aprobacion"] = None
            st.session_state["revision_confirmada"] = False

            st.success("Análisis terminado")

        except Exception as error:
            st.error(f"No se pudo analizar la factura: {error}")

        finally:
            if ruta_temporal and os.path.exists(ruta_temporal):
                os.remove(ruta_temporal)

if st.session_state["datos_factura"] is not None:
    datos = st.session_state["datos_factura"]

    st.subheader("Datos extraídos y editables")
    st.write(
        "Verifica cada dato con la factura original. "
        "Puedes corregir los campos antes de aprobar."
    )

    proveedor_original = datos["proveedor"]["valor"] or ""
    fecha_original = datos["fecha"]["valor"] or ""
    folio_original = datos["folio"]["valor"] or ""
    subtotal_original = datos["subtotal"]["valor"] or ""
    impuestos_original = datos["impuestos"]["valor"] or ""
    total_original = datos["total"]["valor"] or ""

    with st.form("formulario_revision"):
        proveedor = st.text_input(
            "Proveedor",
            value=proveedor_original
        )

        fecha = st.text_input(
            "Fecha",
            value=fecha_original
        )

        folio = st.text_input(
            "Número de factura",
            value=folio_original
        )

        subtotal = st.text_input(
            "Subtotal",
            value=subtotal_original
        )

        impuestos = st.text_input(
            "Impuestos",
            value=impuestos_original
        )

        total = st.text_input(
            "Total",
            value=total_original
        )

        confirmar_datos = st.checkbox(
            "Confirmo que comparé los datos con la factura original"
        )

        guardar_revision = st.form_submit_button(
            "Guardar revisión"
        )

    if guardar_revision:
        if not all([
            proveedor.strip(),
            fecha.strip(),
            folio.strip(),
            total.strip()
        ]):
            st.error(
                "Completa el proveedor, la fecha, el folio y el total."
            )
        elif not confirmar_datos:
            st.warning(
                "Confirma que revisaste los datos con la factura original."
            )
        else:
            datos_corregidos = {
                "proveedor": proveedor.strip(),
                "fecha": fecha.strip(),
                "folio": folio.strip(),
                "subtotal": subtotal.strip(),
                "impuestos": impuestos.strip(),
                "total": total.strip()
            }

            st.session_state["datos_corregidos"] = datos_corregidos
            st.session_state["revision_confirmada"] = True
            st.session_state["resultado_aprobacion"] = None

            st.success(
                "Revisión guardada. Ya puedes intentar aprobar la factura."
            )

if st.session_state.get("revision_confirmada", False):
    st.subheader("Aprobación de factura")

    responsable = st.text_input(
        "Nombre de la persona responsable de aprobar",
        key="responsable_aprobacion"
    )

    st.write(
        "Verifica la información antes de aprobar la factura."
    )

    if st.button("Aprobar factura"):
        if not responsable.strip():
            st.warning(
                "Escribe el nombre de la persona responsable."
            )

        elif not st.session_state.get("archivo_contenido"):
            st.error(
                "No se encontró el archivo original. "
                "Vuelve a seleccionar y analizar la factura."
            )

        else:
            factura = st.session_state["datos_corregidos"].copy()

            factura["responsable_aprobacion"] = responsable.strip()
            factura["fecha_hora_aprobacion"] = (
                datetime.now().astimezone().isoformat(
                    timespec="seconds"
                )
            )

            try:
                if es_duplicada(factura):
                    st.session_state["resultado_aprobacion"] = (
                        "Posible factura duplicada. "
                        "No se subió ni registró nuevamente."
                    )

                else:
                    with st.spinner("Guardando factura en Azure..."):
                        nombre_blob = subir_factura(
                            st.session_state["archivo_nombre"],
                            st.session_state["archivo_contenido"]
                        )

                        factura["archivo_azure"] = nombre_blob

                        # Guardar los datos en Azure Table Storage
                        guardar_en_tabla(factura)

                        # Guardar también el registro local
                        guardada = guardar_factura(factura)

                    if guardada:
                        st.session_state["resultado_aprobacion"] = (
                            "Factura aprobada. Archivo guardado en Azure "
                            "y datos registrados correctamente."
                        )
                    else:
                        st.session_state["resultado_aprobacion"] = (
                            "La factura ya estaba registrada. "
                            "No se agregó otro registro."
                        )

            except Exception as error:
                st.error(
                    "No se pudo completar el guardado. "
                    f"Detalle: {type(error).__name__}: {error}"
                )

resultado = st.session_state.get("resultado_aprobacion")

if resultado:
    if resultado.startswith("Factura aprobada"):
        st.success(resultado)
    else:
        st.warning(resultado)

