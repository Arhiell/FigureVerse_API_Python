# 🧠 FigureVerse API — Documentación Profesional

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/) [![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/) [![DRF](https://img.shields.io/badge/DRF-3.14%2B-ff3c2e)](https://www.django-rest-framework.org/) [![Firebase](https://img.shields.io/badge/Firebase-Admin-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com/) [![Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)

API para análisis de reseñas con integración a Firebase (Firestore), consumo de Google Cloud Functions y generación de resúmenes automáticos con Gemini.

## Cuentas de los repositorios de Git

- 🌐 Figure Verse — Página Web de Productos
  - URL: `https://github.com/Arhiell/FigureVerse_Web.git`
  - Enfoque en cliente: catálogos, compras, etc.

- 🖥️ Figure Verse — Aplicación de Escritorio
  - URL: `https://github.com/BautiC-9/FigureVerse-Escritorio.git`
  - Apartado de administradores para la gestión de la tienda.

- ⚙️ API desarrollada en Node
  - URL: `https://github.com/Arhiell/FigureVerse-API.git`
  - Núcleo de gestión y peticiones del ecosistema (web y escritorio).

- 🐍 API en Django (este repositorio)
  - URL: `https://github.com/Arhiell/FigureVerse_API_Python.git`
  - Integra Cloud Functions y Gemini para análisis de reseñas.

Así se sincroniza completamente todo el proyecto entre sí.

## Resumen

- Framework: `Django` + `Django REST Framework`.
- Integraciones: `Firebase Admin` (Firestore), `Cloud Functions` vía `requests`, `Google Generative AI (Gemini)`.
- App principal: `feedback` expone endpoints de datos, análisis, runs, historial y comentarios.

## Requisitos

- Python `3.10+` (requerido por Django 5.x).
- `pip` y `virtualenv`.
- Credenciales de Firebase (JSON de cuenta de servicio).
- Acceso a Cloud Functions/Cloud Run (URLs y opcional token `Bearer`).

## Instalación

```bash
python -m venv venv
./venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

## Configuración

Variables de entorno (ver `.env.example`):

| Variable | Descripción |
|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta de Django |
| `DJANGO_DEBUG` | `True` en desarrollo, `False` en producción |
| `DJANGO_ALLOWED_HOSTS` | Lista de hosts permitidos (coma) |
| `GEMINI_API_KEY` | API Key de Google Gemini |
| `GOOGLE_APPLICATION_CREDENTIALS` | Ruta al JSON de la cuenta de servicio |
| `FIREBASE_CREDENTIALS_PATH` | Alternativa a la ruta de credenciales |
| `FIREBASE_PROJECT_ID` | ID del proyecto en Firebase |
| `CLOUD_FUNCTIONS_BASE_URL` | URL principal de Cloud Functions / Cloud Run |
| `CLOUD_FUNCTIONS_FALLBACK_BASE_URL` | URL de respaldo |
| `CLOUD_FUNCTIONS_EMULATOR_BASE_URL` | URL del emulador en desarrollo |
| `CLOUD_FUNCTIONS_FUNCTION_NAME` | Nombre de la función (prefijo de ruta) |
| `CLOUD_FUNCTIONS_VERIFY_TLS` | Verificación TLS (`True`/`False`) |
| `CLOUD_FUNCTIONS_TIMEOUT` | Timeout en segundos |
| `CLOUD_FUNCTIONS_AUTH_TOKEN` | Token Bearer opcional |

Referencias en código: `aiReviewsApi/ai_reviews_api/settings.py:49–66`.

## Ejecución

```bash
cd aiReviewsApi
python manage.py runserver 0.0.0.0:8000
```

- Base de la API: `http://localhost:8000/api/`
- Ruteo: `aiReviewsApi/ai_reviews_api/urls.py:6` incluye `feedback.urls`.

## Dependencias y herramientas

Archivo `requirements.txt` con iconos, versiones, uso y ubicación en código:

| Icono | Paquete | Versión | Uso | Ubicación en código |
|---|---|---|---|---|
| 🧩 | `Django` | `>=5.2,<5.3` | Framework web | `aiReviewsApi/ai_reviews_api/settings.py:70`, `aiReviewsApi/ai_reviews_api/urls.py:6`, `aiReviewsApi/manage.py:1` |
| 🔗 | `djangorestframework` | `>=3.14,<3.16` | REST API | `aiReviewsApi/feedback/views_analysis.py:1` |
| 🔥 | `firebase-admin` | `>=6.3,<7` | Firestore (persistencia) | `aiReviewsApi/ai_reviews_api/settings.py:31`, `aiReviewsApi/feedback/services/firebase_client.py:1` |
| 🌐 | `requests` | `>=2.31,<3` | HTTP hacia Cloud Functions/Run | `aiReviewsApi/feedback/services/cloud_functions_client.py:1` |
| ✨ | `google-generativeai` | `==0.7.2` | Cliente de Gemini | `aiReviewsApi/feedback/services/gemini_client.py:1` |
| 🔒 | `certifi` | `>=2024.7,<2026` | CA bundle para TLS | `aiReviewsApi/feedback/services/cloud_functions_client.py:1` |

Herramientas externas:

- Firebase Firestore: `aiReviewsApi/ai_reviews_api/settings.py:22–37` inicializa cliente si existen credenciales.
- Cloud Functions/Run: `feedback/services/cloud_functions_client.py:1–73` gestiona URLs, TLS y fallback.
- Gemini: `feedback/services/gemini_client.py:1–20` configura API key y modelo.

## Endpoints detallados

Base: `http://localhost:8000/api/` (ver `feedback/urls.py:12–64`).

Resumen en tabla con iconos:

| Icono | Método | Ruta | Descripción |
|---|---|---|---|
| 📦 | GET | `/api/productos/` | Lista productos |
| 📝 | GET | `/api/resenas/` | Lista reseñas |
| 🔍 | GET | `/api/resenas/producto/<id>/` | Reseñas por producto |
| 🧠 | POST | `/api/analisis/productos/malas-calificaciones/` | Ejecuta análisis por umbral |
| 🗂 | GET | `/api/analisis/productos/<id>/resumen/` | Último análisis de un producto |
| 📊 | GET | `/api/analisis/productos/resumenes/` | Listado de análisis paginado |
| ⏱️ | GET | `/api/analisis/runs/` | Corridas del análisis |
| 🕓 | GET | `/api/analisis/productos/<id>/historial/` | Historial por producto |
| 💬 | GET | `/api/comentarios/producto/<id>/` | Comentarios con filtros |
| 🔄 | POST | `/api/comentarios/producto/<id>/sync/` | Sincroniza comentarios |

Datos (Cloud Functions):

- `GET /api/productos/` — Lista productos.
- `GET /api/resenas/` — Lista reseñas.
- `GET /api/resenas/producto/<id>/` — Reseñas por producto.

Análisis (Gemini + Firebase):

- `POST /api/analisis/productos/malas-calificaciones/`
  - Body opcional: `{ "rating_threshold": 3 }`
  - Respuesta `200`:
    ```json
    {
      "rating_threshold": 3,
      "analyzed_products": ["Producto A", "Producto B"],
      "analyzed_count": 2,
      "total_products": 10,
      "summaries": [
        {"product_id": 1, "product_name": "Producto A", "summary": "..."}
      ]
    }
    ```

- `GET /api/analisis/productos/<id>/resumen/`
  - Respuesta `200`: análisis guardado con campos como `product_name`, `summary`, `avg_rating`, `total_reviews`, `rating_threshold`, `low_rating_reviews_count`, `last_analyzed_at`, `product_id` (ver `firebase_client.py:38–70`).
  - `404` si no existe.

- `GET /api/analisis/productos/resumenes/`
  - Query: `page`, `page_size`, `product_name`/`q`.
  - Respuesta `200`:
    ```json
    {
      "count": 12,
      "page": 1,
      "page_size": 10,
      "results": [ { "product_id": "1", "product_name": "...", "summary": "...", "last_analyzed_at": "..." } ]
    }
    ```

- `GET /api/analisis/runs/`
  - Respuesta `200`: `{ "count": N, "results": [{ "id": "...", "rating_threshold": 3, "analyzed_products": [...], "created_at": "..." }] }`.

- `GET /api/analisis/productos/<id>/historial/`
  - Respuesta `200`: `{ "count": N, "results": [{ "id": "...", "created_at": "...", ... }] }`.

Comentarios (Firestore):

- `GET /api/comentarios/producto/<id>/`
  - Query: `page`, `page_size`, `q`, `from`, `to`.
  - Respuesta `200`:
    ```json
    { "count": 5, "page": 1, "page_size": 20, "results": [ { "id": "...", "comment": "...", "created_at": "..." } ] }
    ```

- `POST /api/comentarios/producto/<id>/sync/`
  - Respuesta `200`: `{ "product_id": 1, "saved": 25 }`.

## Paginación y filtros

- Paginación: `page` (por defecto 1), `page_size` (por defecto 20; mínimo 1).
- Filtro por nombre de producto: `product_name`/`q` en resúmenes.
- Filtro de comentarios: `q` (texto), `from`/`to` (ISO 8601).

## Errores y códigos de estado

- `400` — `rating_threshold` inválido (`views_analysis.py:34–46`).
- `404` — No hay análisis guardado para el producto (`views_analysis.py:68–73`).
- `502` — Error consumiendo Cloud Functions (`views_analysis.py:50–54`, `108–113`).
- `200` — Éxito con payload correspondiente.

## Arquitectura y flujo

- `analysis_service.py:13–136`:
  - Lee productos y reseñas desde Cloud Functions.
  - Agrupa reseñas por producto y calcula métricas.
  - Llama a Gemini para generar un resumen de reseñas con baja calificación.
  - Persiste resultados en Firestore (`product_analysis`, `product_analysis_history`) y registra `analysis_runs`.

- Firebase: `firebase_client.py:1–239` (CRUD y consultas, ordenado por `created_at`/`last_analyzed_at`).
- Gemini: `gemini_client.py:1–111` (modelo `gemini-1.5-flash`, fallback local si no hay API key).
- Cloud Functions: `cloud_functions_client.py:1–73` (emulador, base, fallback, TLS, headers y tiempo de espera).

## Estructura del proyecto

- `aiReviewsApi/manage.py` — utilidades y servidor (`aiReviewsApi/manage.py:1–22`).
- `aiReviewsApi/ai_reviews_api/` — `settings.py`, `urls.py`, `asgi.py`, `wsgi.py`.
- `aiReviewsApi/feedback/` — app principal: servicios, vistas y rutas (`feedback/urls.py:12–64`).
- `requirements.txt` — dependencias.
- `.env.example` — plantilla de configuración.

## Seguridad

- No exponer secretos (`.env`, JSON de cuenta de servicio); ver `.gitignore` para exclusión (`.gitignore:12–30`).
- `CLOUD_FUNCTIONS_VERIFY_TLS`: habilitar verificación en producción.
- `DJANGO_ALLOWED_HOSTS`: configurar hosts válidos en despliegue.
- `CLOUD_FUNCTIONS_AUTH_TOKEN`: usar `Bearer` para proteger endpoints de origen si aplica.

## Despliegue y emulador

- Base en producción: `CLOUD_FUNCTIONS_BASE_URL` (por defecto `https://api-pcjssvdena-uc.a.run.app`).
- Fallback: `CLOUD_FUNCTIONS_FALLBACK_BASE_URL` (`https://us-central1-figureverse-9b12e.cloudfunctions.net/api`).
- Emulador local: `CLOUD_FUNCTIONS_EMULATOR_BASE_URL` (`http://localhost:5001/.../us-central1/api`).
- En `DEBUG=True` se prioriza el emulador si está definido.

## Ecosistema

- Web: `https://github.com/Arhiell/FigureVerse_Web.git`
- Escritorio: `https://github.com/BautiC-9/FigureVerse-Escritorio.git`
- API Node: `https://github.com/Arhiell/FigureVerse-API.git`
- API Django (este repo): `https://github.com/Arhiell/FigureVerse_API_Python.git`

## Autores y Universidad

- Universidad Tecnológica Nacional (UTN) – Facultad Regional Resistencia.
- Carrera: Técnico Universitario en Programación.
- Autores: Ayala, Ariel (`https://github.com/Arhiell`), Capovilla, Bautista (`https://github.com/BautiC-9`).
- Profesores: Python (Goya, Juan Manuel) — JavaScript (Puljiz, Emilio).

## Licencia

- Definir la licencia aplicable al proyecto.
