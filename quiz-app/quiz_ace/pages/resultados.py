"""Resultado del examen: puntaje, desglose y revisión de falladas."""

import reflex as rx

from ..components import ui
from ..components.pregunta import texto_bilingue
from ..states.exam_state import ExamState
from ..states.lang_state import LangState
from ..templates.base_layout import base_layout


def _panel_puntaje() -> rx.Component:
    """El puntaje contra las dos líneas que importan: el corte y tu meta."""
    return ui.panel(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    ExamState.puntaje,
                    "%",
                    class_name="g-display g-numeral",
                    color=rx.cond(ExamState.aprobado, "var(--g-strong-text)", "var(--g-weak-text)"),
                ),
                rx.el.p(
                    ExamState.correctas,
                    " / ",
                    ExamState.total_resultado,
                    " ",
                    LangState.t["correctas"],
                    class_name="g-body-sm g-numeral",
                    color="var(--g-on-surface-variant)",
                    margin="4px 0 0",
                ),
                display="flex",
                flex_direction="column",
            ),
            ui.state_badge(
                rx.cond(ExamState.aprobado, "fuerte", "debil"),
                rx.cond(ExamState.aprobado, LangState.t["aprobado"], LangState.t["reprobado"]),
            ),
            display="flex",
            align_items="center",
            gap="20px",
            flex_wrap="wrap",
        ),
        rx.el.div(
            ui.meter(
                ExamState.puntaje,
                estado=rx.cond(ExamState.aprobado, "fuerte", "debil"),
            ),
            rx.el.div(
                rx.el.span(
                    LangState.t["meta_aprobacion"],
                    class_name="g-body-sm",
                    color="var(--g-on-surface-variant)",
                ),
                rx.el.span(
                    LangState.t["meta_personal"],
                    class_name="g-body-sm",
                    color="var(--g-on-surface-variant)",
                ),
                display="flex",
                justify_content="space-between",
                gap="12px",
                margin_top="8px",
                flex_wrap="wrap",
            ),
            margin_top="20px",
        ),
    )


def _fila_desglose(fila: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            texto_bilingue(fila["nombre_en"], fila["nombre_es"]),
            class_name="g-body-sm",
            flex="1",
            min_width="0",
        ),
        rx.el.span(
            fila["aciertos"],
            " / ",
            fila["total"],
            class_name="g-body-sm g-numeral",
            color="var(--g-on-surface-variant)",
        ),
        display="flex",
        align_items="center",
        gap="12px",
        padding="10px 0",
        border_bottom="1px solid var(--g-outline-variant)",
    )


def _tabla_desglose(titulo: rx.Var, filas: rx.Var) -> rx.Component:
    return ui.card(
        rx.el.h2(
            titulo,
            class_name="g-title",
            margin="0 0 4px",
        ),
        rx.foreach(filas, _fila_desglose),
        plana=True,
        flex="1",
        min_width="260px",
    )


def _fallada(item: rx.Var) -> rx.Component:
    """Cada fallo trae su explicación: es donde de verdad se aprende."""
    return ui.card(
        rx.el.p(
            texto_bilingue(item["texto_en"], item["texto_es"]),
            class_name="g-title g-measure",
            margin="0 0 12px",
        ),
        ui.cluster(
            rx.el.span(
                LangState.t["tu_respuesta"],
                ": ",
                item["respuesta_dada"],
                class_name="g-state g-state--debil",
            ),
            rx.el.span(
                LangState.t["respuesta_correcta"],
                ": ",
                item["respuesta_correcta"],
                class_name="g-state g-state--fuerte",
            ),
            gap="8px",
        ),
        rx.el.p(
            texto_bilingue(item["explicacion_en"], item["explicacion_es"]),
            class_name="g-body-sm g-measure",
            color="var(--g-on-surface-variant)",
            margin="12px 0 0",
        ),
        rx.link(
            LangState.t["ver_doc"],
            rx.icon(tag="external-link", size=14),
            href=item["doc"],
            is_external=True,
            class_name="g-body-sm",
            color="var(--g-primary)",
            display="inline-flex",
            align_items="center",
            gap="6px",
            margin_top="12px",
        ),
    )


@rx.page(route="/resultados", title="Results · Google Cloud ACE Certification Exam")
def resultados() -> rx.Component:
    return base_layout(
        ui.stack(
            ui.headline(LangState.t["resultado"], margin="0"),
            _panel_puntaje(),
            ui.cluster(
                _tabla_desglose(LangState.t["desglose_seccion"], ExamState.desglose_seccion),
                _tabla_desglose(LangState.t["desglose_servicio"], ExamState.desglose_servicio),
                align_items="flex-start",
                gap="16px",
            ),
            rx.cond(
                ExamState.falladas.length() > 0,
                ui.section(
                    ui.title(LangState.t["revision_falladas"], nivel=2, margin="0"),
                    ui.stack(rx.foreach(ExamState.falladas, _fallada), gap="12px"),
                ),
                rx.fragment(),
            ),
            ui.cluster(
                ui.link_button(LangState.t["nav_dashboard"], href="/dashboard", variante="filled"),
                ui.link_button(LangState.t["volver_inicio"], href="/", variante="outlined"),
            ),
            gap="28px",
        ),
    )
