from app.config import get_settings
from app.context.examples import ESTIMATION_EXAMPLES

SYSTEM_PROMPT_TEMPLATE = """Eres un estimador de software experto. Tu trabajo es generar \
estimaciones de esfuerzo (horas, equipo recomendado y duracion) para nuevos proyectos, \
basandote en la transcripcion de una reunion con el cliente.

Usa como referencia las siguientes estimaciones previas realizadas por el equipo. \
Sigue un formato y nivel de detalle similar al de estos ejemplos.

{examples_block}

Genera la estimacion para la nueva transcripcion que te proporcione el usuario, \
siguiendo el mismo formato (desglose de tareas con horas, total estimado, equipo \
recomendado y duracion estimada)."""


def _build_examples_block() -> str:
    blocks = []
    for i, example in enumerate(ESTIMATION_EXAMPLES, start=1):
        blocks.append(
            f"### Ejemplo {i}\n"
            f"**Resumen de la reunion:** {example['meeting_summary']}\n"
            f"**Estimacion generada:**\n{example['estimation']}"
        )
    return "\n\n".join(blocks)


def _build_system_prompt() -> str:
    return SYSTEM_PROMPT_TEMPLATE.format(examples_block=_build_examples_block())


def _call_openai(system_prompt: str, transcription: str, model: str) -> str:
    from openai import OpenAI

    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcription},
        ],
    )
    return response.choices[0].message.content or ""


def _call_anthropic(system_prompt: str, transcription: str, model: str) -> str:
    from anthropic import Anthropic

    settings = get_settings()
    client = Anthropic(api_key=settings.anthropic_api_key)

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": transcription}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def generate_estimation(transcription: str) -> tuple[str, str, str]:
    """Genera una estimacion inyectando el contexto estatico en el prompt (CAG).

    Devuelve una tupla (estimation, model, provider).
    """
    settings = get_settings()
    system_prompt = _build_system_prompt()

    if settings.llm_provider == "anthropic":
        estimation = _call_anthropic(system_prompt, transcription, settings.llm_model)
    else:
        estimation = _call_openai(system_prompt, transcription, settings.llm_model)

    return estimation, settings.llm_model, settings.llm_provider
