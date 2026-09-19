"""Ejemplos de estimaciones previas: el contexto estatico que se inyecta en cada prompt (CAG)."""

ESTIMATION_EXAMPLES = [
    {
        "meeting_summary": (
            "El cliente necesita una plataforma web de gestion de inventario para su "
            "almacen central. Debe permitir dar de alta productos, controlar stock en "
            "tiempo real, generar alertas de reposicion y mostrar un dashboard con "
            "metricas de rotacion. Se requiere control de acceso por roles (almacenista, "
            "supervisor, administrador). El plazo deseado es de 2 meses."
        ),
        "estimation": """
## Estimacion: Plataforma de Gestion de Inventario

### Desglose de tareas:
1. Diseno UI/UX: 40 horas
2. Backend API (CRUD inventario): 60 horas
3. Autenticacion y roles: 20 horas
4. Sistema de alertas de reposicion: 15 horas
5. Dashboard con metricas: 30 horas
6. Testing y QA: 25 horas

**Total estimado: 190 horas**
**Equipo recomendado: 2 desarrolladores full-stack + 1 disenador UX (part-time)**
**Duracion estimada: 6-8 semanas**
""",
    },
    {
        "meeting_summary": (
            "En la reunion con el equipo comercial, el cliente pidio una aplicacion movil "
            "(iOS y Android) para gestionar pedidos de sus repartidores. Necesita "
            "geolocalizacion en tiempo real, notificaciones push cuando cambia el estado "
            "de un pedido, y sincronizacion con su sistema ERP existente via API REST. "
            "El presupuesto es limitado, por lo que se plantea usar un framework "
            "multiplataforma (React Native o Flutter)."
        ),
        "estimation": """
## Estimacion: App Movil de Gestion de Pedidos

### Desglose de tareas:
1. Diseno UI/UX (mobile-first): 35 horas
2. Setup del proyecto multiplataforma: 10 horas
3. Modulo de geolocalizacion en tiempo real: 30 horas
4. Notificaciones push: 20 horas
5. Integracion con API REST del ERP: 40 horas
6. Autenticacion de repartidores: 15 horas
7. Testing en dispositivos iOS/Android: 30 horas

**Total estimado: 180 horas**
**Equipo recomendado: 2 desarrolladores mobile + 1 disenador UX (part-time)**
**Duracion estimada: 6-7 semanas**
""",
    },
]
