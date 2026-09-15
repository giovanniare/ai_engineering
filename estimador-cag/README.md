# Estimador CAG

Proyecto 1 del programa de AI Engineering — Sesion 2.

Servicio FastAPI que recibe la transcripcion de una reunion y devuelve una
estimacion de software generada por un LLM (OpenAI o Anthropic), usando
arquitectura **CAG** (Context-Augmented Generation): el contexto de referencia
(ejemplos de estimaciones previas) viaja completo en cada prompt, sin base de
datos ni retrieval.

## Estructura del proyecto

```
estimador-cag/
├── app/
│   ├── main.py              # App FastAPI, router y /health
│   ├── config.py            # Configuracion via variables de entorno
│   ├── routers/
│   │   └── estimations.py   # POST /api/v1/estimate
│   ├── services/
│   │   └── llm_service.py   # Construccion del prompt + llamada al LLM
│   └── context/
│       └── examples.py      # Ejemplos few-shot inyectados en el prompt
├── tests/                   # Validacion de estructura y del servicio (pytest)
├── transcripts/
│   └── sample_meeting.txt   # Transcripcion de ejemplo para probar el endpoint
└── .github/workflows/ci.yml # Pipeline de validacion automatica
```

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- API key de OpenAI y/o Anthropic

## Configuracion

1. Copia `.env.example` a `.env` y completa tus valores:

```
LLM_PROVIDER=openai        # openai | anthropic
LLM_MODEL=gpt-4o-mini      # o claude-haiku-4-5 para anthropic
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
APP_ENV=development
LOG_LEVEL=info
```

2. Instala dependencias:

```bash
uv sync
```

## Ejecutar el servicio

```bash
uv run uvicorn app.main:app --reload
```

- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Probar el endpoint

Se incluye una transcripcion de ejemplo en [`transcripts/sample_meeting.txt`](transcripts/sample_meeting.txt)
para usar como parametro de prueba:

```bash
curl -X POST http://localhost:8000/api/v1/estimate \
  -H "Content-Type: application/json" \
  -d "{\"transcription\": \"$(cat transcripts/sample_meeting.txt)\"}"
```

Respuesta esperada:

```json
{
  "estimation": "## Estimacion: ...",
  "model": "gpt-4o-mini",
  "provider": "openai"
}
```

## Validacion automatica

El proyecto incluye una suite de pytest (`tests/`) que valida:

- Que la estructura de carpetas/archivos esperada exista.
- Que `.env` este en `.gitignore` y que `.env.example` no contenga claves reales.
- Que el servicio arranque y `/health` y `/docs` respondan.
- Que `POST /api/v1/estimate` funcione end-to-end (el LLM se sustituye por un
  stub para no depender de API keys en CI).

Ejecutar localmente:

```bash
uv run pytest -v
```

Esta misma suite corre automaticamente en cada push/PR via GitHub Actions
([`.github/workflows/ci.yml`](.github/workflows/ci.yml)).
