import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore

try:
    import environ  # opcional: si está instalado, leemos .env
except Exception:
    environ = None


BASE_DIR = Path(__file__).resolve().parent


def resolve_credentials_path() -> str | None:
    """Obtiene la ruta al JSON de credenciales.
    Prioriza la variable GOOGLE_APPLICATION_CREDENTIALS del entorno/.env,
    y si no existe, intenta rutas comunes en ./secrets/.
    """
    env_path = BASE_DIR / ".env"
    cred_from_env: str | None = None

    # Cargar desde .env si existe y django-environ está disponible
    if environ and env_path.exists():
        env = environ.Env()
        env.read_env(str(env_path))
        cred_from_env = env("GOOGLE_APPLICATION_CREDENTIALS", default=None)
    else:
        cred_from_env = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    candidates: list[str] = []
    if cred_from_env:
        candidates.append(cred_from_env)

    # Fallbacks comunes
    candidates.extend([
        "./secrets/serviceAccountKey.json",
        "./secrets/service-account.json",
    ])

    for c in candidates:
        p = Path(c)
        if not p.is_absolute():
            p = (BASE_DIR / p).resolve()
        if p.exists():
            return str(p)
    return None


def main():
    cred_path = resolve_credentials_path()
    if not cred_path:
        print("❌ No encontré credenciales de Firebase.")
        print("Coloca el JSON en ./secrets/serviceAccountKey.json o ./secrets/service-account.json")
        print("O define GOOGLE_APPLICATION_CREDENTIALS en .env o en el entorno.")
        return

    try:
        cred = credentials.Certificate(cred_path)
        # Inicializar sólo si no hay apps registradas
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)

        db = firestore.client()
        docs = db.collection("events").limit(1).stream()
        count = 0
        for doc in docs:
            print(f"Documento: {doc.id} => {doc.to_dict()}")
            count += 1
        if count == 0:
            print("✅ Conectado a Firestore, pero no hay documentos en 'events'.")
        else:
            print(f"✅ Conectado correctamente. {count} documento(s) leídos.")
    except Exception as e:
        print("❌ Error al conectar con Firestore:", e)
        print(f"Intenté usar credenciales en: {cred_path}")


if __name__ == "__main__":
    main()