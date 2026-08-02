"""Estado de una sesión de estudio: feedback inmediato pregunta a pregunta."""

import random

import reflex as rx

from ..models.registro import Intento, Respuesta, ahora
from ..services.db import abrir_sesion
from ..services.muestreo import barajar_opciones, seleccionar_estudio
from ..services.puntuacion import es_correcta
from .catalog_state import BANCO

LIMITE_SESION_ESTUDIO = 20


def _para_ui(pregunta: dict) -> dict:
    """Aplana una pregunta del banco al formato que consume la UI."""
    letras = "ABCDEFGH"
    return {
        "id": pregunta["id"],
        "tipo": pregunta["tipo"],
        "texto_en": pregunta["pregunta"]["en"],
        "texto_es": pregunta["pregunta"]["es"],
        "opciones": [
            {"letra": letras[i], "en": opcion["en"], "es": opcion["es"]}
            for i, opcion in enumerate(pregunta["opciones"])
        ],
        "respuesta": pregunta["respuesta"],
        "explicacion_en": pregunta["explicacion"]["en"],
        "explicacion_es": pregunta["explicacion"]["es"],
        "doc": pregunta["doc"],
        "curso": pregunta.get("curso") or "",
        "servicios": ",".join(pregunta["servicios"]),
        "nivel": pregunta["nivel"],
        "seccion": pregunta["seccion_blueprint"],
        "subtopicos": ",".join(pregunta["subtopicos"]),
    }


class QuizState(rx.State):
    """Sesión de estudio con feedback inmediato."""

    modo: str = ""
    filtro: str = ""
    preguntas: list[dict] = []
    indice: int = 0
    seleccion: list[str] = []
    mostrando_feedback: bool = False
    ultima_correcta: bool = False
    correctas: int = 0
    terminado: bool = False
    nivel_filtro: str = "todos"
    intento_id: int = 0

    @rx.event
    def set_nivel_filtro(self, nivel: str):
        self.nivel_filtro = nivel

    @rx.event
    def iniciar_por_curso(self, curso: str):
        return self._iniciar("estudio-curso", curso=curso)

    @rx.event
    def iniciar_por_servicio(self, servicio: str):
        return self._iniciar("estudio-servicio", servicio=servicio)

    def _iniciar(self, modo: str, curso: str | None = None, servicio: str | None = None):
        nivel = None if self.nivel_filtro == "todos" else self.nivel_filtro
        seleccion = seleccionar_estudio(
            BANCO.preguntas,
            curso=curso,
            servicio=servicio,
            nivel=nivel,
            limite=LIMITE_SESION_ESTUDIO,
            rng=random.Random(),  # noqa: S311
        )
        if not seleccion:
            return rx.toast.warning("No questions available / No hay preguntas disponibles")

        self.modo = modo
        self.filtro = ":".join(filter(None, [curso or servicio, nivel]))
        self.preguntas = [_para_ui(barajar_opciones(p)) for p in seleccion]
        self.indice = 0
        self.seleccion = []
        self.mostrando_feedback = False
        self.correctas = 0
        self.terminado = False

        with abrir_sesion() as session:
            intento = Intento(modo=self.modo, filtro=self.filtro, inicio=ahora(), total=len(self.preguntas))
            session.add(intento)
            session.commit()
            session.refresh(intento)
            self.intento_id = intento.id
        return rx.redirect("/quiz")

    @rx.event
    def alternar_opcion(self, letra: str):
        if self.mostrando_feedback:
            return
        if self.pregunta_actual["tipo"] == "unica":
            self.seleccion = [letra]
        elif letra in self.seleccion:
            self.seleccion = [le for le in self.seleccion if le != letra]
        else:
            self.seleccion = sorted([*self.seleccion, letra])

    @rx.event
    def responder(self):
        if not self.seleccion or self.mostrando_feedback:
            return
        pregunta = self.preguntas[self.indice]
        self.ultima_correcta = es_correcta({"respuesta": pregunta["respuesta"]}, self.seleccion)
        if self.ultima_correcta:
            self.correctas += 1
        self.mostrando_feedback = True

        with abrir_sesion() as session:
            session.add(
                Respuesta(
                    intento_id=self.intento_id,
                    pregunta_id=pregunta["id"],
                    fecha=ahora(),
                    respuesta_dada=",".join(self.seleccion),
                    correcta=self.ultima_correcta,
                    curso=pregunta["curso"],
                    servicios=pregunta["servicios"],
                    nivel=pregunta["nivel"],
                    seccion=pregunta["seccion"],
                    subtopicos=pregunta["subtopicos"],
                )
            )
            session.commit()

    @rx.event
    def siguiente(self):
        if not self.mostrando_feedback:
            return
        if self.indice + 1 >= len(self.preguntas):
            return QuizState.terminar
        self.indice += 1
        self.seleccion = []
        self.mostrando_feedback = False

    @rx.event
    def terminar(self):
        self.terminado = True
        respondidas = self.indice + (1 if self.mostrando_feedback else 0)
        with abrir_sesion() as session:
            intento = session.get(Intento, self.intento_id)
            if intento:
                intento.fin = ahora()
                intento.duracion_seg = int((intento.fin - intento.inicio).total_seconds())
                intento.correctas = self.correctas
                intento.total = respondidas or len(self.preguntas)
                intento.puntaje = round(self.correctas * 100 / intento.total, 1) if intento.total else 0.0
                intento.completado = respondidas >= len(self.preguntas)
                session.add(intento)
                session.commit()

    @rx.var
    def pregunta_actual(self) -> dict:
        if not self.preguntas or self.indice >= len(self.preguntas):
            return {"id": "", "tipo": "unica", "texto_en": "", "texto_es": "", "opciones": [], "respuesta": [],
                    "explicacion_en": "", "explicacion_es": "", "doc": "", "curso": "", "servicios": "",
                    "nivel": "", "seccion": 0, "subtopicos": ""}
        return self.preguntas[self.indice]

    @rx.var
    def opciones_actuales(self) -> list[dict]:
        return self.pregunta_actual["opciones"]

    @rx.var
    def respuesta_actual(self) -> list[str]:
        return self.pregunta_actual["respuesta"]

    @rx.var
    def progreso(self) -> int:
        if not self.preguntas:
            return 0
        return round((self.indice + (1 if self.mostrando_feedback else 0)) * 100 / len(self.preguntas))

    @rx.var
    def numero_actual(self) -> int:
        return self.indice + 1

    @rx.var
    def total(self) -> int:
        return len(self.preguntas)

    @rx.var
    def es_ultima(self) -> bool:
        return self.indice + 1 >= len(self.preguntas)

    @rx.var
    def puntaje_sesion(self) -> str:
        respondidas = self.indice + (1 if self.mostrando_feedback else 0)
        return f"{self.correctas}/{respondidas}" if respondidas else "0/0"
