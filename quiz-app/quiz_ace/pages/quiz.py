"""Sesión de estudio con feedback inmediato."""

import reflex as rx

from ..components import ui
from ..components.pregunta import boton_opcion, encabezado_pregunta, tarjeta_enunciado, texto_bilingue
from ..components.tarjetas import cifra
from ..states.lang_state import LangState
from ..states.quiz_state import QuizState
from ..templates.base_layout import base_layout


def _veredicto() -> rx.Component:
    """Correcto o incorrecto, en el trío semántico y con icono, no solo color."""
    return rx.el.div(
        rx.icon(
            tag=rx.cond(QuizState.ultima_correcta, "check", "x"),
            size=18,
        ),
        rx.el.span(
            rx.cond(QuizState.ultima_correcta, LangState.t["correcto"], LangState.t["incorrecto"]),
            class_name="g-title",
        ),
        display="flex",
        align_items="center",
        gap="8px",
        padding="10px 16px",
        border_radius="var(--g-corner-md)",
        background=rx.cond(
            QuizState.ultima_correcta,
            "var(--g-strong-container)",
            "var(--g-weak-container)",
        ),
        color=rx.cond(
            QuizState.ultima_correcta,
            "var(--g-on-strong-container)",
            "var(--g-on-weak-container)",
        ),
        role="status",
    )


def _explicacion() -> rx.Component:
    """Por qué la correcta es correcta y por qué falla cada distractor."""
    return ui.card(
        rx.el.h3(
            LangState.t["explicacion"],
            class_name="g-label",
            color="var(--g-on-surface-variant)",
            text_transform="uppercase",
            margin="0 0 8px",
        ),
        rx.el.p(
            texto_bilingue(
                QuizState.pregunta_actual["explicacion_en"],
                QuizState.pregunta_actual["explicacion_es"],
            ),
            class_name="g-body-sm g-measure",
            margin="0",
        ),
        rx.link(
            LangState.t["ver_doc"],
            rx.icon(tag="external-link", size=14),
            href=QuizState.pregunta_actual["doc"],
            is_external=True,
            class_name="g-body-sm",
            color="var(--g-primary)",
            display="inline-flex",
            align_items="center",
            gap="6px",
            margin_top="12px",
        ),
    )


def _feedback() -> rx.Component:
    return rx.cond(
        QuizState.mostrando_feedback,
        ui.stack(_veredicto(), _explicacion(), gap="12px"),
        rx.fragment(),
    )


def _sesion_activa() -> rx.Component:
    return ui.stack(
        encabezado_pregunta(
            QuizState.numero_actual,
            QuizState.total,
            rx.el.span(
                QuizState.puntaje_sesion,
                class_name="g-body-sm g-numeral",
                color="var(--g-on-surface-variant)",
            ),
        ),
        ui.meter(QuizState.progreso, estado="brand"),
        tarjeta_enunciado(
            QuizState.pregunta_actual["texto_en"],
            QuizState.pregunta_actual["texto_es"],
            QuizState.pregunta_actual["tipo"],
        ),
        ui.stack(
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
            gap="10px",
        ),
        _feedback(),
        ui.cluster(
            ui.button(
                LangState.t["terminar_sesion"],
                on_click=QuizState.terminar,
                variante="text",
            ),
            rx.el.div(flex="1"),
            rx.cond(
                QuizState.mostrando_feedback,
                ui.button(
                    rx.cond(QuizState.es_ultima, LangState.t["terminar_sesion"], LangState.t["siguiente"]),
                    on_click=QuizState.siguiente,
                    variante="filled",
                ),
                ui.button(
                    LangState.t["responder"],
                    on_click=QuizState.responder,
                    disabled=QuizState.seleccion.length() == 0,
                    variante="filled",
                ),
            ),
            width="100%",
            padding_top="4px",
        ),
        gap="20px",
    )


def _sesion_terminada() -> rx.Component:
    return ui.panel(
        ui.title(LangState.t["sesion_completada"], nivel=2, margin="0"),
        rx.el.div(
            cifra(QuizState.puntaje_sesion, LangState.t["aciertos"], tono="brand"),
            margin="16px 0 20px",
        ),
        ui.cluster(
            ui.link_button(LangState.t["nav_dashboard"], href="/dashboard", variante="filled"),
            ui.link_button(LangState.t["volver_inicio"], href="/", variante="outlined"),
        ),
    )


def _sin_preguntas() -> rx.Component:
    return ui.panel(
        rx.el.p(LangState.t["sin_preguntas"], class_name="g-title", margin="0 0 16px"),
        ui.link_button(LangState.t["volver_inicio"], href="/", variante="filled"),
    )


@rx.page(route="/quiz", title="Study · Google Cloud ACE Certification Exam")
def quiz() -> rx.Component:
    return base_layout(
        rx.cond(
            QuizState.preguntas.length() == 0,
            _sin_preguntas(),
            rx.cond(QuizState.terminado, _sesion_terminada(), _sesion_activa()),
        ),
    )
