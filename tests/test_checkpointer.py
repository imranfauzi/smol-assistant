import sqlite3

import pytest
from langgraph.checkpoint.sqlite import SqliteSaver

from core import checkpointer


def test_get_assistant_memory_creates_parent_directory(monkeypatch, tmp_path):
    db_path = tmp_path / "memory" / "assistant.sqlite"
    monkeypatch.setattr(checkpointer.settings, "CHECKPOINTER_PATH", str(db_path))

    memory = checkpointer.get_assistant_memory()

    assert isinstance(memory, SqliteSaver)
    assert db_path.exists()


def test_get_assistant_memory_wraps_sqlite_errors(monkeypatch, tmp_path):
    db_path = tmp_path / "checkpointer"
    db_path.mkdir()

    # A directory path should fail because sqlite expects a file path.
    monkeypatch.setattr(checkpointer.settings, "CHECKPOINTER_PATH", str(db_path))

    with pytest.raises(RuntimeError) as exc_info:
        checkpointer.get_assistant_memory()

    error_message = str(exc_info.value)
    assert "Initialization critical failure for assistant memory" in error_message
    assert str(db_path) in error_message
    assert isinstance(exc_info.value.__cause__, sqlite3.Error)
