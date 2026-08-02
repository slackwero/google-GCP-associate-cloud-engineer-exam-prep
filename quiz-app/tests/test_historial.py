"""History deletion tests: what goes, what stays, and what must not be orphaned."""

from sqlmodel import Session, SQLModel, create_engine, select

from quiz_ace.models.registro import Intento, Respuesta, ahora
from quiz_ace.services.historial import borrar_incompletos, borrar_todo, contar_historial


def _engine(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path}/test.db")
    SQLModel.metadata.create_all(engine)
    return engine


def _poblar(session):
    """Two finished attempts and one abandoned, each with its own answers."""
    completado_a = Intento(modo="examen-corto", inicio=ahora(), completado=True, total=2)
    completado_b = Intento(modo="estudio-curso", inicio=ahora(), completado=True, total=1)
    abandonado = Intento(modo="examen-full", inicio=ahora(), completado=False, total=1)
    session.add_all([completado_a, completado_b, abandonado])
    session.commit()

    for intento, cuantas in ((completado_a, 2), (completado_b, 1), (abandonado, 1)):
        for i in range(cuantas):
            session.add(
                Respuesta(
                    intento_id=intento.id,
                    pregunta_id=f"q-{intento.id}-{i}",
                    fecha=ahora(),
                    correcta=True,
                )
            )
    session.commit()
    return {"completados": [completado_a.id, completado_b.id], "abandonado": abandonado.id}


def test_contar_historial_distingue_incompletos(tmp_path):
    with Session(_engine(tmp_path)) as session:
        _poblar(session)
        conteo = contar_historial(session)

    assert conteo["intentos"] == 3
    assert conteo["intentos_incompletos"] == 1
    assert conteo["respuestas"] == 4
    # The "clear unfinished" dialog announces this number, not the total:
    # promising 4 and deleting 1 would misstate the scope of the deletion.
    assert conteo["respuestas_incompletas"] == 1


def test_contar_historial_vacio(tmp_path):
    with Session(_engine(tmp_path)) as session:
        conteo = contar_historial(session)

    assert conteo == {
        "intentos": 0,
        "intentos_incompletos": 0,
        "respuestas": 0,
        "respuestas_incompletas": 0,
    }


def test_borrar_todo_vacia_ambas_tablas(tmp_path):
    engine = _engine(tmp_path)
    with Session(engine) as session:
        _poblar(session)
        borrado = borrar_todo(session)

    assert borrado == {"intentos": 3, "respuestas": 4}
    with Session(engine) as session:
        assert session.exec(select(Intento)).all() == []
        assert session.exec(select(Respuesta)).all() == []


def test_borrar_todo_sobre_base_vacia_no_falla(tmp_path):
    with Session(_engine(tmp_path)) as session:
        assert borrar_todo(session) == {"intentos": 0, "respuestas": 0}


def test_borrar_incompletos_conserva_los_completados_y_sus_respuestas(tmp_path):
    engine = _engine(tmp_path)
    with Session(engine) as session:
        ids = _poblar(session)
        borrado = borrar_incompletos(session)

    assert borrado == {"intentos": 1, "respuestas": 1}
    with Session(engine) as session:
        quedan = {i.id for i in session.exec(select(Intento)).all()}
        assert quedan == set(ids["completados"])
        # Answers belonging to the finished attempts are still intact.
        assert len(session.exec(select(Respuesta)).all()) == 3


def test_borrar_incompletos_no_deja_respuestas_huerfanas(tmp_path):
    """intento_id is an index, not a cascading foreign key: if the attempt is
    deleted without its answers, they keep polluting the dashboard mastery."""
    engine = _engine(tmp_path)
    with Session(engine) as session:
        _poblar(session)
        borrar_incompletos(session)

    with Session(engine) as session:
        intentos_vivos = {i.id for i in session.exec(select(Intento)).all()}
        huerfanas = [r for r in session.exec(select(Respuesta)).all() if r.intento_id not in intentos_vivos]
        assert huerfanas == []


def test_borrar_incompletos_sin_incompletos_no_toca_nada(tmp_path):
    engine = _engine(tmp_path)
    with Session(engine) as session:
        intento = Intento(modo="examen-corto", inicio=ahora(), completado=True, total=1)
        session.add(intento)
        session.commit()
        session.add(Respuesta(intento_id=intento.id, pregunta_id="q-1", fecha=ahora(), correcta=True))
        session.commit()

        assert borrar_incompletos(session) == {"intentos": 0, "respuestas": 0}

    with Session(engine) as session:
        assert len(session.exec(select(Intento)).all()) == 1
        assert len(session.exec(select(Respuesta)).all()) == 1
