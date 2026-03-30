# Blacklist Microservice

Microservicio REST para gestionar la lista negra global de emails de la organización. Permite agregar emails a la lista negra y consultar si un email está bloqueado.

## Stack tecnológico

- Python 3.13
- Flask 3.1 + Flask-RESTful
- Flask-SQLAlchemy + PostgreSQL
- Flask-Marshmallow
- Gunicorn

## Endpoints

### `POST /blacklists`
Agrega un email a la lista negra global.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "blocked_reason": "Motivo opcional (máx 255 caracteres)"
}
```

**Respuestas:**
- `201` — Email agregado exitosamente
- `400` — Faltan campos requeridos
- `401` — Token ausente o inválido
- `409` — El email ya está en la lista negra para esa app

---

### `GET /blacklists/<email>`
Consulta si un email está en la lista negra global.

**Headers:**
```
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
  "is_blacklisted": true,
  "blocked_reason": "Motivo por el que fue bloqueado"
}
```

---

### `GET /`
Health check del servicio.

**Respuesta:**
```json
{ "status": "ok" }
```

## Variables de entorno

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DATABASE_URL` | URL de conexión a PostgreSQL | `postgresql://user:pass@host/db` |
| `JWT_SECRET_KEY` | Token estático de autorización | `mi-token-secreto` |

Copia `.env.example` a `.env` y completa los valores antes de ejecutar.

## Ejecución local

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Despliegue

La aplicación está configurada para desplegarse en **AWS Elastic Beanstalk** usando `gunicorn` como servidor WSGI. El archivo `application.py` y el `Procfile` están listos para el despliegue en EB.
