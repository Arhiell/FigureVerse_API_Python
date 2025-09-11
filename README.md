# 🎬 FilmTribe Sentiment Engine – API de Análisis de Comentarios de Películas  

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-success?logo=fastapi)](https://fastapi.tiangolo.com/)  
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen?logo=github)](https://github.com/)  

> Autores: **Ariel & Bautista – Técnico Universitario en Programación (UTN)**  
> Proyecto desarrollado en conjunto con el ecosistema **FilmTribe** (API principal en Node.js).

---

**FilmTribe Sentiment Engine** es una API desarrollada en **Python** que se encarga de **analizar los comentarios que los usuarios dejan sobre películas**, como parte del ecosistema de FilmTribe.  
A través del análisis de sentimientos, esta API permite clasificar cada opinión como **positiva, negativa o neutral**, y generar **informes** útiles para:

- 📊 Evaluar la percepción general del público.  
- ⭐ Determinar el posicionamiento emocional de las películas.  
- 📈 Obtener métricas para reportes, visualizaciones o dashboards.  
- 🔗 Conectarse con otros servicios como la API principal de FilmTribe desarrollada en Node.js.  

---

## 🚀 Características  

- 📥 Carga y gestión de comentarios.  
- 🤖 Clasificación automática de sentimientos.  
- 📊 Informes por película y globales.  
- 🔗 API REST para ser consumida desde otras partes del sistema FilmTribe.  
- 🧩 Arquitectura desacoplada, lista para integrarse vía HTTP o colas de mensajes.  
- 🔒 Validaciones y estructura robusta para datos limpios y trazables.  

---

## 🏗️ Tecnologías utilizadas  

- 🐍 **Python 3.11+**  
- ⚡ **FastAPI**  
- 🧠 **TextBlob / NLTK / Transformers** (según configuración)  
- 🗄️ **SQLite / MongoDB / MySQL**  
- 🔍 **Pydantic** para validación de datos  
- 📑 **Swagger UI** para documentación de endpoints  

---

## 📂 Estructura del proyecto  

```bash
📦 filmtribe-sentiment-engine
 ┣ 📂 app
 ┃ ┣ 📜 main.py              # Punto de entrada
 ┃ ┣ 📜 models.py            # Modelos de datos
 ┃ ┣ 📜 routes.py            # Endpoints principales
 ┃ ┣ 📜 sentiment.py         # Lógica de análisis
 ┃ ┣ 📜 database.py          # Conexión BD
 ┃ ┗ 📜 utils.py             # Funciones auxiliares
 ┣ 📂 tests                  # Pruebas unitarias
 ┣ 📜 requirements.txt       # Dependencias
 ┣ 📜 README.md              # Documentación
 ┗ 📜 .gitignore             # Archivos ignorados
