"""Examen cronometrado con navegación libre y marcado para revisar."""

import reflex as rx

from ..components import ui
from ..components.pregunta import boton_opcion, encabezado_pregunta, tarjeta_enunciado
from ..states.exam_state import ExamState
from ..states.lang_state import LangState
from ..templates.base_layout import base_layout


def _boton_navegacion(item: rx.Var) -> rx.Component:
    return rx.el.button(
        item["numero"],
        on_click=ExamState.ir_a(item["indice"]),
        type="button",
        class_name="g-navdot g-numeral",
        custom_attrs={
            "data-current": rx.cond(item["actual"], "true", "false"),
            "data-answered": rx.cond(item["respondida"], "true", "false"),
            "data-flagged": rx.cond(item["marcada"], "true", "false"),
        },
        aria_current=rx.cond(item["actual"], "true", "false"),
    )


def _barra_superior() -> rx.Component:
    """El tiempo es el dato crítico: se lee de un vistazo y avisa a 5 minutos."""
    apremia = ExamState.restante_seg < 300
    return rx.el.div(
        rx.el.div(
            rx.icon(tag="timer", size=18),
            rx.el.span(ExamState.tiempo_restante, class_name="g-title g-numeral"),
            display="flex",
            align_items="center",
            gap="8px",
            padding="8px 16px",
            border_radius="var(--g-corner-full)",
            background=rx.cond(apremia, "var(--g-weak-container)", "var(--g-surface-container)"),
            color=rx.cond(apremia, "var(--g-on-weak-container)", "var(--g-on-surface)"),
            role="timer",
            aria_live="off",
        ),
        rx.el.div(flex="1"),
        rx.el.span(
            ExamState.respondidas,
            " / ",
            ExamState.total,
            " ",
            LangState.t["respondidas"],
            class_name="g-body-sm g-numeral",
            color="var(--g-on-surface-variant)",
        ),
        display="flex",
        align_items="center",
        gap="12px",
        width="100%",
        flex_wrap="wrap",
    )


def _navegador() -> rx.Component:
    return rx.el.nav(
        rx.el.h2(
            LangState.t["navegador_preguntas"],
            class_name="g-label",
            color="var(--g-on-surface-variant)",
            text_transform="uppercase",
            margin="0 0 10px",
        ),
        rx.el.div(
            rx.foreach(ExamState.navegacion, _boton_navegacion),
            class_name="g-navgrid",
        ),
        aria_label=LangState.t["navegador_preguntas"],
        width="100%",
    )


def _dialogo_enviar() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            ui.button(LangState.t["enviar_examen"], variante="filled"),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title(LangState.t["enviar_examen"]),
            rx.alert_dialog.description(LangState.t["confirmar_envio"]),
            ui.cluster(
                rx.alert_dialog.cancel(
                    ui.button(LangState.t["anterior"], variante="text"),
                ),
                rx.alert_dialog.action(
                    ui.button(
                        LangState.t["enviar_examen"],
                        on_click=ExamState.enviar,
                        variante="filled",
                    ),
                ),
                justify_content="flex-end",
                margin_top="20px",
            ),
        ),
    )


def _sin_preguntas() -> rx.Component:
    return ui.panel(
        rx.el.p(LangState.t["sin_preguntas"], class_name="g-title", margin="0 0 16px"),
        ui.link_button(LangState.t["volver_inicio"], href="/", variante="filled"),
    )


@rx.page(route="/examen", title="Exam · Google Cloud ACE Certification Exam")
def examen() -> rx.Component:
    return base_layout(
        rx.cond(
            ExamState.preguntas.length() == 0,
            _sin_preguntas(),
            ui.stack(
                _barra_superior(),
                _navegador(),
                ui.divider(),
                encabezado_pregunta(
                    ExamState.numero_actual,
                    ExamState.total,
                    ui.chip(
                        rx.cond(ExamState.actual_marcada, LangState.t["marcada"], LangState.t["sin_marcar"]),
                        activo=ExamState.actual_marcada,
                        on_click=ExamState.alternar_marca,
                    ),
                ),
                tarjeta_enunciado(
                    ExamState.pregunta_actual["texto_en"],
                    ExamState.pregunta_actual["texto_es"],
                    ExamState.pregunta_actual["tipo"],
                ),
                ui.stack(
                    rx.foreach(
                        ExamState.opciones_actuales,
                        lambda opcion: boton_opcion(
                            opcion,
                            ExamState.seleccion_actual,
                            ExamState.alternar_opcion(opcion["letra"]),
                        ),
                    ),
                    gap="10px",
                ),
                ui.cluster(
                    ui.button(
                        LangState.t["anterior"],
                        on_click=ExamState.ir_a(ExamState.indice - 1),
                        variante="outlined",
                        disabled=ExamState.indice == 0,
                    ),
                    ui.button(
                        LangState.t["siguiente"],
                        on_click=ExamState.ir_a(ExamState.indice + 1),
                        variante="outlined",
                        disabled=ExamState.indice + 1 >= ExamState.total,
                    ),
                    rx.el.div(flex="1"),
                    _dialogo_enviar(),
                    width="100%",
                    padding_top="4px",
                ),
                gap="20px",
            ),
        ),
    )
