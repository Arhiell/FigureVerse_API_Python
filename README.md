# 🧠 FigureVerse API (Python / Django)

> API de reseñas con integración a Firebase y consumo de Cloud Functions. Proyecto listo para trabajo en equipo, con dependencias definidas, variables de entorno y archivos sensibles excluidos del repositorio.

## Visión General

- Framework: `Django` + `Django REST Framework`.
- Integraciones: `Firebase Admin` (Firestore) y `Cloud Functions` vía `requests`.
- App principal: `feedback` expone endpoints para productos y reseñas.

## Estructura del Proyecto

- `aiReviewsApi/ai_reviews_api/` configuración de Django y Firebase.
- `aiReviewsApi/feedback/` vistas de API y cliente a Cloud Functions.
- `requirements.txt` dependencias con rangos estables.
- `.gitignore` excluye credenciales y archivos generados.

## Dependencias

Instalar con:

```bash
pip install -r requirements.txt
```

Incluye:

- `Django` (>=5.2,<5.3)
- `djangorestframework` (>=3.14,<3.16)
- `firebase-admin` (>=6.3,<7)
- `requests` (>=2.31,<3)
- `google-generativeai` (>=0.6,<0.8)
- `certifi` (CA bundle para HTTPS estable)

## Variables de Entorno

Se cargan automáticamente desde `.env` si existe (ver `.env.example`). Puedes exportarlas manualmente si prefieres.

- `DJANGO_SECRET_KEY` clave secreta de Django.
- `DJANGO_DEBUG` `True` o `False`.
- `DJANGO_ALLOWED_HOSTS` lista separada por comas (ej. `localhost,127.0.0.1`).
- `CLOUD_FUNCTIONS_BASE_URL` base principal (Cloud Run/Functions/Emulador).
- `CLOUD_FUNCTIONS_FALLBACK_BASE_URL` base de respaldo (opcional; por defecto Cloud Functions).
- `CLOUD_FUNCTIONS_FUNCTION_NAME` nombre de la función (por defecto `api`).
- `CLOUD_FUNCTIONS_VERIFY_TLS` `True`/`False` para verificación TLS (usa `certifi` cuando es `True`).
- `CLOUD_FUNCTIONS_EMULATOR_BASE_URL` base del emulador (`http://localhost:5001/figureverse-9b12e/us-central1/api`).
- `GOOGLE_APPLICATION_CREDENTIALS` / `FIREBASE_CREDENTIALS_PATH` ruta al `serviceAccountKey.json`.
- `FIREBASE_PROJECT_ID` id del proyecto Firebase.

Notas:

- En desarrollo (`DEBUG=True`) la base por defecto apunta al emulador.
- En producción la base por defecto apunta a Cloud Run, con fallback a Cloud Functions.

## Seguridad y Archivos Sensibles

- `.gitignore` bloquea `**/serviceAccountKey*.json`, `.env`, llaves (`*.pem`, `*.key`) y artefactos.
- Nunca subas `serviceAccountKey.json` ni secretos al repositorio.
- Usa `FIREBASE_CREDENTIALS` en producción para apuntar al JSON fuera del código.

## Ejecución

1. Copia `.env.example` a `.env` y ajusta las variables (Cloud Run/Functions/Emulador).

2. Migraciones iniciales (si aplica):

```bash
python manage.py migrate
```

3. Servidor de desarrollo:

```bash
python manage.py runserver
```

API base: `http://localhost:8000/api/`

## Endpoints

- `GET /api/productos/` listado de productos.
- `GET /api/resenas/` listado de reseñas.
- `GET /api/resenas/producto/<product_id>/` reseñas por producto.

Implementación y consumo:

- Vistas en `aiReviewsApi/feedback/views_data.py`.
- Cliente HTTP en `aiReviewsApi/feedback/services/cloud_functions_client.py`.
- Rutas remotas:
  - Cloud Run: `https://api-pcjssvdena-uc.a.run.app/api/...`
  - Cloud Functions: `https://us-central1-figureverse-9b12e.cloudfunctions.net/api/api/...` (doble `api` por nombre de función + prefijo interno)
  - Emulador: `http://localhost:5001/figureverse-9b12e/us-central1/api/api/...`

## Firebase

- Se inicializa con `firebase_admin` y un `serviceAccountKey.json`.
- Configuración en `aiReviewsApi/ai_reviews_api/settings.py`.
- En producción, usa `FIREBASE_CREDENTIALS` para la ruta del JSON.

## Notas de Configuración

- `settings.py` carga secretos desde variables de entorno y corrige el orden de `BASE_DIR`.
- La base de datos por defecto es SQLite (`db.sqlite3`), ignorada por `.gitignore`.

## Icono

- Proyecto identificado con 🧠 en el título.
- Puedes reemplazarlo por un logo propio enlazado vía URL externa si lo deseas.

## Trabajo en Equipo

- Tu compañero solo necesita:
  - Clonar el repo.
  - Crear/ubicar `serviceAccountKey.json` localmente o definir `FIREBASE_CREDENTIALS`.
  - Exportar variables de entorno indicadas.
  - Instalar dependencias con `pip install -r requirements.txt`.
  - Ejecutar `python manage.py runserver`.

## Licencia

- Define la licencia que aplique a tu proyecto.
