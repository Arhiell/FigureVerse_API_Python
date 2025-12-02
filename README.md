# 🧠 FigureVerse API — Django + DRF

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/) [![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/) [![DRF](https://img.shields.io/badge/DRF-3.14%2B-ff3c2e)](https://www.django-rest-framework.org/) [![Firebase](https://img.shields.io/badge/Firebase-Admin-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com/) [![Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)

API para análisis de reseñas con integración a Firebase (Firestore), consumo de Cloud Functions y resúmenes automáticos con Gemini. Enfoque en calidad, seguridad y trabajo en equipo.

## Índice

- [Resumen](#resumen)
- [Arquitectura](#arquitectura)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Endpoints](#endpoints)
- [Ejemplos (curl)](#ejemplos-curl)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Buenas prácticas](#buenas-prácticas)
- [Ecosistema](#ecosistema)
- [Autores](#autores)
- [Licencia](#licencia)

## Resumen

- Framework: `Django` + `Django REST Framework`.
- Integraciones: `Firebase Admin` (Firestore), `Cloud Functions` vía `requests`, `Google Generative AI (Gemini)`.
- App principal: `feedback` expone endpoints para datos, análisis, runs, historial y comentarios.

## Arquitectura

- Configuración: `aiReviewsApi/ai_reviews_api/settings.py` carga `.env`, inicializa Firestore y define URLs de Cloud Functions.
- Servicios:
  - `feedback/services/cloud_functions_client.py`: lectura de productos y reseñas desde Cloud Functions.
  - `feedback/services/firebase_client.py`: persistencia en Firestore (`product_analysis`, `product_analysis_history`, `analysis_runs`, `product_comments`).
  - `feedback/services/analysis_service.py`: análisis y generación de resúmenes.
  - `feedback/services/gemini_client.py`: llamada a Gemini y fallback local.
- Ruteo: `feedback/urls.py` mapea los endpoints bajo `api/`.

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
| `CLOUD_FUNCTIONS_FUNCTION_NAME` | Nombre de la función (prefijo) |
| `CLOUD_FUNCTIONS_VERIFY_TLS` | Verificación TLS (`True`/`False`) |
| `CLOUD_FUNCTIONS_TIMEOUT` | Timeout en segundos |
| `CLOUD_FUNCTIONS_AUTH_TOKEN` | Token Bearer opcional |

Notas:

- En `DEBUG=True` se prioriza el emulador si está definido; en producción se usa Cloud Run y fallback.
- No subir credenciales ni `.env`. Están excluidos por `.gitignore`.

## Ejecución

```bash
python manage.py runserver 0.0.0.0:8000
```

- Base: `http://localhost:8000/api/`

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/productos/` | Lista productos |
| GET | `/api/resenas/` | Lista todas las reseñas |
| GET | `/api/resenas/producto/<id>/` | Reseñas por producto |
| POST | `/api/analisis/productos/malas-calificaciones/` | Ejecuta análisis por umbral (`rating_threshold`) |
| GET | `/api/analisis/productos/<id>/resumen/` | Último análisis de un producto |
| GET | `/api/analisis/productos/resumenes/` | Listado de análisis con paginación y filtro por nombre |
| GET | `/api/analisis/runs/` | Corridas del análisis |
| GET | `/api/analisis/productos/<id>/historial/` | Historial de análisis por producto |
| GET | `/api/comentarios/producto/<id>/` | Comentarios (paginación, texto, rango de fechas) |
| POST | `/api/comentarios/producto/<id>/sync/` | Sincroniza comentarios desde Cloud Functions |

Parámetros comunes:

- `GET /api/analisis/productos/resumenes/`: `page`, `page_size`, `product_name`.
- `GET /api/comentarios/producto/<id>/`: `page`, `page_size`, `q` (texto), `from` (ISO), `to` (ISO).

## Ejemplos (curl)

```bash
# Ejecutar análisis
curl -X POST http://127.0.0.1:8000/api/analisis/productos/malas-calificaciones/ \
  -H "Content-Type: application/json" \
  -d "{\"rating_threshold\": 3}"

# Listar resúmenes (paginado y filtro)
curl "http://127.0.0.1:8000/api/analisis/productos/resumenes/?page=1&page_size=10&product_name=iphone"

# Sincronizar comentarios
curl -X POST http://127.0.0.1:8000/api/comentarios/producto/1/sync/

# Listar comentarios con filtros
curl "http://127.0.0.1:8000/api/comentarios/producto/1/?page=1&page_size=5&q=calidad&from=2025-12-01"
```

## Estructura del proyecto

- `aiReviewsApi/ai_reviews_api/`: `settings.py`, `urls.py`, configuración base.
- `aiReviewsApi/feedback/`: app principal (servicios, vistas y ruteo).
  - `services/`: Cloud Functions, Firebase, Gemini, análisis.
  - `views_analysis.py`: vistas para análisis, comentarios e historial.
  - `urls.py`: mapeo de rutas bajo `/api/`.
- `requirements.txt`: dependencias principales.
- `.env.example`: ejemplo de configuración por entorno.

## Buenas prácticas

- No exponer secretos ni credenciales.
- Mantener `requirements.txt` actualizado.
- Usar ramas feature y Pull Requests para cambios significativos.

## Ecosistema

- Web: `https://github.com/Arhiell/FigureVerse_Web.git`
- Escritorio: `https://github.com/BautiC-9/FigureVerse-Escritorio.git`
- API Node: `https://github.com/Arhiell/FigureVerse-API.git`
- API Django (este repo): `https://github.com/Arhiell/FigureVerse_API_Python.git`

## Autores

- Universidad Tecnológica Nacional (UTN) – FR Resistencia
- Carrera: Técnico Universitario en Programación

- Ayala, Ariel: `https://github.com/Arhiell`
- Capovilla, Bautista: `https://github.com/BautiC-9`

Profesores:

- Python: Goya, Juan Manuel
- JavaScript: Puljiz, Emilio

## Licencia

- Definir la licencia aplicable al proyecto.
