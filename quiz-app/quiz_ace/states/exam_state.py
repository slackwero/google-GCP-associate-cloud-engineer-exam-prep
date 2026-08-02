"""Estado de un examen cronometrado: sin feedback hasta enviar."""

import asyncio
import random

import reflex as rx

from ..models.registro import Intento, Respuesta, ahora
from ..services.db import abrir_sesion
from ..services.muestreo import barajar_opciones, generar_examen
from ..services.puntuacion import calcular_resultado
from .catalog_state import BANCO, CATALOGOS
from .quiz_state import _para_ui

CONFIG_EXAMEN = {
    "corto": {"tamano": 20, "minutos": 25, "ponderado": False},
    "medio": {"tamano": 40, "minutos": 50, "ponderado": False},
    "full": {"tamano": 50, "minutos": 120, "ponderado": True},
}


class ExamState(rx.State):
    """Examen aleatorio con temporizador, navegación libre y marcado."""

    tipo_examen: str = ""
    preguntas: list[dict] = []
    respuestas: dict[str, list[str]] = {}
    marcadas: list[str] = []
    indice: int = 0
    restante_seg: int = 0
    en_curso: bool = False
    intento_id: int = 0

    # Resultado (se llena al enviar)
    puntaje: float = 0.0
    aprobado: bool = False
    correctas: int = 0
    total_resultado: int = 0
    desglose_seccion: list[dict] = []
    desglose_servicio: list[dict] = []
    falladas: list[dict] = []

    @rx.event
    def iniciar(self, tipo: str):
        config = CONFIG_EXAMEN[tipo]
        seleccion = generar_examen(
            BANCO.preguntas,
            tamano=config["tamano"],
            ponderado=config["ponderado"],
            rng=random.Random(),  # noqa: S311
        )
        if not seleccion:
            return rx.toast.warning("No questions available / No hay preguntas disponibles")

        self.tipo_examen = tipo
        self.preguntas = [_para_ui(barajar_opciones(p)) for p in seleccion]
        self.respuestas = {}
        self.marcadas = []
        self.indice = 0
        self.restante_seg = config["minutos"] * 60
        self.en_curso = True
        self.puntaje = 0.0
        self.falladas = []

        with abrir_sesion() as session:
            intento = Intento(modo=f"examen-{tipo}", inicio=ahora(), total=len(self.preguntas))
            session.add(intento)
            session.commit()
            session.refresh(intento)
            self.intento_id = intento.id
        yield rx.redirect("/examen")
        yield ExamState.correr_temporizador

    @rx.event(background=True)
    async def correr_temporizador(self):
        while True:
            await asyncio.sleep(1)
            async with self:
                if not self.en_curso:
                    return
                self.restante_seg -= 1
                if self.restante_seg <= 0:
                    self.restante_seg = 0
                    return ExamState.enviar

    @rx.event
    def alternar_opcion(self, letra: str):
        pregunta = self.pregunta_actual
        actual = self.respuestas.get(pregunta["id"], [])
        if pregunta["tipo"] == "unica":
            nueva = [letra]
        elif letra in actual:
            nueva = [le for le in actual if le != letra]
        else:
            nueva = sorted([*actual, letra])
        self.respuestas = {**self.respuestas, pregunta["id"]: nueva}

    @rx.event
    def ir_a(self, indice: int):
        if 0 <= indice < len(self.preguntas):
            self.indice = indice

    @rx.event
    def alternar_marca(self):
        id_actual = self.pregunta_actual["id"]
        if id_actual in self.marcadas:
            self.marcadas = [m for m in self.marcadas if m != id_actual]
        else:
            self.marcadas = [*self.marcadas, id_actual]

    @rx.event
    def enviar(self):
        if not self.en_curso:
            return
        self.en_curso = False

        banco_por_id = {p["id"]: p for p in BANCO.preguntas}
        preguntas_originales = [banco_por_id[p["id"]] for p in self.preguntas]
        # Remapear letras barajadas de la UI a las letras originales del banco.
        respuestas_originales = {}
        for pregunta_ui in self.preguntas:
            dadas = self.respuestas.get(pregunta_ui["id"], [])
            if not dadas:
                continue
            textos = {o["letra"]: o["en"] for o in pregunta_ui["opciones"]}
            original = banco_por_id[pregunta_ui["id"]]
            letras = "ABCDEFGH"
            texto_a_letra_original = {opcion["en"]: letras[i] for i, opcion in enumerate(original["opciones"])}
            respuestas_originales[pregunta_ui["id"]] = sorted(texto_a_letra_original[textos[le]] for le in dadas)

        resultado = calcular_resultado(preguntas_originales, respuestas_originales)
        self.puntaje = resultado.puntaje
        self.aprobado = resultado.aprobado
        self.correctas = resultado.correctas
        self.total_resultado = resultado.total
        self.desglose_seccion = [
            {
                "nombre_en": seccion["nombre"]["en"],
                "nombre_es": seccion["nombre"]["es"],
                "aciertos": resultado.por_seccion.get(seccion["numero"], (0, 0))[0],
                "total": resultado.por_seccion.get(seccion["numero"], (0, 0))[1],
            }
            for seccion in CATALOGOS.secciones
            if resultado.por_seccion.get(seccion["numero"], (0, 0))[1]
        ]
        self.desglose_servicio = sorted(
            (
                {
                    "nombre_en": CATALOGOS.servicios[slug]["nombre"]["en"],
                    "nombre_es": CATALOGOS.servicios[slug]["nombre"]["es"],
                    "aciertos": aciertos,
                    "total": total,
                }
                for slug, (aciertos, total) in resultado.por_servicio.items()
            ),
            key=lambda fila: fila["total"] - fila["aciertos"],
            reverse=True,
        )
        self.falladas = [
            {
                **_para_ui(fallada["pregunta"]),
                "respuesta_dada": ",".join(fallada["respuesta_dada"]) or "-",
                "respuesta_correcta": ",".join(fallada["pregunta"]["respuesta"]),
            }
            for fallada in resultado.falladas
        ]

        with abrir_sesion() as session:
            intento = session.get(Intento, self.intento_id)
            if intento:
                intento.fin = ahora()
                intento.duracion_seg = int((intento.fin - intento.inicio).total_seconds())
                intento.correctas = resultado.correctas
                intento.puntaje = resultado.puntaje
                intento.completado = True
                session.add(intento)
            for pregunta in preguntas_originales:
                dadas = respuestas_originales.get(pregunta["id"], [])
                session.add(
                    Respuesta(
                        intento_id=self.intento_id,
                        pregunta_id=pregunta["id"],
                        fecha=ahora(),
                        respuesta_dada=",".join(dadas),
                        correcta=bool(dadas) and set(dadas) == set(pregunta["respuesta"]),
                        curso=pregunta.get("curso") or "",
                        servicios=",".join(pregunta["servicios"]),
                        nivel=pregunta["nivel"],
                        seccion=pregunta["seccion_blueprint"],
                        subtopicos=",".join(pregunta["subtopicos"]),
                    )
                )
            session.commit()
        return rx.redirect("/resultados")

    @rx.var
    def pregunta_actual(self) -> dict:
        if not self.preguntas or self.indice >= len(self.preguntas):
            return {"id": "", "tipo": "unica", "texto_en": "", "texto_es": "", "opciones": []}
        return self.preguntas[self.indice]

    @rx.var
    def opciones_actuales(self) -> list[dict]:
        return self.pregunta_actual["opciones"]

    @rx.var
    def seleccion_actual(self) -> list[str]:
        return self.respuestas.get(self.pregunta_actual["id"], [])

    @rx.var
    def tiempo_restante(self) -> str:
        minutos, segundos = divmod(max(self.restante_seg, 0), 60)
        horas, minutos = divmod(minutos, 60)
        if horas:
            return f"{horas}:{minutos:02d}:{segundos:02d}"
        return f"{minutos:02d}:{segundos:02d}"

    @rx.var
    def navegacion(self) -> list[dict]:
        return [
            {
                "indice": i,
                "numero": i + 1,
                "respondida": bool(self.respuestas.get(p["id"])),
                "marcada": p["id"] in self.marcadas,
                "actual": i == self.indice,
            }
            for i, p in enumerate(self.preguntas)
        ]

    @rx.var
    def actual_marcada(self) -> bool:
        return self.pregunta_actual["id"] in self.marcadas

    @rx.var
    def numero_actual(self) -> int:
        return self.indice + 1

    @rx.var
    def total(self) -> int:
        return len(self.preguntas)

    @rx.var
    def respondidas(self) -> int:
        return sum(1 for r in self.respuestas.values() if r)
