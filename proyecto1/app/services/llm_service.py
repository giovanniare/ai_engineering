from dataclasses import dataclass

from app.config import Settings, get_settings
from app.context.examples import ESTIMATION_EXAMPLES

SYSTEM_PROMPT_TEMPLATE = """Eres un estimador de software experto con anios de experiencia \
en consultoria tecnica. Tu trabajo es leer la transcripcion de una reunion con un cliente y \
generar una estimacion de esfuerzo detallada (desglose de tareas, horas, equipo recomendado \
y duracion), tal como lo haria un tech lead senior.

Usa como referencia las siguientes estimaciones previas que el equipo ha generado para \
proyectos similares. Sigue un formato y nivel de detalle equivalente al de estos ejemplos.

{examples_block}

Genera la estimacion para la nueva transcripcion que te proporcione el usuario, siguiendo \
el mismo formato Markdown (titulo, desglose numerado de tareas con horas, total de horas, \
equipo recomendado y duracion estimada)."""


def _build_examples_block() -> str:
    blocks = []
    for i, example in enumerate(ESTIMATION_EXAMPLES, start=1):
        blocks.append(
            f"### Ejemplo {i}\n\n"
            f"**Resumen de la reunion:**\n{example['meeting_summary']}\n\n"
            f"**Estimacion generada:**\n{example['estimation']}"
        )
    return "\n\n---\n\n".join(blocks)


def build_system_prompt() -> str:
    return SYSTEM_PROMPT_TEMPLATE.format(examples_block=_build_examples_block())


@dataclass
class EstimationResult:
    estimation: str
    model: str
    provider: str


def generate_estimation(transcription: str, settings: Settings | None = None) -> EstimationResult:
    settings = settings or get_settings()
    system_prompt = build_system_prompt()

    if settings.llm_provider == "openai":
        return _generate_with_openai(system_prompt, transcription, settings)
    return _generate_with_anthropic(system_prompt, transcription, settings)


def _generate_with_openai(system_prompt: str, transcription: str, settings: Settings) -> EstimationResult:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcription},
        ],
    )
    estimation_text = response.choices[0].message.content or ""
    return EstimationResult(estimation=estimation_text, model=settings.openai_model, provider="openai")


def _generate_with_anthropic(system_prompt: str, transcription: str, settings: Settings) -> EstimationResult:
    import anthropic

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    response = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": transcription}],
    )
    estimation_text = "".join(block.text for block in response.content if block.type == "text")
    return EstimationResult(estimation=estimation_text, model=settings.anthropic_model, provider="anthropic")
