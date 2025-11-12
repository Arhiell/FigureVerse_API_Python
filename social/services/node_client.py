import os
import requests


class NodeClient:
    """Cliente simple para consumir tu API Node (placeholder)."""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or os.getenv("NODE_API_BASE_URL", "http://localhost:3000")

    def get_health(self) -> dict:
        try:
            r = requests.get(f"{self.base_url}/health", timeout=5)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {"ok": False, "error": str(e)}