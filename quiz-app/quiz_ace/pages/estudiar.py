"""Selección de estudio por curso o por servicio."""

import reflex as rx

from ..components.pregunta import texto_bilingue
from ..states.catalog_state import CatalogState
from ..states.lang_state import LangState
from ..states.quiz_state import QuizState
from ..templates.base_layout import base_layout

NIVELES_OPCIONES = ["todos", "principiante", "intermedio", "avanzado"]


def _selector_nivel() -> rx.Component:
    return rx.flex(
        rx.text(LangState.t["nivel"], size="2", weight="medium"),
        rx.select(
            NIVELES_OPCIONES,
            value=QuizState.nivel_filtro,
            on_change=QuizState.set_nivel_filtro,
            size="2",
        ),
        align="center",
        gap="3",
    )


def _fila_curso(curso: rx.Var) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.box(
                rx.text(texto_bilingue(curso["nombre_en"], curso["nombre_es"]), size="3", weight="medium"),
                rx.text(
                    curso["disponibles"], " ", LangState.t["preguntas_disponibles"],
                    size="1",
                    color=rx.color("gray", 10),
                ),
            ),
            rx.spacer(),
            rx.button(
                LangState.t["comenzar"],
                on_click=QuizState.iniciar_por_curso(curso["slug"]),
                disabled=curso["disponibles"] == 0,
            ),
            align="center",
            width="100%",
            gap="3",
        ),
        width="100%",
    )


def _fila_servicio(servicio: rx.Var) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.box(
                rx.text(texto_bilingue(servicio["nombre_en"], servicio["nombre_es"]), size="3", weight="medium"),
                rx.text(
                    servicio["disponibles"], " ", LangState.t["preguntas_disponibles"],
                    size="1",
                    color=rx.color("gray", 10),
                ),
            ),
            rx.spacer(),
            rx.button(LangState.t["comenzar"], on_click=QuizState.iniciar_por_servicio(servicio["slug"])),
            align="center",
            width="100%",
            gap="3",
        ),
        width="100%",
    )


@rx.page(route="/estudiar/curso", title="Study by course · ACE Quiz")
def estudiar_curso() -> rx.Component:
    return base_layout(
        rx.flex(
            rx.heading(LangState.t["por_curso"], size="7"),
            _selector_nivel(),
            rx.foreach(CatalogState.cursos, _fila_curso),
            direction="column",
            gap="3",
            padding_y="4",
        ),
    )


@rx.page(route="/estudiar/servicio", title="Study by service · ACE Quiz")
def estudiar_servicio() -> rx.Component:
    return base_layout(
        rx.flex(
            rx.heading(LangState.t["por_servicio"], size="7"),
            _selector_nivel(),
            rx.foreach(CatalogState.servicios, _fila_servicio),
            direction="column",
            gap="3",
            padding_y="4",
        ),
    )
