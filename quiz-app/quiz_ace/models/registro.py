"""Modelos de persistencia del historial de práctica (SQLite local)."""

from datetime import UTC, datetime

import reflex as rx


def ahora() -> datetime:
    return datetime.now(UTC)


class Intento(rx.Model, table=True):
    """Un intento de quiz o examen, completo o abandonado."""

    modo: str  # estudio-curso | estudio-servicio | examen-corto | examen-medio | examen-full
    filtro: str = ""  # slug del curso/servicio y nivel usados, si aplican
    inicio: datetime
    fin: datetime | None = None
    duracion_seg: int = 0
    puntaje: float = 0.0
    correctas: int = 0
    total: int = 0
    completado: bool = False


class Respuesta(rx.Model, table=True):
    """Respuesta individual dentro de un intento.

    Desnormaliza los metadatos de la pregunta para que las estadísticas
    del dashboard no dependan de re-leer los JSON del banco.
    """

    intento_id: int
    pregunta_id: str
    respuesta_dada: str = ""  # letras separadas por coma, p. ej. "A,C"
    correcta: bool = False
    tiempo_seg: int = 0
    curso: str = ""
    servicios: str = ""  # slugs separados por coma
    nivel: str = ""
    seccion: int = 0
    subtopicos: str = ""  # ids separados por coma
