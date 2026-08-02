"""Selección de estudio por curso o por servicio."""

import reflex as rx

from ..components import ui
from ..components.pregunta import texto_bilingue
from ..components.tarjetas import fila_accion
from ..states.catalog_state import CatalogState
from ..states.lang_state import LangState
from ..states.quiz_state import QuizState
from ..templates.base_layout import base_layout

NIVELES_OPCIONES = ["todos", "principiante", "intermedio", "avanzado"]
ETIQUETA_NIVEL = {
    "todos": "nivel_todos",
    "principiante": "nivel_principiante",
    "intermedio": "nivel_intermedio",
    "avanzado": "nivel_avanzado",
}


def _selector_nivel() -> rx.Component:
    """Chips de filtro M3 en vez de un select: se ven todas las opciones."""
    return rx.el.div(
        rx.el.span(
            LangState.t["nivel"],
            class_name="g-label",
            color="var(--g-on-surface-variant)",
            text_transform="uppercase",
        ),
        ui.cluster(
            *[
                ui.chip(
                    LangState.t[ETIQUETA_NIVEL[nivel]],
                    activo=QuizState.nivel_filtro == nivel,
                    on_click=QuizState.set_nivel_filtro(nivel),
                )
                for nivel in NIVELES_OPCIONES
            ],
            gap="8px",
        ),
        display="flex",
        flex_direction="column",
        gap="8px",
        width="100%",
    )


def _fila_curso(curso: rx.Var) -> rx.Component:
    return fila_accion(
        texto_bilingue(curso["nombre_en"], curso["nombre_es"]),
        curso["disponibles"].to_string() + " " + LangState.t["preguntas"],
        ui.button(
            LangState.t["comenzar"],
            on_click=QuizState.iniciar_por_curso(curso["slug"]),
            disabled=curso["disponibles"] == 0,
            variante="tonal",
        ),
    )


def _fila_servicio(servicio: rx.Var) -> rx.Component:
    return fila_accion(
        texto_bilingue(servicio["nombre_en"], servicio["nombre_es"]),
        servicio["disponibles"].to_string() + " " + LangState.t["preguntas"],
        ui.button(
            LangState.t["comenzar"],
            on_click=QuizState.iniciar_por_servicio(servicio["slug"]),
            disabled=servicio["disponibles"] == 0,
            variante="tonal",
        ),
    )


def _pagina(titulo, filas, plantilla) -> rx.Component:
    return base_layout(
        ui.stack(
            rx.el.div(
                ui.headline(titulo, margin="0"),
                rx.el.p(
                    LangState.t["practicar_desc"],
                    class_name="g-body-sm",
                    color="var(--g-on-surface-variant)",
                    margin="8px 0 0",
                ),
            ),
            _selector_nivel(),
            ui.stack(rx.foreach(filas, plantilla), gap="8px"),
            gap="24px",
        ),
    )


@rx.page(route="/study/course", title="Study by course · Google Cloud ACE Certification Exam")
def estudiar_curso() -> rx.Component:
    return _pagina(LangState.t["por_curso"], CatalogState.cursos, _fila_curso)


@rx.page(route="/study/service", title="Study by service · Google Cloud ACE Certification Exam")
def estudiar_servicio() -> rx.Component:
    return _pagina(LangState.t["por_servicio"], CatalogState.servicios, _fila_servicio)
