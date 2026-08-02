"""Estado del dashboard: historial, dominio, cobertura y enfoque."""

import reflex as rx
from sqlmodel import select

from ..models.registro import Intento, Respuesta, ahora
from ..services.db import abrir_sesion
from ..services.estadisticas import calcular_cobertura, calcular_dominio, calcular_enfoque
from ..services.historial import borrar_incompletos, borrar_todo, contar_historial
from .catalog_state import BANCO, CATALOGOS

PESOS_SECCION = {s["numero"]: s["peso"] for s in CATALOGOS.secciones}


def _nombre(catalogo: dict, clave: str) -> dict:
    # Las preguntas de refuerzo no pertenecen a ningún curso del path.
    if clave == "":
        return {"en": "Blueprint reinforcement", "es": "Refuerzo del blueprint"}
    entrada = catalogo.get(clave)
    return entrada["nombre"] if entrada else {"en": str(clave), "es": str(clave)}


class ProgressState(rx.State):
    """Agrega el historial persistido para el dashboard de avances."""

    intentos_totales: int = 0
    promedio_examenes: float = 0.0
    evolucion: list[dict] = []
    dominio_seccion: list[dict] = []
    dominio_servicio: list[dict] = []
    dominio_curso: list[dict] = []
    cobertura_curso: list[dict] = []
    enfoque: list[dict] = []
    hay_datos: bool = False

    # Actual scope of each deletion. `intentos_totales` above is the KPI and only
    # counts finished attempts; these count everything stored in the database.
    historial_intentos: int = 0
    historial_incompletos: int = 0
    historial_respuestas: int = 0
    historial_respuestas_incompletas: int = 0

    # Indexar una lista de dicts dentro de un componente devuelve Any, así que
    # el foco recomendado se expone como vars tipadas para la home.
    @rx.var
    def tiene_foco(self) -> bool:
        return bool(self.enfoque)

    @rx.var
    def foco_nombre_en(self) -> str:
        return self.enfoque[0]["nombre_en"] if self.enfoque else ""

    @rx.var
    def foco_nombre_es(self) -> str:
        return self.enfoque[0]["nombre_es"] if self.enfoque else ""

    @rx.var
    def foco_estado(self) -> str:
        return self.enfoque[0]["estado"] if self.enfoque else "sin_datos"

    @rx.event
    def cargar(self):
        with abrir_sesion() as session:
            intentos = session.exec(select(Intento).where(Intento.completado == True)).all()  # noqa: E712
            filas = session.exec(select(Respuesta)).all()
            conteo = contar_historial(session)

        self.historial_intentos = conteo["intentos"]
        self.historial_incompletos = conteo["intentos_incompletos"]
        self.historial_respuestas = conteo["respuestas"]
        self.historial_respuestas_incompletas = conteo["respuestas_incompletas"]

        respuestas = [
            {
                "pregunta_id": r.pregunta_id,
                "correcta": r.correcta,
                "fecha": r.fecha,
                "curso": r.curso,
                "servicios": r.servicios,
                "seccion": r.seccion,
                "subtopicos": r.subtopicos,
            }
            for r in filas
        ]
        self.hay_datos = bool(respuestas)
        self.intentos_totales = len(intentos)

        examenes = [i for i in intentos if i.modo.startswith("examen")]
        self.promedio_examenes = round(sum(i.puntaje for i in examenes) / len(examenes), 1) if examenes else 0.0

        self.evolucion = [
            {
                "fecha": intento.fin.strftime("%d/%m %H:%M") if intento.fin else "",
                "puntaje": intento.puntaje,
                "modo": intento.modo,
            }
            for intento in sorted(intentos, key=lambda i: i.inicio)
        ]

        momento = ahora()
        self.dominio_seccion = self._con_nombres_seccion(calcular_dominio(respuestas, "seccion", momento))
        self.dominio_servicio = self._con_nombres(
            calcular_dominio(respuestas, "servicios", momento), CATALOGOS.servicios
        )
        self.dominio_curso = self._con_nombres(calcular_dominio(respuestas, "curso", momento), CATALOGOS.cursos)

        banco_por_curso = {slug: [p["id"] for p in pgs] for slug, pgs in BANCO.por_curso.items()}
        cobertura_curso = calcular_cobertura(respuestas, banco_por_curso, campo="curso")
        self.cobertura_curso = [
            {
                "nombre_en": _nombre(CATALOGOS.cursos, slug)["en"],
                "nombre_es": _nombre(CATALOGOS.cursos, slug)["es"],
                **datos,
            }
            for slug, datos in sorted(cobertura_curso.items(), key=lambda kv: kv[1]["pct"])
        ]

        banco_por_seccion = {n: [p["id"] for p in pgs] for n, pgs in BANCO.por_seccion.items()}
        dominio_secciones = calcular_dominio(respuestas, "seccion", momento)
        cobertura_secciones = calcular_cobertura(respuestas, banco_por_seccion, campo="seccion")
        self.enfoque = [
            {
                "nombre_en": _nombre({s["numero"]: s for s in CATALOGOS.secciones}, e["clave"])["en"],
                "nombre_es": _nombre({s["numero"]: s for s in CATALOGOS.secciones}, e["clave"])["es"],
                "estado": e["estado"],
                "dominio": e["dominio_pct"] if e["dominio_pct"] is not None else -1.0,
                "cobertura": e["cobertura_pct"],
            }
            for e in calcular_enfoque(dominio_secciones, cobertura_secciones, PESOS_SECCION)
        ]

    @rx.event
    def resetear_todo(self):
        """Wipe the history and reload: the page falls back to its empty state."""
        with abrir_sesion() as session:
            borrar_todo(session)
        self.cargar()

    @rx.event
    def limpiar_incompletos(self):
        """Drop abandoned attempts and keep the ones that were finished."""
        with abrir_sesion() as session:
            borrar_incompletos(session)
        self.cargar()

    def _con_nombres_seccion(self, dominio: dict) -> list[dict]:
        secciones = {s["numero"]: s for s in CATALOGOS.secciones}
        return [
            {
                "nombre_en": f"S{clave}: {_nombre(secciones, clave)['en']}",
                "nombre_es": f"S{clave}: {_nombre(secciones, clave)['es']}",
                "pct": datos["pct"],
                "estado": datos["estado"],
            }
            for clave, datos in sorted(dominio.items())
        ]

    def _con_nombres(self, dominio: dict, catalogo: dict) -> list[dict]:
        return sorted(
            (
                {
                    "nombre_en": _nombre(catalogo, clave)["en"],
                    "nombre_es": _nombre(catalogo, clave)["es"],
                    "pct": datos["pct"],
                    "estado": datos["estado"],
                }
                for clave, datos in dominio.items()
            ),
            key=lambda fila: fila["pct"],
        )
