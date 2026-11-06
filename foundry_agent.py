
import os
from functools import lru_cache

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()


@lru_cache(maxsize=1)
def obtener_cliente_agente():

    endpoint = os.getenv("PROJECT_ENDPOINT")
    nombre_agente = os.getenv("FOUNDRY_AGENT_NAME")

    if not endpoint:
        raise ValueError("Falta PROJECT_ENDPOINT en el archivo .env")

    if not nombre_agente:
        raise ValueError("Falta FOUNDRY_AGENT_NAME en el archivo .env")

    credencial = DefaultAzureCredential()

    proyecto = AIProjectClient(
        endpoint=endpoint,
        credential=credencial
    )

    cliente = proyecto.get_openai_client()

    return cliente


def consultar_agente(mensaje):

    cliente = obtener_cliente_agente()
    nombre_agente = os.getenv("FOUNDRY_AGENT_NAME")

    respuesta = cliente.responses.create(
        input=mensaje,
        extra_body={
            "agent_reference": {
                "name": nombre_agente,
                "type": "agent_reference"
            }
        }
    )

    return respuesta.output_text
