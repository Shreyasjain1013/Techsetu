import uuid
import datetime
from typing import List, Dict, Any, Optional
import requests
from app.config import SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY

class StorageService:
    def __init__(self):
        self.supabase_url = SUPABASE_URL
        self.supabase_key = SUPABASE_PUBLISHABLE_KEY
        # Local in-memory store for instant fallback and fast local tests
        self.history: List[Dict[str, Any]] = []

    def save_translation(
        self,
        original_content: str,
        translated_content: str,
        mode: str,
        integrity_score: float,
        analysis: Dict[str, Any],
        validation: Dict[str, Any]
    ) -> str:
        record_id = str(uuid.uuid4())
        record = {
            "id": record_id,
            "original_content": original_content,
            "translated_content": translated_content,
            "mode": mode,
            "integrity_score": integrity_score,
            "analysis": analysis,
            "validation": validation,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self.history.insert(0, record)

        # Attempt to save to Supabase if credentials are valid
        if self.supabase_url and self.supabase_key and "supabase.com/dashboard" not in self.supabase_url:
            try:
                headers = {
                    "apikey": self.supabase_key,
                    "Authorization": f"Bearer {self.supabase_key}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal"
                }
                payload = {
                    "id": record_id,
                    "mode": mode,
                    "translated_content": translated_content,
                    "integrity_score": integrity_score,
                    "status": "completed"
                }
                requests.post(
                    f"{self.supabase_url.rstrip('/')}/rest/v1/translations",
                    headers=headers,
                    json=payload,
                    timeout=3
                )
            except Exception:
                pass # Silently proceed with local storage

        return record_id

    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self.history[:limit]

storage = StorageService()
