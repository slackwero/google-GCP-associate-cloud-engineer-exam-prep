"""Examen cronometrado con navegación libre y marcado para revisar."""

import reflex as rx

from ..components.pregunta import boton_opcion, encabezado_pregunta, tarjeta_enunciado
from ..states.exam_state import ExamState
from ..states.lang_state import LangState
from ..templates.base_layout import base_layout


def _boton_navegacion(item: rx.Var) -> rx.Component:
    return rx.button(
        item["numero"],
        size="1",
        variant=rx.cond(item["actual"], "solid", rx.cond(item["respondida"], "soft", "outline")),
        color_scheme=rx.cond(item["marcada"], "amber", "blue"),
        on_click=ExamState.ir_a(item["indice"]),
        min_width="36px",
    )


def _barra_superior() -> rx.Component:
    return rx.flex(
        rx.badge(
            LangState.t["tiempo_restante"], ": ", ExamState.tiempo_restante,
            size="2",
            color_scheme=rx.cond(ExamState.restante_seg < 300, "red", "blue"),
        ),
        rx.spacer(),
        rx.text(
            ExamState.respondidas, " / ", ExamState.total,
            size="2",
            color=rx.color("gray", 11),
        ),
        align="center",
        width="100%",
    )


def _dialogo_enviar() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(rx.button(LangState.t["enviar_examen"], color_scheme="green")),
        rx.alert_dialog.content(
            rx.alert_dialog.title(LangState.t["enviar_examen"]),
            rx.alert_dialog.description(LangState.t["confirmar_envio"]),
            rx.flex(
                rx.alert_dialog.cancel(rx.button("Cancel / Cancelar", variant="soft", color_scheme="gray")),
                rx.alert_dialog.action(
                    rx.button(LangState.t["enviar_examen"], color_scheme="green", on_click=ExamState.enviar)
                ),
                gap="3",
                justify="end",
                margin_top="4",
            ),
        ),
    )


@rx.page(route="/examen", title="Exam · ACE Quiz")
def examen() -> rx.Component:
    return base_layout(
        rx.cond(
            ExamState.preguntas.length() == 0,
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
            rx.flex(
                _barra_superior(),
                rx.flex(rx.foreach(ExamState.navegacion, _boton_navegacion), wrap="wrap", gap="1", width="100%"),
                encabezado_pregunta(
                    ExamState.numero_actual,
                    ExamState.total,
                    rx.button(
                        rx.cond(ExamState.actual_marcada, LangState.t["marcada"], LangState.t["marcar_revision"]),
                        on_click=ExamState.alternar_marca,
                        variant=rx.cond(ExamState.actual_marcada, "solid", "outline"),
                        color_scheme="amber",
                        size="1",
                    ),
                ),
                tarjeta_enunciado(
                    ExamState.pregunta_actual["texto_en"],
                    ExamState.pregunta_actual["texto_es"],
                    ExamState.pregunta_actual["tipo"],
                ),
                rx.foreach(
                    ExamState.opciones_actuales,
                    lambda opcion: boton_opcion(
                        opcion,
                        ExamState.seleccion_actual,
                        ExamState.alternar_opcion(opcion["letra"]),
                    ),
                ),
                rx.flex(
                    rx.button(
                        LangState.t["anterior"],
                        on_click=ExamState.ir_a(ExamState.indice - 1),
                        variant="soft",
                        disabled=ExamState.indice == 0,
                    ),
                    rx.button(
                        LangState.t["siguiente"],
                        on_click=ExamState.ir_a(ExamState.indice + 1),
                        variant="soft",
                        disabled=ExamState.indice + 1 >= ExamState.total,
                    ),
                    rx.spacer(),
                    _dialogo_enviar(),
                    width="100%",
                    gap="3",
                ),
                direction="column",
                gap="3",
                padding_y="4",
            ),
        ),
    )
