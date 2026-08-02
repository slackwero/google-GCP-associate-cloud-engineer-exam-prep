"""Home: elegir modo de estudio o examen."""

import reflex as rx

from ..components.tarjetas import tarjeta_modo
from ..states.catalog_state import CatalogState
from ..states.exam_state import ExamState
from ..states.lang_state import LangState
from ..templates.base_layout import base_layout


def _seccion_estudiar() -> rx.Component:
    return rx.box(
        rx.heading(LangState.t["estudiar"], size="6", margin_bottom="1"),
        rx.text(LangState.t["estudiar_desc"], size="2", color=rx.color("gray", 11), margin_bottom="3"),
        rx.grid(
            tarjeta_modo(
                LangState.t["por_curso"],
                LangState.t["por_curso_desc"],
                rx.link(rx.button(LangState.t["comenzar"], width="100%"), href="/estudiar/curso", width="100%"),
            ),
            tarjeta_modo(
                LangState.t["por_servicio"],
                LangState.t["por_servicio_desc"],
                rx.link(rx.button(LangState.t["comenzar"], width="100%"), href="/estudiar/servicio", width="100%"),
            ),
            columns="2",
            gap="4",
            width="100%",
        ),
        width="100%",
    )


def _seccion_examen() -> rx.Component:
    return rx.box(
        rx.heading(LangState.t["examen"], size="6", margin_bottom="1"),
        rx.text(LangState.t["examen_desc"], size="2", color=rx.color("gray", 11), margin_bottom="3"),
        rx.grid(
            tarjeta_modo(
                LangState.t["examen_corto"],
                LangState.t["examen_corto_desc"],
                rx.button(LangState.t["comenzar"], on_click=ExamState.iniciar("corto"), width="100%"),
            ),
            tarjeta_modo(
                LangState.t["examen_medio"],
                LangState.t["examen_medio_desc"],
                rx.button(LangState.t["comenzar"], on_click=ExamState.iniciar("medio"), width="100%"),
            ),
            tarjeta_modo(
                LangState.t["examen_full"],
                LangState.t["examen_full_desc"],
                rx.button(LangState.t["comenzar"], on_click=ExamState.iniciar("full"), width="100%"),
            ),
            columns="3",
            gap="4",
            width="100%",
        ),
        width="100%",
    )


@rx.page(route="/", title="ACE Quiz")
def index() -> rx.Component:
    return base_layout(
        rx.flex(
            rx.box(
                rx.heading(LangState.t["app_titulo"], size="8"),
                rx.text(LangState.t["app_subtitulo"], size="3", color=rx.color("gray", 11)),
                rx.text(
                    CatalogState.total_preguntas, " ", LangState.t["preguntas_disponibles"],
                    size="2",
                    color=rx.color("gray", 10),
                ),
                margin_bottom="2",
            ),
            _seccion_estudiar(),
            _seccion_examen(),
            direction="column",
            gap="6",
            padding_y="4",
        ),
    )
