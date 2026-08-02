"""Quality gate de cobertura del banco real contra el blueprint oficial 2026.

Estos tests garantizan que el banco cubre el 100% de la guía del examen.
Están en xfail mientras se completa la generación masiva (Fase 4);
al terminarla se retiran los marcadores y DEBEN pasar.
"""

from pathlib import Path

import pytest

from quiz_ace.services.banco import cargar_banco, cargar_catalogos

DATA_DIR = Path(__file__).parent.parent / "data"

MIN_PREGUNTAS_POR_SUBTOPICO = 5
MIN_PREGUNTAS_POR_CURSO = 60
MIN_PREGUNTAS_TOTAL = 1200


@pytest.fixture(scope="module")
def banco():
    return cargar_banco(DATA_DIR)


@pytest.fixture(scope="module")
def catalogos():
    return cargar_catalogos(DATA_DIR)


def test_banco_sin_preguntas_invalidas(banco):
    detalles = [f"{e.archivo}/{e.id}: {'; '.join(e.errores)}" for e in banco.excluidas]
    assert banco.excluidas == [], "Preguntas inválidas en el banco:\n" + "\n".join(detalles)


@pytest.mark.xfail(reason="Banco en construcción (Fase 4): aún no se alcanza el total meta", strict=False)
def test_total_de_preguntas(banco):
    assert len(banco.preguntas) >= MIN_PREGUNTAS_TOTAL


@pytest.mark.xfail(reason="Banco en construcción (Fase 4): cursos aún sin banco completo", strict=False)
def test_cada_curso_tiene_minimo_de_preguntas(banco, catalogos):
    faltantes = {
        slug: len(banco.por_curso.get(slug, []))
        for slug in catalogos.cursos
        if len(banco.por_curso.get(slug, [])) < MIN_PREGUNTAS_POR_CURSO
    }
    assert not faltantes, f"Cursos bajo el mínimo de {MIN_PREGUNTAS_POR_CURSO}: {faltantes}"


@pytest.mark.xfail(reason="Banco en construcción (Fase 4): subtópicos aún sin cubrir", strict=False)
def test_cada_subtopico_del_blueprint_esta_cubierto(banco, catalogos):
    faltantes = {
        subtopico: len(banco.por_subtopico.get(subtopico, []))
        for subtopico in catalogos.subtopicos
        if len(banco.por_subtopico.get(subtopico, [])) < MIN_PREGUNTAS_POR_SUBTOPICO
    }
    assert not faltantes, f"Subtópicos bajo el mínimo de {MIN_PREGUNTAS_POR_SUBTOPICO}: {faltantes}"


@pytest.mark.xfail(reason="Banco en construcción (Fase 4): niveles aún sin equilibrar", strict=False)
def test_cada_nivel_tiene_presencia_significativa(banco):
    for nivel in ("principiante", "intermedio", "avanzado"):
        assert len(banco.por_nivel.get(nivel, [])) >= MIN_PREGUNTAS_TOTAL * 0.2, nivel
