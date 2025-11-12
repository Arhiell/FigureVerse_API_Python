# FigureVerse Analytics API (Django + Firebase)

API de analytics y asistencia de IA construida con Django y conectada directamente a Firebase (Firestore). No usa base de datos local ni Docker; Firebase es la única fuente de verdad.

## Objetivos
- Leer y escribir métricas en Firestore (`/analytics`, `/product_stats`).
- Procesar eventos (`/events`) para recalcular overview y ventas por producto.
- Analizar comentarios con Gemini y publicar insights en `/ai_insights`.
- Exponer endpoints REST bajo `/v1/` para overview, top productos, recálculo y análisis de comentarios.

## Colecciones Firebase
- `/events`: eventos fuente (ventas, catálogo, etc.).
- `/analytics/overview`: documento con métricas agregadas del negocio.
- `/product_stats/{product_id}`: métricas agregadas por producto (ventas, etc.).
- `/comments`: comentarios de usuarios.
- `/ai_insights`: resultados de análisis de IA (sentimiento, toxicidad, explicación).

## Estructura relevante
- `social/services/firebase_client.py`: cliente Firestore (lectura/escritura y agregador desde `/events`).
- `social/services/gemini_client.py`: cliente Gemini (análisis y preguntas libres).
- `social/services/analytics_service.py`: lectura de overview/top y recálculo/publicación.
- `social/tasks/sync_events.py`: procesamiento de eventos y publicación en Firestore.
- `social/views/*`: vistas DRF que exponen los endpoints.
- `core/settings.py`: configuración (DRF, claves, credenciales Google).

## Endpoints (prefijo `/v1/`)
- `GET /v1/firebase/test`: prueba de conexión a Firestore.
- `GET /v1/analytics/overview`: devuelve el documento `/analytics/overview`.
- `GET /v1/analytics/top-products`: top desde `/product_stats` (ordenado por `sales_total`).
- `POST /v1/analytics/recalculate`: recalcula overview y `product_stats` a partir de `/events`.
- `POST /v1/comments/analyze`: guarda comentario, analiza con Gemini y publica insight.
- `POST /v1/comments/{product_id}/analysis`: analiza texto libre para un producto.
- `POST /v1/admin/questions`: preguntas libres al modelo Gemini.

## Dependencias
Listado en `requirements.txt`:
- `django` y `djangorestframework`.
- `firebase-admin` y `google-cloud-firestore`.
- `google-generativeai` (Gemini).
- `django-environ`, `requests`, `gunicorn`.

## Variables de entorno (.env)
Tomar `.env.example` y completar:
- `DJANGO_SECRET_KEY`: clave de Django.
- `DEBUG`: `True/False`.
- `ALLOWED_HOSTS`: lista separada por comas.
- `GOOGLE_APPLICATION_CREDENTIALS`: ruta absoluta al JSON de servicio (Windows usa `\\`).
- `FIREBASE_PROJECT_ID`: ID del proyecto Firebase (opcional, recomendable).
- `GEMINI_API_KEY`: clave de API para Google Generative AI.

Ejemplo (Windows):
```
DJANGO_SECRET_KEY=dev-secret
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
GOOGLE_APPLICATION_CREDENTIALS=C:\\Users\\tuusuario\\Desktop\\FigureVerse_API_Python\\figureverse.json
FIREBASE_PROJECT_ID=figureverse-xxxx
GEMINI_API_KEY=ya29....
```

## Instalación y arranque (local, sin Docker)
1) Crear y activar entorno virtual:
```
python -m venv .venv
.\.venv\Scripts\activate
```
2) Instalar dependencias:
```
pip install -r requirements.txt
```
3) Configurar `.env` y credenciales.
4) Levantar servidor:
```
python manage.py runserver 0.0.0.0:8000
```
Accede a `http://127.0.0.1:8000/`.

## Despliegue sin Docker
- Incluido `Procfile` para plataformas con buildpacks (Render/Railway/Heroku):
  - `web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT`
- Asegura `GOOGLE_APPLICATION_CREDENTIALS` en variables del servicio y sube el JSON de credenciales como Secret (no en el repo).

## Pruebas rápidas
- Script: `python test_firebase_connection.py` (verifica credenciales y lectura de `events`).
- Navegador:
  - `http://localhost:8000/v1/firebase/test`
  - `http://localhost:8000/v1/analytics/overview`
  - `http://localhost:8000/v1/analytics/top-products`
  - `http://localhost:8000/v1/analytics/recalculate` (POST)
  - `http://localhost:8000/v1/comments/analyze` (POST JSON: `{ product_id, text, rating? }`)
  - `http://localhost:8000/v1/admin/questions` (POST JSON: `{ question }`)

## Troubleshooting
- Falta `GEMINI_API_KEY`: el cliente lanzará un error descriptivo.
- `GOOGLE_APPLICATION_CREDENTIALS` inválido o ruta incorrecta: Firestore no inicializa.
- Windows: usar rutas con `\\` en `.env`.

## Seguridad y buenas prácticas
- No subir `.env` ni JSON de servicio. Usa `secrets/` local y `.gitignore`.
- Configurar dominios en `ALLOWED_HOSTS` para producción.