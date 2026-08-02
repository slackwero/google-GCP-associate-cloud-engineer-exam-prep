"""Tests del servicio de banco de preguntas: carga, validación e índices."""

import json
from pathlib import Path

import pytest

from quiz_ace.services.banco import cargar_banco, cargar_catalogos, validar_pregunta

DATA_DIR = Path(__file__).parent.parent / "data"


def pregunta_valida(**overrides) -> dict:
    base = {
        "id": "gke-001",
        "curso": "como-comenzar-gke",
        "servicios": ["gke"],
        "seccion_blueprint": 2,
        "subtopicos": ["2.1-gke-cluster-configs"],
        "nivel": "principiante",
        "tipo": "unica",
        "pregunta": {"en": "What is GKE?", "es": "¿Qué es GKE?"},
        "opciones": [
            {"en": "A managed Kubernetes service", "es": "Un servicio administrado de Kubernetes"},
            {"en": "A database", "es": "Una base de datos"},
            {"en": "A load balancer", "es": "Un balanceador de cargas"},
            {"en": "A VPN", "es": "Una VPN"},
        ],
        "respuesta": ["A"],
        "explicacion": {
            "en": "GKE is Google's managed Kubernetes service; the rest are unrelated products.",
            "es": "GKE es el servicio administrado de Kubernetes de Google; el resto son productos no relacionados.",
        },
        "doc": "https://cloud.google.com/kubernetes-engine/docs",
    }
    base.update(overrides)
    return base


@pytest.fixture(scope="module")
def catalogos():
    return cargar_catalogos(DATA_DIR)


class TestCatalogos:
    def test_carga_cursos_servicios_y_blueprint(self, catalogos):
        assert len(catalogos.cursos) == 15
        assert len(catalogos.servicios) >= 38
        assert len(catalogos.subtopicos) >= 60
        assert {s["numero"] for s in catalogos.secciones} == {1, 2, 3, 4}

    def test_pesos_de_secciones_suman_uno(self, catalogos):
        assert sum(s["peso"] for s in catalogos.secciones) == pytest.approx(1.0)


class TestValidarPregunta:
    def test_pregunta_valida_no_tiene_errores(self, catalogos):
        assert validar_pregunta(pregunta_valida(), catalogos) == []

    def test_respuesta_fuera_de_opciones_es_invalida(self, catalogos):
        errores = validar_pregunta(pregunta_valida(respuesta=["E"]), catalogos)
        assert any("respuesta" in e for e in errores)

    def test_tipo_unica_exige_exactamente_una_respuesta(self, catalogos):
        errores = validar_pregunta(pregunta_valida(respuesta=["A", "B"]), catalogos)
        assert any("unica" in e for e in errores)

    def test_tipo_multiple_exige_dos_o_mas_respuestas(self, catalogos):
        errores = validar_pregunta(pregunta_valida(tipo="multiple", respuesta=["A"]), catalogos)
        assert any("multiple" in e for e in errores)

    def test_falta_idioma_es_invalida(self, catalogos):
        pregunta = pregunta_valida(pregunta={"en": "Only English"})
        errores = validar_pregunta(pregunta, catalogos)
        assert any("idioma" in e for e in errores)

    def test_opcion_sin_espanol_es_invalida(self, catalogos):
        pregunta = pregunta_valida()
        pregunta["opciones"][1] = {"en": "A database"}
        errores = validar_pregunta(pregunta, catalogos)
        assert any("idioma" in e for e in errores)

    def test_servicio_fuera_de_catalogo_es_invalido(self, catalogos):
        errores = validar_pregunta(pregunta_valida(servicios=["no-existe"]), catalogos)
        assert any("servicio" in e for e in errores)

    def test_subtopico_fuera_de_blueprint_es_invalido(self, catalogos):
        errores = validar_pregunta(pregunta_valida(subtopicos=["9.9-nada"]), catalogos)
        assert any("subtopico" in e for e in errores)

    def test_curso_fuera_de_catalogo_es_invalido(self, catalogos):
        errores = validar_pregunta(pregunta_valida(curso="curso-fantasma"), catalogos)
        assert any("curso" in e for e in errores)

    def test_curso_nulo_es_valido_para_refuerzo(self, catalogos):
        assert validar_pregunta(pregunta_valida(curso=None), catalogos) == []

    def test_nivel_invalido(self, catalogos):
        errores = validar_pregunta(pregunta_valida(nivel="experto"), catalogos)
        assert any("nivel" in e for e in errores)

    def test_explicacion_obligatoria(self, catalogos):
        errores = validar_pregunta(pregunta_valida(explicacion={"en": "", "es": ""}), catalogos)
        assert any("explicacion" in e for e in errores)

    def test_doc_debe_ser_url_de_google_cloud(self, catalogos):
        errores = validar_pregunta(pregunta_valida(doc="http://example.com"), catalogos)
        assert any("doc" in e for e in errores)


class TestCargarBanco:
    def _escribir_banco(self, tmp_path: Path, preguntas: list[dict]) -> Path:
        """Copia los catálogos reales y escribe un archivo de preguntas de prueba."""
        data_dir = tmp_path / "data"
        (data_dir / "preguntas").mkdir(parents=True)
        for catalogo in ("cursos.json", "servicios.json", "blueprint.json"):
            (data_dir / catalogo).write_text((DATA_DIR / catalogo).read_text())
        archivo = data_dir / "preguntas" / "test.json"
        archivo.write_text(json.dumps({"preguntas": preguntas}))
        return data_dir

    def test_carga_preguntas_validas(self, tmp_path):
        data_dir = self._escribir_banco(tmp_path, [pregunta_valida()])
        banco = cargar_banco(data_dir)
        assert len(banco.preguntas) == 1
        assert banco.excluidas == []

    def test_excluye_invalidas_sin_romper(self, tmp_path):
        rota = pregunta_valida(id="gke-002", respuesta=["Z"])
        data_dir = self._escribir_banco(tmp_path, [pregunta_valida(), rota])
        banco = cargar_banco(data_dir)
        assert len(banco.preguntas) == 1
        assert len(banco.excluidas) == 1
        assert banco.excluidas[0].id == "gke-002"

    def test_ids_duplicados_se_excluyen(self, tmp_path):
        data_dir = self._escribir_banco(tmp_path, [pregunta_valida(), pregunta_valida()])
        banco = cargar_banco(data_dir)
        assert len(banco.preguntas) == 1
        assert len(banco.excluidas) == 1

    def test_indices_por_curso_servicio_nivel_seccion_subtopico(self, tmp_path):
        otra = pregunta_valida(
            id="iam-001",
            curso="infraestructura-conceptos-basicos",
            servicios=["iam"],
            seccion_blueprint=4,
            subtopicos=["4.1-role-types"],
            nivel="avanzado",
        )
        data_dir = self._escribir_banco(tmp_path, [pregunta_valida(), otra])
        banco = cargar_banco(data_dir)
        assert {p["id"] for p in banco.por_curso["como-comenzar-gke"]} == {"gke-001"}
        assert {p["id"] for p in banco.por_servicio["iam"]} == {"iam-001"}
        assert {p["id"] for p in banco.por_nivel["avanzado"]} == {"iam-001"}
        assert {p["id"] for p in banco.por_seccion[2]} == {"gke-001"}
        assert {p["id"] for p in banco.por_subtopico["4.1-role-types"]} == {"iam-001"}
