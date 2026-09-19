# Transcripcion de ejemplo

Usa el siguiente texto como valor del campo `transcription` al probar el endpoint
`POST /api/v1/estimate` (via curl, Postman o Swagger UI en `/docs`).

## Reunion: Landing page + blog para equipo de marketing

> En la reunion con el equipo de marketing, el cliente explico que necesita una landing
> page con formulario de contacto, integracion con su CRM actual (HubSpot), y una seccion
> de blog con editor WYSIWYG. El plazo ideal seria tenerlo listo en 4 semanas. El diseno
> ya existe en Figma.

### Uso con curl

```bash
curl -X POST http://localhost:8000/api/v1/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "transcription": "En la reunion con el equipo de marketing, el cliente explico que necesita una landing page con formulario de contacto, integracion con su CRM actual (HubSpot), y una seccion de blog con editor WYSIWYG. El plazo ideal seria tenerlo listo en 4 semanas. El diseno ya existe en Figma."
  }'
```

### Otra transcripcion de prueba (proyecto mas grande)

> El cliente de retail nos comento que quiere migrar su tienda online actual (construida
> en una plataforma no-code) a una solucion a medida. Necesitan catalogo de productos con
> variantes (talla, color), carrito de compras, pasarela de pago (Stripe), gestion de
> pedidos para el equipo de logistica, y un panel de administracion. Tienen unos 500
> productos actualmente. El equipo interno puede encargarse del contenido, pero necesitan
> que nosotros migremos los datos desde la plataforma actual. Sin fecha limite estricta,
> pero preferirian tenerlo para la campana de fin de ano.

Esta segunda transcripcion es util para observar como el modelo ajusta el desglose de
tareas cuando el alcance es mayor (migracion de datos, pasarela de pago, panel de admin).
