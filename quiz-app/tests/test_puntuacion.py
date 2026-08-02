"""Tests de la puntuación: corrección, puntaje y desglose."""

from quiz_ace.services.puntuacion import calcular_resultado, es_correcta

UMBRAL_APROBACION = 70.0


def _pregunta(id_, tipo="unica", respuesta=("A",), seccion=2, servicios=("gke",), subtopicos=("2.1-compute-choices",)):
    return {
        "id": id_,
        "curso": "curso-a",
        "servicios": list(servicios),
        "seccion_blueprint": seccion,
        "subtopicos": list(subtopicos),
        "nivel": "intermedio",
        "tipo": tipo,
        "pregunta": {"en": "Q", "es": "P"},
        "opciones": [{"en": o, "es": o} for o in ("op A", "op B", "op C", "op D")],
        "respuesta": list(respuesta),
        "explicacion": {"en": "E", "es": "E"},
        "doc": "https://cloud.google.com/docs",
    }


class TestEsCorrecta:
    def test_unica_correcta(self):
        assert es_correcta(_pregunta("q1"), ["A"]) is True

    def test_unica_incorrecta(self):
        assert es_correcta(_pregunta("q1"), ["B"]) is False

    def test_multiple_exige_conjunto_exacto(self):
        pregunta = _pregunta("q1", tipo="multiple", respuesta=("A", "C"))
        assert es_correcta(pregunta, ["C", "A"]) is True
        assert es_correcta(pregunta, ["A"]) is False
        assert es_correcta(pregunta, ["A", "C", "D"]) is False

    def test_sin_respuesta_es_incorrecta(self):
        assert es_correcta(_pregunta("q1"), []) is False


class TestCalcularResultado:
    def test_puntaje_y_aprobacion(self):
        preguntas = [_pregunta(f"q{i}") for i in range(10)]
        respuestas = {f"q{i}": ["A"] if i < 8 else ["B"] for i in range(10)}
        resultado = calcular_resultado(preguntas, respuestas)
        assert resultado.puntaje == 80.0
        assert resultado.aprobado is True
        assert resultado.correctas == 8
        assert resultado.total == 10

    def test_reprobado_bajo_el_umbral(self):
        preguntas = [_pregunta(f"q{i}") for i in range(10)]
        respuestas = {f"q{i}": ["A"] if i < 6 else ["B"] for i in range(10)}
        resultado = calcular_resultado(preguntas, respuestas)
        assert resultado.puntaje == 60.0
        assert resultado.aprobado is False

    def test_pregunta_sin_responder_cuenta_como_incorrecta(self):
        preguntas = [_pregunta("q0"), _pregunta("q1")]
        resultado = calcular_resultado(preguntas, {"q0": ["A"]})
        assert resultado.correctas == 1
        assert resultado.total == 2

    def test_desglose_por_seccion(self):
        preguntas = [
            _pregunta("q0", seccion=1),
            _pregunta("q1", seccion=1),
            _pregunta("q2", seccion=4),
        ]
        respuestas = {"q0": ["A"], "q1": ["B"], "q2": ["A"]}
        resultado = calcular_resultado(preguntas, respuestas)
        assert resultado.por_seccion[1] == (1, 2)
        assert resultado.por_seccion[4] == (1, 1)

    def test_desglose_por_servicio(self):
        preguntas = [
            _pregunta("q0", servicios=("gke", "iam")),
            _pregunta("q1", servicios=("iam",)),
        ]
        respuestas = {"q0": ["A"], "q1": ["B"]}
        resultado = calcular_resultado(preguntas, respuestas)
        assert resultado.por_servicio["gke"] == (1, 1)
        assert resultado.por_servicio["iam"] == (1, 2)

    def test_falladas_conserva_la_respuesta_dada(self):
        preguntas = [_pregunta("q0"), _pregunta("q1")]
        respuestas = {"q0": ["A"], "q1": ["C"]}
        resultado = calcular_resultado(preguntas, respuestas)
        assert [f["pregunta"]["id"] for f in resultado.falladas] == ["q1"]
        assert resultado.falladas[0]["respuesta_dada"] == ["C"]
