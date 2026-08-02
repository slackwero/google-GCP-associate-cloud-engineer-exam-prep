"""Tests de persistencia del historial: las fechas deben ser operables tras leerlas."""

from sqlmodel import Session, SQLModel, create_engine, select

from quiz_ace.models.registro import Intento, Respuesta, ahora


def _engine(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path}/test.db")
    SQLModel.metadata.create_all(engine)
    return engine


def test_duracion_de_un_intento_leido_de_la_base(tmp_path):
    """SQLite devuelve datetimes sin zona horaria: restarlos no debe fallar."""
    engine = _engine(tmp_path)
    with Session(engine) as session:
        session.add(Intento(modo="examen-corto", inicio=ahora(), total=20))
        session.commit()

    with Session(engine) as session:
        intento = session.exec(select(Intento)).one()
        intento.fin = ahora()
        # Esta resta es la que ejecuta ExamState.enviar al cerrar el intento.
        duracion = (intento.fin - intento.inicio).total_seconds()
        assert duracion >= 0


def test_antiguedad_de_una_respuesta_leida_de_la_base(tmp_path):
    """El dashboard pondera por recencia: ahora() - fecha tampoco debe fallar."""
    engine = _engine(tmp_path)
    with Session(engine) as session:
        session.add(Respuesta(intento_id=1, pregunta_id="gke-001", fecha=ahora(), correcta=True))
        session.commit()

    with Session(engine) as session:
        respuesta = session.exec(select(Respuesta)).one()
        assert (ahora() - respuesta.fecha).total_seconds() >= 0
