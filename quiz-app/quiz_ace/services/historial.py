"""History maintenance: count and delete practice attempts.

Deleting is irreversible and there is no backup, so every function returns how
many rows it removed: that is what the UI shows before asking for confirmation.
"""

from sqlmodel import Session, col, select

from ..models.registro import Intento, Respuesta


def contar_historial(session: Session) -> dict[str, int]:
    """Count what is stored today, to announce the scope of each deletion."""
    intentos = session.exec(select(Intento)).all()
    respuestas = session.exec(select(Respuesta)).all()

    incompletos = {i.id for i in intentos if not i.completado}
    return {
        "intentos": len(intentos),
        "intentos_incompletos": len(incompletos),
        "respuestas": len(respuestas),
        "respuestas_incompletas": sum(1 for r in respuestas if r.intento_id in incompletos),
    }


def borrar_todo(session: Session) -> dict[str, int]:
    """Wipe the whole history. The question bank is never touched."""
    respuestas = session.exec(select(Respuesta)).all()
    intentos = session.exec(select(Intento)).all()

    for fila in (*respuestas, *intentos):
        session.delete(fila)
    session.commit()

    return {"intentos": len(intentos), "respuestas": len(respuestas)}


def borrar_incompletos(session: Session) -> dict[str, int]:
    """Drop abandoned attempts and keep the ones that were finished."""
    intentos = session.exec(select(Intento).where(col(Intento.completado) == False)).all()  # noqa: E712
    ids = [i.id for i in intentos if i.id is not None]
    if not ids:
        return {"intentos": 0, "respuestas": 0}

    # Answers go first: intento_id is an index, not a foreign key with cascade,
    # so deleting the attempt alone would orphan them and they would keep
    # weighing on the dashboard mastery figures.
    respuestas = session.exec(select(Respuesta).where(col(Respuesta.intento_id).in_(ids))).all()
    for fila in (*respuestas, *intentos):
        session.delete(fila)
    session.commit()

    return {"intentos": len(intentos), "respuestas": len(respuestas)}
