"""Tests de las estadísticas del dashboard: dominio, cobertura y enfoque."""

from datetime import UTC, datetime, timedelta

from quiz_ace.services.estadisticas import (
    calcular_cobertura,
    calcular_dominio,
    calcular_enfoque,
    clasificar_dominio,
)

AHORA = datetime(2026, 8, 2, 12, 0, tzinfo=UTC)


def _respuesta(pregunta_id, correcta, dias_atras=0, curso="curso-a", servicios="gke", seccion=2, subtopicos="2.1-x"):
    return {
        "pregunta_id": pregunta_id,
        "correcta": correcta,
        "fecha": AHORA - timedelta(days=dias_atras),
        "curso": curso,
        "servicios": servicios,
        "seccion": seccion,
        "subtopicos": subtopicos,
    }


class TestClasificarDominio:
    def test_umbrales(self):
        assert clasificar_dominio(85.0) == "fuerte"
        assert clasificar_dominio(70.0) == "medio"
        assert clasificar_dominio(59.9) == "debil"
        assert clasificar_dominio(None) == "sin_practicar"


class TestCalcularDominio:
    def test_agrupa_por_seccion(self):
        respuestas = [
            _respuesta("q1", True, seccion=1),
            _respuesta("q2", True, seccion=1),
            _respuesta("q3", False, seccion=4),
        ]
        dominio = calcular_dominio(respuestas, dimension="seccion", ahora=AHORA)
        assert dominio[1]["pct"] == 100.0
        assert dominio[1]["estado"] == "fuerte"
        assert dominio[4]["pct"] == 0.0
        assert dominio[4]["estado"] == "debil"

    def test_agrupa_por_servicio_multivalor(self):
        respuestas = [
            _respuesta("q1", True, servicios="gke,iam"),
            _respuesta("q2", False, servicios="iam"),
        ]
        dominio = calcular_dominio(respuestas, dimension="servicios", ahora=AHORA)
        assert dominio["gke"]["pct"] == 100.0
        assert dominio["iam"]["pct"] == 50.0

    def test_lo_reciente_pesa_mas(self):
        historia = [_respuesta("q1", False, dias_atras=60), _respuesta("q2", True, dias_atras=0)]
        dominio = calcular_dominio(historia, dimension="seccion", ahora=AHORA)
        assert dominio[2]["pct"] > 50.0

    def test_sin_respuestas_devuelve_vacio(self):
        assert calcular_dominio([], dimension="seccion", ahora=AHORA) == {}


class TestCalcularCobertura:
    def test_cobertura_por_curso(self):
        banco = {"curso-a": ["q1", "q2", "q3", "q4"], "curso-b": ["q5", "q6"]}
        respuestas = [_respuesta("q1", True), _respuesta("q1", False), _respuesta("q2", True)]
        cobertura = calcular_cobertura(respuestas, banco, campo="curso")
        assert cobertura["curso-a"] == {"vistas": 2, "total": 4, "pct": 50.0}
        assert cobertura["curso-b"] == {"vistas": 0, "total": 2, "pct": 0.0}


class TestCalcularEnfoque:
    def test_prioriza_dominio_bajo_y_peso_alto(self):
        dominio = {
            2: {"pct": 40.0, "estado": "debil"},
            4: {"pct": 90.0, "estado": "fuerte"},
        }
        cobertura = {
            2: {"vistas": 5, "total": 10, "pct": 50.0},
            4: {"vistas": 9, "total": 10, "pct": 90.0},
        }
        pesos = {1: 0.20, 2: 0.30, 3: 0.30, 4: 0.20}
        enfoque = calcular_enfoque(dominio, cobertura, pesos)
        # Sin practicar va primero; entre ellas, mayor peso del examen primero.
        assert enfoque[0]["clave"] == 3
        assert enfoque[1]["clave"] == 1
        secciones_restantes = [e["clave"] for e in enfoque[2:]]
        assert secciones_restantes == [2, 4]

    def test_sin_practicar_va_primero(self):
        pesos = {1: 0.5, 2: 0.5}
        enfoque = calcular_enfoque({2: {"pct": 10.0, "estado": "debil"}}, {}, pesos)
        assert enfoque[0]["clave"] == 1
        assert enfoque[0]["estado"] == "sin_practicar"
