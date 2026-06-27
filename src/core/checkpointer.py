import sqlite3
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver

from core.config import settings

def get_assistant_memory() -> SqliteSaver:
    try:
        assistant_db_path = Path(settings.CHECKPOINTER_PATH).resolve()
        assistant_db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(str(assistant_db_path), check_same_thread=False)
        return SqliteSaver(sqlite_conn)
        
    except (OSError, sqlite3.Error) as e:
        raise RuntimeError(
            f"Initialization critical failure for assistant memory at '{settings.CHECKPOINTER_PATH}': {e}"
        ) from e