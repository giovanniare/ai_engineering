# Estimador CAG

Servicio FastAPI que recibe la transcripcion de una reunion y devuelve una estimacion de
software generada por un LLM (OpenAI o Anthropic), usando arquitectura **CAG**
(Context-Augmented Generation): todo el contexto de referencia (ejemplos de estimaciones
previas) viaja directamente en el prompt de cada llamada. No hay base de datos, retrieval
ni persistencia.

## Arquitectura

```
app/
├── main.py              # App FastAPI, monta routers y /health
├── config.py            # Configuracion via variables de entorno (pydantic-settings)
├── routers/
│   └── estimations.py   # POST /api/v1/estimate
├── services/
│   └── llm_service.py   # Construccion del prompt + llamada a OpenAI/Anthropic
└── context/
    └── examples.py      # Ejemplos de estimaciones previas (contexto estatico CAG)
```

Flujo de una peticion:

```
[system]    -> instrucciones de rol + ejemplos de estimaciones previas (context/examples.py)
[user]      -> transcripcion de la reunion (request.transcription)
[assistant] -> estimacion generada por el LLM
```

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) como gestor de paquetes
- Una API key de OpenAI y/o Anthropic

## Instalacion

```bash
uv sync
```

## Configuracion

Copia `.env.example` a `.env` y rellena tus valores:

```bash
cp .env.example .env
```

| Variable            | Descripcion                                      |
|---------------------|---------------------------------------------------|
| `LLM_PROVIDER`       | `openai` o `anthropic`                            |
| `OPENAI_API_KEY`     | API key de OpenAI (si usas ese proveedor)         |
| `OPENAI_MODEL`       | Modelo de OpenAI, por defecto `gpt-4o-mini`       |
| `ANTHROPIC_API_KEY`  | API key de Anthropic (si usas ese proveedor)      |
| `ANTHROPIC_MODEL`    | Modelo de Anthropic, por defecto `claude-haiku-4-5` |
| `APP_ENV`            | Entorno de la app (`development`, `production`, ...) |

El `.env` nunca se sube al repositorio (esta en `.gitignore`).

## Arrancar el servidor

```bash
uv run uvicorn app.main:app --reload
```

- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Probar el endpoint

```bash
curl -X POST http://localhost:8000/api/v1/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "transcription": "En la reunion con el equipo de marketing, el cliente explico que necesita una landing page con formulario de contacto, integracion con su CRM actual (HubSpot), y una seccion de blog con editor WYSIWYG. El plazo ideal seria tenerlo listo en 4 semanas. El diseno ya existe en Figma."
  }'
```

Respuesta esperada:

```json
{
  "estimation": "## Estimacion: ...",
  "model": "claude-haiku-4-5",
  "provider": "anthropic"
}
```

Una transcripcion de ejemplo lista para usar esta en
[`docs/transcripcion_ejemplo.md`](docs/transcripcion_ejemplo.md).

## Validacion automatica

El proyecto incluye una suite de tests que valida:

1. **Estructura de carpetas** (`tests/test_structure.py`): que existan los archivos
   requeridos, que `.env` este en `.gitignore` y que haya al menos dos ejemplos de
   contexto CAG.
2. **Funcionamiento del servicio** (`tests/test_api.py`): que `/health` responda 200, que
   `/docs` este disponible, y que `/api/v1/estimate` devuelva la estimacion (el LLM se
   mockea para no depender de API keys reales ni gastar creditos en CI).

Ejecutar localmente:

```bash
uv run pytest -v
```

Este pipeline corre automaticamente en cada push/PR via GitHub Actions
(`.github/workflows/ci.yml`), que ademas levanta el servidor real con `uvicorn` y
verifica que `/health` responde, como smoke test de arranque.

## Checklist de verificacion

- [x] El proyecto arranca sin errores con `uv run uvicorn app.main:app --reload`
- [x] Las API keys se cargan desde `.env` y nunca aparecen en el codigo
- [x] `GET /health` responde con status 200
- [x] `POST /api/v1/estimate` recibe una transcripcion y devuelve una estimacion
- [x] La estimacion generada se inspira en los ejemplos de contexto inyectados
- [x] La documentacion Swagger esta accesible en `/docs`
- [x] `.env` esta en `.gitignore`
