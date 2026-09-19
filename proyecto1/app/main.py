from fastapi import FastAPI

from app.routers import estimations

app = FastAPI(
    title="Estimador CAG",
    description=(
        "Servicio que recibe la transcripcion de una reunion y devuelve una estimacion "
        "de software generada por un LLM, usando arquitectura CAG (contexto estatico "
        "inyectado directamente en el prompt)."
    ),
    version="0.1.0",
)

app.include_router(estimations.router, prefix="/api/v1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
