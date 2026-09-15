from fastapi import FastAPI

from app.routers import estimations

app = FastAPI(
    title="Estimador CAG",
    description=(
        "Servicio que genera estimaciones de software a partir de transcripciones "
        "de reuniones, usando arquitectura CAG (contexto estatico inyectado en el prompt)."
    ),
    version="0.1.0",
)

app.include_router(estimations.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
