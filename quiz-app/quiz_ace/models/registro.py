"""Modelos de persistencia del historial de práctica (SQLite local)."""

from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def ahora() -> datetime:
    """UTC sin zona horaria: SQLite no la conserva, y mezclar fechas con y sin
    tzinfo hace fallar cualquier resta contra un registro leído de la base."""
    return datetime.now(UTC).replace(tzinfo=None)


class Intento(SQLModel, table=True):
    """Un intento de quiz o examen, completo o abandonado."""

    id: int | None = Field(default=None, primary_key=True)
    modo: str  # estudio-curso | estudio-servicio | examen-corto | examen-medio | examen-full
    filtro: str = ""  # slug del curso/servicio y nivel usados, si aplican
    inicio: datetime
    fin: datetime | None = None
    duracion_seg: int = 0
    puntaje: float = 0.0
    correctas: int = 0
    total: int = 0
    completado: bool = False


class Respuesta(SQLModel, table=True):
    """Respuesta individual dentro de un intento.

    Desnormaliza los metadatos de la pregunta para que las estadísticas
    del dashboard no dependan de re-leer los JSON del banco.
    """

    id: int | None = Field(default=None, primary_key=True)
    intento_id: int = Field(index=True)
    pregunta_id: str = Field(index=True)
    fecha: datetime
    respuesta_dada: str = ""  # letras separadas por coma, p. ej. "A,C"
    correcta: bool = False
    tiempo_seg: int = 0
    curso: str = ""
    servicios: str = ""  # slugs separados por coma
    nivel: str = ""
    seccion: int = 0
    subtopicos: str = ""  # ids separados por coma
