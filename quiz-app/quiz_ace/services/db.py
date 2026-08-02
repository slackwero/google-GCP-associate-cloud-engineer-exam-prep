"""Motor SQLite local para el historial de práctica."""

from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

RUTA_DB = Path(__file__).parent.parent.parent / "quiz_ace.db"

engine = create_engine(f"sqlite:///{RUTA_DB}")


def init_db() -> None:
    """Crea las tablas si no existen (idempotente)."""
    from ..models import registro  # noqa: F401 — registra los modelos en el metadata

    SQLModel.metadata.create_all(engine)


def abrir_sesion() -> Session:
    return Session(engine)
