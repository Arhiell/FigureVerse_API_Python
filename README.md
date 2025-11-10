# 🔗 FigureVerse — API Django de Integración, Social y Analítica

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&labelColor=222)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&labelColor=222)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.x-EF3B2D?logo=django)](https://www.django-rest-framework.org/)
[![Firebase](https://img.shields.io/badge/Firebase-Admin-FFCA28?logo=firebase&labelColor=222)](https://firebase.google.com/)
[![Status](https://img.shields.io/badge/Estado-En%20Integración-2CA5E0)](#)

Proyecto Django/DRF que sincroniza con el core en Node.js mediante eventos publicados en Firestore (Firebase), expone endpoints sociales (comentarios y calificaciones) y provee analítica de negocio. La integración es desacoplada: no se comparte base de datos; se sincroniza por contrato JSON v1 y un endpoint interno seguro con HMAC.

---

## 🎯 Objetivos

- Exponer endpoints públicos para comentarios y calificaciones por producto.
- Procesar eventos de negocio generados por la API Node (órdenes, pagos, etc.).
- Convertir eventos en datos analíticos útiles (top de productos, overview, métricas).
- Mantener arquitectura desacoplada, escalable y segura.

## 🧩 Arquitectura general

- Integración: `Node → Firebase (Firestore) → Cloud Function → Django`.
- Seguridad: Cloud Function firma el cuerpo con `HMAC-SHA256` y Django valida en `POST /internal/events`.
- Patrón interno: `View → Controller → Service → Model`.
  - View: validaciones HTTP, auth, parseo básico.
  - Controller: mapeo de tipo de evento a handlers (sin lógica pesada).
  - Service: lógica de negocio; actualización de cachés y agregados analíticos.
  - Model: persistencia opcional para agregados analíticos.
- Comunicación con Node: `repositories`/`services` realizan requests HTTP a la API Node (productos, órdenes, etc.).

## 🧠 Patrones y diseño

- Separación de capas (Views/Controllers/Services/Models).
- Contratos tipados con `pydantic` para el envelope y payloads de eventos.
- Repositorio/Cliente HTTP para integración con Node.
- Caché en memoria para productos (`ProductCacheService`) con invalidación por eventos `ProductUpdated`.
- HMAC aplicado sobre los bytes del cuerpo para integridad del mensaje.
- JWT (pendiente) para identidad compartida entre APIs sin compartir DB.

---

## 📂 Estructura del proyecto y rol de cada archivo

```
c:\Users\ariel\Desktop\FigureVerse_API_Python
├── .env.example                      # Variables de entorno de referencia
├── .gitignore                        # Ignora archivos de entorno/compilación
├── README.md                         # Esta guía completa
├── config\
│   ├── __init__.py                   # Init del paquete Django
│   ├── asgi.py                       # Runner ASGI
│   ├── settings.py                   # Configuración de Django + .env
│   ├── urls.py                       # Enrutamiento global (v1 e internal)
│   └── wsgi.py                       # Runner WSGI
├── manage.py                         # Entrypoint de comandos Django
├── requirements.txt                  # Dependencias y versiones
└── social\
    ├── __init__.py                   # Init del app Django
    ├── admin.py                      # Registro en admin (si aplica)
    ├── apps.py                       # Configuración del app
    ├── auth\
    │   ├── __init__.py
    │   └── node_jwt.py               # (Pendiente) Validación de JWT de Node
    ├── controllers\
    │   ├── __init__.py
    │   └── event_controller.py       # Despacha eventos a servicios internos
    ├── events\
    │   ├── __init__.py               # Export de contratos/eventos
    │   ├── contract_v1.py            # Envelope y modelos Pydantic de eventos
    │   └── schemas.py                # Esquemas adicionales/histórico
    ├── migrations\
    │   ├── 0001_initial.py           # Migración inicial
    │   ├── 0002_rating.py            # Migración de ratings
    │   └── __init__.py
    ├── models\
    │   ├── __init__.py
    │   ├── analytics.py              # Modelo ProductAnalytics (agregados)
    │   ├── comment.py                # Modelo de comentarios
    │   └── rating.py                 # Modelo de calificaciones
    ├── repositories\
    │   ├── __init__.py
    │   ├── order_repository.py       # Requests a Node para órdenes
    │   └── product_repository.py     # Requests a Node para productos
    ├── serializers\
    │   ├── __init__.py
    │   ├── comment_serializer.py     # DRF serializer para comentarios
    │   └── rating_serializer.py      # DRF serializer para calificaciones
    ├── services\
    │   ├── __init__.py
    │   ├── analytics_service.py      # Top/Overview de analítica
    │   ├── comment_service.py        # Lógica de negocio de comentarios
    │   ├── event_processor_service.py# Handlers por tipo de evento
    │   ├── node_client.py            # Cliente HTTP hacia la API Node
    │   ├── product_cache.py          # Caché en memoria de productos
    │   └── rating_service.py         # Lógica de negocio de ratings
    ├── urls\
    │   ├── __init__.py
    │   ├── analytics.py              # Rutas /v1/analytics
    │   ├── comments.py               # Rutas /v1/products/<id>/comments
    │   ├── internal.py               # Rutas /internal/events
    │   └── ratings.py                # Rutas /v1/products/<id>/ratings
    ├── utils\
    │   └── hmac.py                   # Verificación HMAC-SHA256
    └── views\
        ├── __init__.py
        ├── analytics_view.py         # Vista GET /v1/analytics
        ├── comment_view.py           # Vista GET/POST comentarios por producto
        ├── internal_events_view.py   # Vista POST /internal/events
        └── rating_view.py            # Vista GET/POST ratings por producto
```

### Descripción de responsabilidades

- `config/settings.py`: lee `.env` (e.g. `INTERNAL_EVENTS_SECRET`, `NODE_API_BASE_URL`, `DEBUG`) y configura Django.
- `config/urls.py`: define prefijos `v1/products/`, `v1/analytics/` y `internal/` incluyendo los URLConfs del app `social`.
- `social/views/*`: capa HTTP de DRF (permisos, validaciones, parseo de parámetros, respuestas JSON).
- `social/controllers/event_controller.py`: despacha por `EventType` hacia `EventProcessorService`.
- `social/services/event_processor_service.py`: implementa lógica de negocio por evento (ventas, ingresos, caché, etc.).
- `social/models/analytics.py`: `ProductAnalytics` guarda agregados por producto (ventas e ingresos acumulados). Requiere migración.
- `social/services/analytics_service.py`: expone rankings (top) y overview.
- `social/services/product_cache.py`: cachea metadatos de productos; invalida ante `ProductUpdated`.
- `social/services/node_client.py` y `social/repositories/*`: integración HTTP hacia Node (productos/órdenes).
- `social/utils/hmac.py`: verificación de firmas HMAC-SHA256 en `/internal/events`.

---

## 🔌 Endpoints

- `GET /v1/analytics?type=top&range_days=30&limit=10`
  - Respuesta: ranking de productos (ingresos).

- `GET /v1/analytics?type=overview`
  - Respuesta: totales del negocio.

- `GET /v1/products/<id>/comments`
  - Permisos: `IsAuthenticated`.
  - Respuesta: comentarios aprobados del producto.

- `POST /v1/products/<id>/comments`
  - Permisos: `IsAuthenticated`.
  - Body: `{ content: string }`.
  - Comportamiento: valida en Node que el producto exista; crea comentario.

- `GET /v1/products/<id>/ratings`
  - Permisos: `IsAuthenticated`.
  - Respuesta: `{ promedio, cantidad }`.

- `POST /v1/products/<id>/ratings`
  - Permisos: `IsAuthenticated`.
  - Body: `{ score: number }`.

- `POST /internal/events`
  - Permisos: `AllowAny` (pero exige HMAC válido).
  - Header: `X-Internal-Events-Signature: sha256=<hex>`.
  - Body: Envelope JSON v1 (ver `social/events/contract_v1.py`).

---

## 📜 Contrato JSON v1 de eventos

Formato general del envelope (resumen):

```
{
  "event": "NombreDelEvento",
  "version": "v1",
  "timestamp": "2025-12-01T10:03:29.344Z",
  "origin": { "service": "node-core", "environment": "production", "ip": "x.x.x.x" },
  "payload": { /* datos específicos del evento */ }
}
```

Eventos contemplados:
- `UserAuthenticated`, `UserRegistered`
- `ProductCreated`, `ProductUpdated`
- `OrderCreated`, `PaymentApproved`, `InvoiceIssued`, `ShipmentCreated`, `DiscountApplied`
- `CompanySettingsUpdated`

Tipado y validación en `social/events/contract_v1.py` (Pydantic). El controlador y servicios consumen payloads ya validados.

---

## 🛡️ Seguridad

- HMAC-SHA256: Django verifica la firma sobre los bytes exactos del cuerpo en `POST /internal/events`.
- Secreto: `INTERNAL_EVENTS_SECRET` en `.env` y Cloud Function.
- JWT (pendiente): Validar tokens emitidos por Node (RS256/HS256), claims (`sub`, `exp`, `iss`).

---

## ⚙️ Configuración

Variables principales en `.env` (ver `.env.example`):
- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`.
- `NODE_API_BASE_URL`, `NODE_API_TIMEOUT`.
- `INTERNAL_EVENTS_SECRET`.
- (Opcional DB) `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.

Pasos rápidos:
- `pip install -r requirements.txt`
- `cp .env.example .env` y ajustar valores.
- `python manage.py migrate`
- `python manage.py runserver`

---

## 📦 Dependencias instaladas (resumen y versiones en requirements.txt)

Clave: `Django`, `djangorestframework`, `python-dotenv`, `firebase_admin`, `google-cloud-firestore`, `httpx`, `PyJWT`, `pydantic`.

Lista completa (requirements.txt):

```
annotated-types==0.7.0
anyio==4.10.0
asgiref==3.10.0
CacheControl==0.14.3
cachetools==5.5.2
certifi==2025.8.3
cffi==2.0.0
charset-normalizer==3.4.3
colorama==0.4.6
contourpy==1.3.3
cryptography==45.0.7
cycler==0.12.1
Django==5.2.8
djangorestframework==3.16.1
firebase_admin==7.1.0
fonttools==4.59.2
git-filter-repo==2.47.0
google-ai-generativelanguage==0.6.15
google-api-core==2.25.1
google-api-python-client==2.186.0
google-auth==2.40.3
google-auth-httplib2==0.2.1
google-cloud-core==2.4.3
google-cloud-firestore==2.21.0
google-cloud-storage==3.3.1
google-crc32c==1.7.1
google-generativeai==0.8.5
google-resumable-media==2.7.2
googleapis-common-protos==1.70.0
grpcio==1.74.0
grpcio-status==1.71.2
h11==0.16.0
h2==4.3.0
hpack==4.1.0
httpcore==1.0.9
httplib2==0.31.0
httpx==0.28.1
hyperframe==6.1.0
idna==3.10
kiwisolver==1.4.9
matplotlib==3.10.6
msgpack==1.1.1
numpy==2.3.2
packaging==25.0
pandas==2.3.2
pillow==11.3.0
proto-plus==1.26.1
protobuf==5.29.5
pyasn1==0.6.1
pyasn1_modules==0.4.2
pycparser==2.23
pydantic==2.12.4
pydantic_core==2.41.5
PyJWT==2.10.1
pyparsing==3.2.3
python-dateutil==2.9.0.post0
python-dotenv==1.2.1
pytz==2025.2
requests==2.32.5
rsa==4.9.1
six==1.17.0
sniffio==1.3.1
sqlparse==0.5.3
tqdm==4.67.1
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2025.2
uritemplate==4.2.0
urllib3==2.5.0
```

---

## 🔄 Flujo de eventos y procesamiento interno

1) Node publica en Firestore (`/events`).
2) Cloud Function observa, firma HMAC y reenvía a `POST /internal/events`.
3) Django valida firma y envelope v1; despacha por tipo de evento.
4) `EventProcessorService` actualiza caché/agregados y registra actividad.

Handlers actuales en `event_processor_service.py`:
- `on_order_created`: actualiza `ProductAnalytics` por ítems y total.
- `on_payment_approved`: registra ingresos confirmados (persistencia futura opcional).
- `on_product_created`: cachea metadatos básicos.
- `on_product_updated`: invalida caché y registra cambios.
- `on_user_authenticated`: registra actividad ligera.
- `on_company_settings_updated`: registra diffs básicos.

Migraciones:
- Generar antes de producción para `ProductAnalytics`:
  - `python manage.py makemigrations social`
  - `python manage.py migrate`

---

## 🛣️ Roadmap — Lista completa de TODO hasta producción

### ✅ 1) Completar Módulo de Eventos (integración Node → Firebase → Django)

1.1 MÓDULO 6F — Cloud Function que escucha Firestore

Qué hace:
- Observa la colección `/events`.
- Cuando Node publica un evento, la Function lo detecta.
- Le agrega firma HMAC.
- Envía el evento a Django vía `POST /internal/events`.
- Garantiza entrega confiable.
- Maneja reintentos si algo falla.

Por qué es necesario:
- Sin esto, Django nunca recibe los eventos.
- Analytics no se actualiza.
- No hay sincronización entre APIs.

1.2 MÓDULO 6G — Configurar proyecto Firebase

Qué hace:
- Crear proyecto en Firebase.
- Habilitar Firestore.
- Crear credencial Service Account.
- Descargar JSON.
- Configurar roles.
- Crear la colección `events`.

Por qué es necesario:
- Firestore es tu “message bus”.
- Es el puente entre Node y Django.
- Asegura que los eventos nunca se pierdan.

1.3 MÓDULO 6H — Validación de seguridad HMAC

Qué hace:
- Django valida que los eventos vengan realmente de Firebase.
- Previene ataques.
- Evita que alguien llame `/internal/events`.

Por qué es necesario:
- Seguridad.
- Integridad de datos.
- Protección del backend.

### ✅ 2) Completar el motor interno de procesamiento de eventos en Django

2.1 Completar la lógica de cada evento

Eventos que aún requieren implementación real:
- `UserAuthenticated`: registrar actividad de sesión.
- `UserRegistered`: analizar nuevos usuarios por día.
- `ProductCreated`: actualizar catálogo local/caché.
- `ProductUpdated`: invalidar caché y registrar cambios.
- `OrderCreated`: sumar ventas pendientes.
- `PaymentApproved`: sumar ingresos confirmados.
- `InvoiceIssued`: actualizar métricas de facturación.
- `ShipmentCreated`: registrar tiempos logísticos.
- `DiscountApplied`: medir uso real de cupones.
- `CompanySettingsUpdated`: registrar cambios administrativos.

Por qué es necesario:
- Alimenta dashboards del panel admin.
- Permite estadísticas reales y tendencias.
- Mantiene sincronía entre Node y Django.

2.2 Crear modelos internos de Analytics opcionales

Qué hacen:
- Guardan tendencias históricas.
- Pre-calculan métricas para acelerar panel admin.
- Permiten gráficos: ventas por día, ingresos acumulados, etc.

Por qué es necesario:
- Evita recalcular estadísticas cada vez.
- Acelera queries.
- Da soporte a dashboards profesionales.

2.3 Crear servicios auxiliares

- Servicio de ventas por usuario.
- Servicio de ingresos confirmados.
- Servicio de recuento de items vendidos.
- Servicio de comportamiento de productos.
- Servicio de cacheo e invalidación de productos.

Por qué:
- Mantienen el código limpio y escalable.
- Permiten dividir responsabilidades.
- Harán que la API sea más rápida.

### ✅ 3) Completar integración Node → Django (API requests)

3.1 Registrador de cache local de productos en Django

Qué hace:
- Cuando se llama `/v1/products/{id}/comments`, Django consulta a Node.
- Guarda el producto temporalmente en caché.
- Si hay `ProductUpdated` → invalida cache.

Por qué:
- Evita hacer cada vez llamadas a Node.
- Acelera comentarios, ratings y analytics.

3.2 Repositorio completo de órdenes, facturas y pagos

Qué hace:
- Django consulta Node para obtener órdenes.
- Necesario para analytics (ventas, ingresos, etc.).

Por qué:
- Django no tiene su propia DB de órdenes.
- Todo proviene del core Node.

### ✅ 4) Completar Módulo de Analytics en Django

- 4.1 Top productos por ventas.
- 4.2 Top productos por ingresos.
- 4.3 Overview general del negocio.
- 4.4 Ventas por día/semana/mes.
- 4.5 Actividad de usuarios.
- 4.6 Métricas de descuento.

Por qué:
- Es lo que va a consumir el panel admin Node+Electron.
- Permite gráficos, indicadores y dashboards avanzados.
- Da real valor agregado a Django.

### ✅ 5) Integración con comentarios y calificaciones

5.1 Validaciones avanzadas
- No permitir 2 ratings del mismo usuario en un producto.
- Moderación (opcional).
- Auto-aprobación de comentarios dependiendo del contenido.

5.2 Conexión con Analytics
- Cada comentario y rating modifica el “score social” de un producto.
- El panel admin podrá ver “tendencia de opinión”.

Por qué:
- Cierra la parte social.
- Permite enriquecer la analítica con feedback de usuarios.

### ✅ 6) Instalación de JWT en Django (validar tokens de Node)

Qué falta:
- Configurar middleware.
- Descargar clave pública (si se usa RS256).
- Validar claims (`sub`, `exp`, `issuer`).

Por qué:
- Ratings, comentarios y endpoints analíticos requieren saber quién es el usuario.
- Las APIs deben compartir identidad sin compartir DB.

---

## 🧪 Pruebas y calidad

- Tests de servicios (`event_processor_service`, `analytics_service`).
- Tests de vistas (permisos, validación y respuestas).
- Pruebas de contrato (envelope v1, HMAC correcto/incorrecto).

## 🚀 Despliegue y operación

- No commitear secretos; usar variables de entorno.
- Rotar `INTERNAL_EVENTS_SECRET` coordinado con Cloud Function.
- Aplicar migraciones antes de exponer endpoints analíticos.
- Observabilidad: logs y alertas en errores de procesamiento de eventos.

---

¿Querés que agregue diagramas de secuencia (eventos y JWT) o ejemplos de Cloud Function/Node listos para copiar? Los puedo sumar como anexos.