"""Corrección de respuestas y cálculo de resultados con desglose."""

from collections import defaultdict
from dataclasses import dataclass, field

UMBRAL_APROBACION = 70.0


@dataclass
class Resultado:
    correctas: int = 0
    total: int = 0
    puntaje: float = 0.0
    aprobado: bool = False
    por_seccion: dict[int, tuple[int, int]] = field(default_factory=dict)
    por_servicio: dict[str, tuple[int, int]] = field(default_factory=dict)
    por_subtopico: dict[str, tuple[int, int]] = field(default_factory=dict)
    falladas: list[dict] = field(default_factory=list)


def es_correcta(pregunta: dict, respuesta_dada: list[str]) -> bool:
    """Una respuesta es correcta solo si coincide el conjunto exacto de letras."""
    return bool(respuesta_dada) and set(respuesta_dada) == set(pregunta["respuesta"])


def calcular_resultado(preguntas: list[dict], respuestas: dict[str, list[str]]) -> Resultado:
    """Califica un intento completo; las preguntas sin responder cuentan como incorrectas."""
    resultado = Resultado(total=len(preguntas))
    seccion = defaultdict(lambda: [0, 0])
    servicio = defaultdict(lambda: [0, 0])
    subtopico = defaultdict(lambda: [0, 0])

    for pregunta in preguntas:
        respuesta_dada = respuestas.get(pregunta["id"], [])
        acierto = es_correcta(pregunta, respuesta_dada)
        if acierto:
            resultado.correctas += 1
        else:
            resultado.falladas.append({"pregunta": pregunta, "respuesta_dada": respuesta_dada})

        _acumular(seccion[pregunta["seccion_blueprint"]], acierto)
        for s in pregunta["servicios"]:
            _acumular(servicio[s], acierto)
        for s in pregunta["subtopicos"]:
            _acumular(subtopico[s], acierto)

    resultado.puntaje = round(resultado.correctas * 100 / resultado.total, 1) if resultado.total else 0.0
    resultado.aprobado = resultado.puntaje >= UMBRAL_APROBACION
    resultado.por_seccion = {k: tuple(v) for k, v in seccion.items()}
    resultado.por_servicio = {k: tuple(v) for k, v in servicio.items()}
    resultado.por_subtopico = {k: tuple(v) for k, v in subtopico.items()}
    return resultado


def _acumular(contador: list[int], acierto: bool) -> None:
    contador[0] += int(acierto)
    contador[1] += 1
