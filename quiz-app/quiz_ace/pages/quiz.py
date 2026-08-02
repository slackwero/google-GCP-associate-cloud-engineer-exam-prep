"""Sesión de estudio con feedback inmediato."""

import reflex as rx

from ..components.pregunta import boton_opcion, encabezado_pregunta, tarjeta_enunciado, texto_bilingue
from ..states.lang_state import LangState
from ..states.quiz_state import QuizState
from ..templates.base_layout import base_layout


def _feedback() -> rx.Component:
    return rx.cond(
        QuizState.mostrando_feedback,
        rx.box(
            rx.callout(
                rx.cond(QuizState.ultima_correcta, LangState.t["correcto"], LangState.t["incorrecto"]),
                icon=rx.cond(QuizState.ultima_correcta, "check", "x"),
                color_scheme=rx.cond(QuizState.ultima_correcta, "green", "red"),
                width="100%",
            ),
            rx.card(
                rx.text(LangState.t["explicacion"], size="2", weight="bold", margin_bottom="1"),
                rx.text(
                    texto_bilingue(
                        QuizState.pregunta_actual["explicacion_en"],
                        QuizState.pregunta_actual["explicacion_es"],
                    ),
                    size="2",
                ),
                rx.link(
                    LangState.t["ver_doc"],
                    href=QuizState.pregunta_actual["doc"],
                    is_external=True,
                    size="2",
                    margin_top="2",
                ),
                width="100%",
                margin_top="2",
            ),
            width="100%",
        ),
        rx.fragment(),
    )


def _sesion_activa() -> rx.Component:
    return rx.flex(
        encabezado_pregunta(
            QuizState.numero_actual,
            QuizState.total,
            rx.badge(QuizState.puntaje_sesion, size="2"),
        ),
        rx.progress(value=QuizState.progreso, width="100%"),
        tarjeta_enunciado(
            QuizState.pregunta_actual["texto_en"],
            QuizState.pregunta_actual["texto_es"],
            QuizState.pregunta_actual["tipo"],
        ),
        rx.foreach(
            QuizState.opciones_actuales,
            lambda opcion: boton_opcion(
                opcion,
                QuizState.seleccion,
                QuizState.alternar_opcion(opcion["letra"]),
                respuesta_correcta=QuizState.respuesta_actual,
                mostrando_feedback=QuizState.mostrando_feedback,
            ),
        ),
        _feedback(),
        rx.flex(
            rx.button(
                LangState.t["terminar_sesion"],
                on_click=QuizState.terminar,
                variant="soft",
                color_scheme="gray",
            ),
            rx.spacer(),
            rx.cond(
                QuizState.mostrando_feedback,
                rx.button(
                    rx.cond(QuizState.es_ultima, LangState.t["terminar_sesion"], LangState.t["siguiente"]),
                    on_click=QuizState.siguiente,
                ),
                rx.button(
                    LangState.t["responder"],
                    on_click=QuizState.responder,
                    disabled=QuizState.seleccion.length() == 0,
                ),
            ),
            width="100%",
        ),
        direction="column",
        gap="3",
        padding_y="4",
    )


def _sesion_terminada() -> rx.Component:
    return rx.flex(
        rx.heading(LangState.t["sesion_completada"], size="7"),
        rx.heading(QuizState.puntaje_sesion, size="9"),
        rx.flex(
            rx.link(rx.button(LangState.t["volver_inicio"], variant="soft"), href="/"),
            rx.link(rx.button(LangState.t["nav_dashboard"]), href="/dashboard"),
            gap="3",
        ),
        direction="column",
        align="center",
        gap="4",
        padding_y="9",
    )


@rx.page(route="/quiz", title="Study · ACE Quiz")
def quiz() -> rx.Component:
    return base_layout(
        rx.cond(
            QuizState.preguntas.length() == 0,
            rx.center(
                rx.flex(
                    rx.text(LangState.t["sin_preguntas"]),
                    rx.link(rx.button(LangState.t["volver_inicio"]), href="/"),
                    direction="column",
                    align="center",
                    gap="3",
                ),
                padding_y="9",
            ),
            rx.cond(QuizState.terminado, _sesion_terminada(), _sesion_activa()),
        ),
    )
