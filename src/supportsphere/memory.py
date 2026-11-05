"""Small local JSON conversation store for demonstration purposes."""
import json
from pathlib import Path
from datetime import datetime, timezone

class ConversationMemory:
    def __init__(self, path: str | Path = ".supportsphere-memory.json"):
        self.path = Path(path)

    def _load(self) -> list[dict]:
        if not self.path.exists():
            return []
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

    def add_turn(self, session_id: str, user: str, assistant: str) -> None:
        turns = self._load()
        turns.append({
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user": user,
            "assistant": assistant,
        })
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(turns, indent=2), encoding="utf-8")

    def recent(self, session_id: str, limit: int = 5) -> list[dict]:
        return [t for t in self._load() if t.get("session_id") == session_id][-limit:]
