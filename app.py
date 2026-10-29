
from duplicados import guardar_factura, es_duplicada
from storage import subir_factura, guardar_en_tabla
from datetime import datetime
import streamlit as st
import tempfile
import os
from extractor import extraer_factura


# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Río Claro Facturas",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# DISEÑO EMPRESARIAL
# ==========================================

st.markdown("""
<style>
    /* Fondo general */
    .stApp {
        background-color: #F4F7FB;
    }

    /* Área principal */
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Encabezado */
    .encabezado {
        background: linear-gradient(135deg, #102A43, #174A70);
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 25px;
        color: white;
        border-bottom: 5px solid #27AE60;
    }

    .encabezado h1 {
        color: white;
        font-size: 34px;
        margin-bottom: 8px;
    }

    .encabezado p {
        color: #E3EDF5;
        font-size: 16px;
        margin-bottom: 0;
    }

    /* Tarjetas de secciones */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 14px;
        border-color: #DCE5EE;
    }

    /* Títulos */
    h2, h3 {
        color: #163A59 !important;
    }

    /* Botones */
    .stButton > button,
    .stFormSubmitButton > button {
        background-color: #174A70;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        min-height: 44px;
        transition: 0.2s;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background-color: #102A43;
        color: white;
        border: 1px solid #27AE60;
    }

    /* Campos de texto */
    .stTextInput input {
        border-radius: 7px;
        border-color: #CBD5E1;
        background-color: white;
    }

    /* Cargador de archivos */
    [data-testid="stFileUploader"] {
        background-color: #F8FAFC;
        border-radius: 10px;
    }

    /* Separadores */
    hr {
        border-color: #DCE5EE;
    }

    /* Pie de página */
    .pie-pagina {
        text-align: center;
        color: #64748B;
        font-size: 13px;
        padding-top: 25px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# ENCABEZADO
# ==========================================

st.markdown("""
<div class="encabezado">
    <h1>📄 Río Claro Facturas</h1>
    <p>
        DISTRIBUIDORA RÍO CLARO<br>
        Sistema inteligente de análisis, revisión y aprobación de facturas.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# ESTADO DE LA APLICACIÓN
# ==========================================

if "datos_factura" not in st.session_state:
    st.session_state["datos_factura"] = None

if "resultado_aprobacion" not in st.session_state:
    st.session_state["resultado_aprobacion"] = None

if "revision_confirmada" not in st.session_state:
    st.session_state["revision_confirmada"] = False


# ==========================================
# SECCIÓN 1: ANÁLISIS DE FACTURAS
# ==========================================

with st.container(border=True):

    st.subheader("📤 1. Análisis de factura")

    st.write(
        "Carga una factura para extraer automáticamente "
        "los datos mediante inteligencia artificial."
    )

    archivo = st.file_uploader(
        "Selecciona el documento",
        type=["pdf", "jpg", "jpeg", "png", "tif", "tiff", "bmp"],
        help="Formatos permitidos: PDF e imágenes."
    )

    if archivo is not None:

        st.info(f"Documento seleccionado: {archivo.name}")

        if st.button(
            "🔍 Analizar factura",
            key="analizar_factura"
        ):

            ruta_temporal = None

            try:
                extension = os.path.splitext(
                    archivo.name
                )[1].lower()

                contenido = archivo.getvalue()

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=extension
                ) as temporal:

                    temporal.write(contenido)
                    ruta_temporal = temporal.name

                with st.spinner(
                    "Analizando el documento con Azure..."
                ):

                    datos = extraer_factura(ruta_temporal)

                st.session_state["datos_factura"] = datos
                st.session_state["archivo_nombre"] = archivo.name
                st.session_state["archivo_contenido"] = contenido
                st.session_state["resultado_aprobacion"] = None
                st.session_state["revision_confirmada"] = False

                st.session_state.pop(
                    "datos_corregidos",
                    None
                )

                st.success(
                    "Análisis terminado. "
                    "Continúa con la revisión humana."
                )

            except Exception as error:

                st.error(
                    f"No se pudo analizar la factura: {error}"
                )

            finally:

                if ruta_temporal and os.path.exists(
                    ruta_temporal
                ):
                    os.remove(ruta_temporal)


# ==========================================
# SECCIÓN 2: REVISIÓN HUMANA
# ==========================================

if st.session_state["datos_factura"] is not None:

    datos = st.session_state["datos_factura"]

    st.write("")

    with st.container(border=True):

        st.subheader("📝 2. Revisión humana")

        st.write(
            "Compara los datos extraídos con el documento original. "
            "Puedes corregir la información antes de aprobar."
        )

        proveedor_original = datos["proveedor"]["valor"] or ""
        fecha_original = datos["fecha"]["valor"] or ""
        folio_original = datos["folio"]["valor"] or ""
        subtotal_original = datos["subtotal"]["valor"] or ""
        impuestos_original = datos["impuestos"]["valor"] or ""
        total_original = datos["total"]["valor"] or ""

        with st.form("formulario_revision"):

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("#### Datos del proveedor")

                proveedor = st.text_input(
                    "Nombre del proveedor",
                    value=proveedor_original
                )

                fecha = st.text_input(
                    "Fecha de la factura",
                    value=fecha_original
                )

                folio = st.text_input(
                    "Número de factura",
                    value=folio_original
                )

            with col2:

                st.markdown("#### Información financiera")

                subtotal = st.text_input(
                    "Subtotal",
                    value=subtotal_original
                )

                impuestos = st.text_input(
                    "Impuestos",
                    value=impuestos_original
                )

                total = st.text_input(
                    "Total de la factura",
                    value=total_original
                )

            st.divider()

            confirmar_datos = st.checkbox(
                "Confirmo que comparé los datos con la factura original"
            )

            guardar_revision = st.form_submit_button(
                "✓ Guardar revisión",
                use_container_width=True
            )

        if guardar_revision:

            if not all([
                proveedor.strip(),
                fecha.strip(),
                folio.strip(),
                total.strip()
            ]):

                st.error(
                    "Completa el proveedor, la fecha, "
                    "el folio y el total."
                )

            elif not confirmar_datos:

                st.warning(
                    "Confirma que revisaste los datos "
                    "con la factura original."
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

                st.session_state[
                    "datos_corregidos"
                ] = datos_corregidos

                st.session_state[
                    "revision_confirmada"
                ] = True

                st.session_state[
                    "resultado_aprobacion"
                ] = None

                st.success(
                    "Revisión guardada correctamente."
                )


# ==========================================
# SECCIÓN 3: APROBACIÓN
# ==========================================

if st.session_state.get("revision_confirmada", False):

    st.write("")

    with st.container(border=True):

        st.subheader("✅ 3. Aprobación de factura")

        st.write(
            "Ingresa el nombre de la persona responsable "
            "y verifica que la información sea correcta."
        )

        responsable = st.text_input(
            "Persona responsable de aprobar",
            key="responsable_aprobacion"
        )

        st.warning(
            "La aprobación guardará el archivo y sus datos "
            "en Azure si la factura no está duplicada."
        )

        if st.button(
            "✓ Aprobar y registrar factura",
            key="aprobar_factura",
            use_container_width=True
        ):

            if not responsable.strip():

                st.warning(
                    "Escribe el nombre de la persona responsable."
                )

            elif not st.session_state.get(
                "archivo_contenido"
            ):

                st.error(
                    "No se encontró el archivo original. "
                    "Vuelve a seleccionar y analizar la factura."
                )

            else:

                factura = st.session_state[
                    "datos_corregidos"
                ].copy()

                factura["responsable_aprobacion"] = (
                    responsable.strip()
                )

                factura["fecha_hora_aprobacion"] = (
                    datetime.now().astimezone().isoformat(
                        timespec="seconds"
                    )
                )

                try:

                    if es_duplicada(factura):

                        st.session_state[
                            "resultado_aprobacion"
                        ] = (
                            "Posible factura duplicada. "
                            "No se subió ni registró nuevamente."
                        )

                    else:

                        with st.spinner(
                            "Guardando factura y datos en Azure..."
                        ):

                            nombre_blob = subir_factura(
                                st.session_state[
                                    "archivo_nombre"
                                ],
                                st.session_state[
                                    "archivo_contenido"
                                ]
                            )

                            factura["archivo_azure"] = nombre_blob

                            guardar_en_tabla(factura)

                            guardada = guardar_factura(factura)

                        if guardada:

                            st.session_state[
                                "resultado_aprobacion"
                            ] = (
                                "Factura aprobada. "
                                "Archivo guardado en Azure "
                                "y datos registrados correctamente."
                            )

                        else:

                            st.session_state[
                                "resultado_aprobacion"
                            ] = (
                                "La factura ya estaba registrada. "
                                "No se agregó otro registro."
                            )

                except Exception as error:

                    st.error(
                        "No se pudo completar el guardado. "
                        f"Detalle: {type(error).__name__}: {error}"
                    )


# ==========================================
# RESULTADO DE LA OPERACIÓN
# ==========================================

resultado = st.session_state.get(
    "resultado_aprobacion"
)

if resultado:

    st.write("")

    if resultado.startswith("Factura aprobada"):

        st.success(f"🎉 {resultado}")

    else:

        st.warning(f"⚠️ {resultado}")


# ==========================================
# PIE DE PÁGINA
# ==========================================

st.markdown("""
<hr>
<div class="pie-pagina">
    <strong>Río Claro Facturas</strong><br>
    Sistema inteligente de gestión de facturas<br>
    Distribuidora Río Claro
</div>
""", unsafe_allow_html=True)