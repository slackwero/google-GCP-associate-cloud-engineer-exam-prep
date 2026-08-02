"""Tests del muestreo de preguntas: estudio filtrado y exámenes aleatorios."""

import random

import pytest

from quiz_ace.services.muestreo import barajar_opciones, generar_examen, seleccionar_estudio

NIVELES = ("principiante", "intermedio", "avanzado")


def _pregunta(id_, curso="curso-a", servicios=("gke",), seccion=2, nivel="principiante"):
    return {
        "id": id_,
        "curso": curso,
        "servicios": list(servicios),
        "seccion_blueprint": seccion,
        "subtopicos": ["2.1-compute-choices"],
        "nivel": nivel,
        "tipo": "unica",
        "pregunta": {"en": f"Q{id_}", "es": f"P{id_}"},
        "opciones": [
            {"en": "Correct", "es": "Correcta"},
            {"en": "Wrong 1", "es": "Incorrecta 1"},
            {"en": "Wrong 2", "es": "Incorrecta 2"},
            {"en": "Wrong 3", "es": "Incorrecta 3"},
        ],
        "respuesta": ["A"],
        "explicacion": {"en": "Because.", "es": "Porque sí."},
        "doc": "https://cloud.google.com/docs",
    }


@pytest.fixture
def banco_preguntas():
    """Banco sintético: 40 preguntas por sección (1-4), niveles y cursos variados."""
    preguntas = []
    for seccion in (1, 2, 3, 4):
        for i in range(40):
            preguntas.append(
                _pregunta(
                    f"s{seccion}-{i:03d}",
                    curso=f"curso-{seccion}",
                    servicios=("gke",) if i % 2 == 0 else ("iam",),
                    seccion=seccion,
                    nivel=NIVELES[i % 3],
                )
            )
    return preguntas


class TestSeleccionarEstudio:
    def test_filtra_por_curso(self, banco_preguntas):
        seleccion = seleccionar_estudio(banco_preguntas, curso="curso-2", rng=random.Random(1))
        assert seleccion and all(p["curso"] == "curso-2" for p in seleccion)

    def test_filtra_por_servicio_y_nivel(self, banco_preguntas):
        seleccion = seleccionar_estudio(banco_preguntas, servicio="iam", nivel="avanzado", rng=random.Random(1))
        assert seleccion
        assert all("iam" in p["servicios"] and p["nivel"] == "avanzado" for p in seleccion)

    def test_limite_restringe_cantidad(self, banco_preguntas):
        seleccion = seleccionar_estudio(banco_preguntas, curso="curso-1", limite=5, rng=random.Random(1))
        assert len(seleccion) == 5

    def test_baraja_el_orden(self, banco_preguntas):
        ids_a = [p["id"] for p in seleccionar_estudio(banco_preguntas, curso="curso-1", rng=random.Random(1))]
        ids_b = [p["id"] for p in seleccionar_estudio(banco_preguntas, curso="curso-1", rng=random.Random(2))]
        assert sorted(ids_a) == sorted(ids_b)
        assert ids_a != ids_b

    def test_sin_coincidencias_devuelve_vacio(self, banco_preguntas):
        assert seleccionar_estudio(banco_preguntas, curso="curso-inexistente", rng=random.Random(1)) == []


class TestGenerarExamen:
    def test_examen_corto_tiene_20_preguntas_unicas(self, banco_preguntas):
        examen = generar_examen(banco_preguntas, tamano=20, rng=random.Random(1))
        assert len(examen) == 20
        assert len({p["id"] for p in examen}) == 20

    def test_examen_full_respeta_pesos_del_blueprint(self, banco_preguntas):
        examen = generar_examen(banco_preguntas, tamano=50, ponderado=True, rng=random.Random(1))
        por_seccion = {s: sum(1 for p in examen if p["seccion_blueprint"] == s) for s in (1, 2, 3, 4)}
        assert por_seccion == {1: 10, 2: 15, 3: 15, 4: 10}

    def test_examen_ponderado_sin_banco_suficiente_completa_con_otras_secciones(self):
        preguntas = [_pregunta(f"p-{i}", seccion=2) for i in range(60)]
        examen = generar_examen(preguntas, tamano=50, ponderado=True, rng=random.Random(1))
        assert len(examen) == 50

    def test_tamano_mayor_al_banco_devuelve_todo_el_banco(self):
        preguntas = [_pregunta(f"p-{i}") for i in range(10)]
        examen = generar_examen(preguntas, tamano=20, rng=random.Random(1))
        assert len(examen) == 10


class TestBarajarOpciones:
    def test_remapea_respuesta_a_la_nueva_posicion(self):
        pregunta = _pregunta("q1")
        barajada = barajar_opciones(pregunta, rng=random.Random(3))
        letras = "ABCD"
        indices_correctos = [letras.index(letra) for letra in barajada["respuesta"]]
        assert [barajada["opciones"][i]["en"] for i in indices_correctos] == ["Correct"]

    def test_no_modifica_la_pregunta_original(self):
        pregunta = _pregunta("q1")
        opciones_originales = [o["en"] for o in pregunta["opciones"]]
        barajar_opciones(pregunta, rng=random.Random(3))
        assert [o["en"] for o in pregunta["opciones"]] == opciones_originales

    def test_multiple_conserva_todas_las_correctas(self):
        pregunta = _pregunta("q1")
        pregunta["tipo"] = "multiple"
        pregunta["respuesta"] = ["A", "C"]
        barajada = barajar_opciones(pregunta, rng=random.Random(5))
        letras = "ABCD"
        textos = {barajada["opciones"][letras.index(le)]["en"] for le in barajada["respuesta"]}
        assert textos == {"Correct", "Wrong 2"}
