# 🧠 FigureVerse API (Python / Django)

API de reseñas y análisis con integración a Firebase (Firestore), consumo de Cloud Functions y generación de resúmenes con Gemini. Pensada para trabajo en equipo, con configuración por entorno y buenas prácticas de seguridad.

## Visión General

- Framework: `Django` + `Django REST Framework`.
- Integraciones: `Firebase Admin` (Firestore), `Cloud Functions` vía `requests`, `Google Generative AI (Gemini)`.
- App principal: `feedback` expone endpoints de datos, análisis, runs, historial y comentarios.

## Arquitectura

- Configuración: `aiReviewsApi/ai_reviews_api/settings.py` (carga `.env`, inicializa Firestore, define URLs de Cloud Functions).
- Servicios:
  - `aiReviewsApi/feedback/services/cloud_functions_client.py` consumo de productos y reseñas.
  - `aiReviewsApi/feedback/services/firebase_client.py` persistencia en Firestore (`product_analysis`, `product_analysis_history`, `analysis_runs`, `product_comments`).
  - `aiReviewsApi/feedback/services/analysis_service.py` lógica de análisis y resúmenes.
  - `aiReviewsApi/feedback/services/gemini_client.py` generación de resúmenes en una sola frase.
- Ruteo: `aiReviewsApi/feedback/urls.py` mapea los endpoints.

## Endpoints

- Datos (Cloud Functions):
  - `GET /api/productos/` lista productos (`aiReviewsApi/feedback/urls.py:12`).
  - `GET /api/resenas/` lista todas las reseñas (`aiReviewsApi/feedback/urls.py:16`).
  - `GET /api/resenas/producto/<id>/` reseñas por producto (`aiReviewsApi/feedback/urls.py:18–23`).

- Análisis (Gemini + Firebase):
  - `POST /api/analisis/productos/malas-calificaciones/` ejecuta análisis por umbral (`aiReviewsApi/feedback/urls.py:27–32`).
  - `GET /api/analisis/productos/<id>/resumen/` último análisis de un producto (`aiReviewsApi/feedback/urls.py:34–39`).
  - `GET /api/analisis/productos/resumenes/` listado de análisis, ordenado y paginado (`aiReviewsApi/feedback/urls.py:41–44`).
  - `GET /api/analisis/runs/` corridas del análisis (`aiReviewsApi/feedback/urls.py:46–49`).
  - `GET /api/analisis/productos/<id>/historial/` historial del producto (`aiReviewsApi/feedback/urls.py:51–54`).

- Comentarios (Firestore):
  - `POST /api/comentarios/producto/<id>/sync/` sincroniza comentarios desde Cloud Functions (`aiReviewsApi/feedback/urls.py:61–64`).
  - `GET /api/comentarios/producto/<id>/` lista comentarios con filtros y paginación (`aiReviewsApi/feedback/urls.py:56–59`).

### Parámetros de consulta

- `GET /api/analisis/productos/resumenes/`:
  - `page`, `page_size`, `product_name`.
- `GET /api/comentarios/producto/<id>/`:
  - `page`, `page_size`, `q` (texto), `from` (ISO), `to` (ISO).

## Colecciones en Firestore

- `product_analysis`: último análisis por producto (incluye `summary`, métricas y `last_analyzed_at`).
- `product_analysis_history`: documento por `product_id`; subcolección `runs` con entradas históricas.
- `analysis_runs`: una entrada por corrida con métricas agregadas y `created_at`.
- `product_comments`: documento por `product_id`; subcolección `comments` con cada comentario.

## Instalación

```bash
python -m venv venv
./venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

## Configuración

- Variables de entorno (ver `.env.example`):
  - `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`.
  - `GEMINI_API_KEY`.
  - `GOOGLE_APPLICATION_CREDENTIALS` o `FIREBASE_CREDENTIALS_PATH`.
  - `FIREBASE_PROJECT_ID`.
  - `CLOUD_FUNCTIONS_BASE_URL`, `CLOUD_FUNCTIONS_FALLBACK_BASE_URL`, `CLOUD_FUNCTIONS_EMULATOR_BASE_URL`, `CLOUD_FUNCTIONS_FUNCTION_NAME`, `CLOUD_FUNCTIONS_VERIFY_TLS`, `CLOUD_FUNCTIONS_TIMEOUT`.

Notas:

- En desarrollo (`DEBUG=True`) se usa el emulador si está definido; en producción, Cloud Run con fallback.
- No commitear credenciales ni `.env`. Los archivos sensibles están excluidos por `.gitignore`.

## Ejecución

```bash
python manage.py runserver 0.0.0.0:8000
```

Base: `http://localhost:8000/api/`

## Pruebas rápidas (curl)

- Ejecutar análisis: `curl -X POST http://127.0.0.1:8000/api/analisis/productos/malas-calificaciones/ -H "Content-Type: application/json" -d "{\"rating_threshold\": 3}"`
- Listar resúmenes: `curl "http://127.0.0.1:8000/api/analisis/productos/resumenes/?page=1&page_size=10&product_name=iphone"`
- Sincronizar comentarios: `curl -X POST http://127.0.0.1:8000/api/comentarios/producto/1/sync/`
- Listar comentarios: `curl "http://127.0.0.1:8000/api/comentarios/producto/1/?page=1&page_size=5&q=calidad&from=2025-12-01"`

## Buenas Prácticas

- No exponer secretos ni credenciales en el repositorio.
- Mantener `requirements.txt` actualizado y con rangos estables.
- Usar ramas feature y Pull Requests para cambios significativos.

## Ecosistema y Repositorios

- Figure Verse – Página Web de Productos
  - URL: `https://github.com/Arhiell/FigureVerse_Web.git`
  - Enfoque en cliente: catálogos, compras, etc.

- Figure Verse – Aplicación de Escritorio
  - URL: `https://github.com/BautiC-9/FigureVerse-Escritorio.git`
  - Apartado de administradores para la gestión de la tienda.

- API desarrollada en Node
  - URL: `https://github.com/Arhiell/FigureVerse-API.git`
  - Núcleo de gestión y peticiones del ecosistema (web y escritorio).

- API en Django (este repositorio)
  - URL: `https://github.com/Arhiell/FigureVerse_API_Python.git`
  - Integra Cloud Functions y Gemini para análisis de reseñas.

## Autores y Universidad

- Universidad Tecnológica Nacional (UTN) – Facultad Regional Resistencia
- Carrera: Técnico Universitario en Programación

- Autores:
  - Ayala, Ariel: `https://github.com/Arhiell`
  - Capovilla, Bautista: `https://github.com/BautiC-9`

- Profesores de la cátedra:
  - Python: Goya, Juan Manuel
  - JavaScript: Puljiz, Emilio

## Licencia

- Definir la licencia aplicable al proyecto.
