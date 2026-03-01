"""
In-memory storage for the To-Do List App.

All task data is stored in a module-level dict keyed by task UUID (str).
No database, no file I/O — data lives only for the lifetime of the process.

Call reset() between tests to ensure isolation.
"""

from typing import Dict

# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

# tasks: Dict[task_id (str) -> task dict]
# Each task dict shape:
#   {
#     "id":          str (UUID),
#     "title":       str,
#     "description": str | None,
#     "status":      str ("todo" | "in_progress" | "done"),
#     "priority":    str ("low" | "medium" | "high"),
#     "created_at":  str (ISO 8601),
#     "updated_at":  str (ISO 8601),
#   }
tasks: Dict[str, dict] = {}


def reset() -> None:
    """Clear all task data. Intended for use in tests only."""
    tasks.clear()
