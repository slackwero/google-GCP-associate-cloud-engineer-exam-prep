"""Resultado del examen: puntaje, desglose y revisión de falladas."""

import reflex as rx

from ..components.pregunta import texto_bilingue
from ..states.exam_state import ExamState
from ..states.lang_state import LangState
from ..templates.base_layout import base_layout


def _hero_puntaje() -> rx.Component:
    return rx.flex(
        rx.heading(LangState.t["resultado"], size="6", color=rx.color("gray", 11)),
        rx.heading(ExamState.puntaje, "%", size="9"),
        rx.badge(
            rx.cond(ExamState.aprobado, LangState.t["aprobado"], LangState.t["reprobado"]),
            color_scheme=rx.cond(ExamState.aprobado, "green", "red"),
            size="3",
        ),
        rx.text(
            ExamState.correctas, " / ", ExamState.total_resultado, " ", LangState.t["correctas"],
            size="3",
            color=rx.color("gray", 11),
        ),
        direction="column",
        align="center",
        gap="2",
    )


def _fila_desglose(fila: rx.Var) -> rx.Component:
    return rx.table.row(
        rx.table.cell(texto_bilingue(fila["nombre_en"], fila["nombre_es"])),
        rx.table.cell(fila["aciertos"], " / ", fila["total"]),
    )


def _tabla_desglose(titulo: rx.Var, filas: rx.Var) -> rx.Component:
    return rx.box(
        rx.heading(titulo, size="4", margin_bottom="2"),
        rx.table.root(rx.table.body(rx.foreach(filas, _fila_desglose)), width="100%"),
        width="100%",
    )


def _fallada(item: rx.Var) -> rx.Component:
    return rx.card(
        rx.text(texto_bilingue(item["texto_en"], item["texto_es"]), weight="medium", size="3"),
        rx.flex(
            rx.badge(LangState.t["tu_respuesta"], ": ", item["respuesta_dada"], color_scheme="red"),
            rx.badge(LangState.t["respuesta_correcta"], ": ", item["respuesta_correcta"], color_scheme="green"),
            gap="3",
            margin_y="2",
        ),
        rx.text(
            texto_bilingue(item["explicacion_en"], item["explicacion_es"]),
            size="2",
            color=rx.color("gray", 11),
        ),
        rx.link(LangState.t["ver_doc"], href=item["doc"], is_external=True, size="2"),
        width="100%",
    )


@rx.page(route="/resultados", title="Results · ACE Quiz")
def resultados() -> rx.Component:
    return base_layout(
        rx.flex(
            _hero_puntaje(),
            rx.grid(
                _tabla_desglose(LangState.t["desglose_seccion"], ExamState.desglose_seccion),
                _tabla_desglose(LangState.t["desglose_servicio"], ExamState.desglose_servicio),
                columns="2",
                gap="5",
                width="100%",
            ),
            rx.cond(
                ExamState.falladas.length() > 0,
                rx.box(
                    rx.heading(LangState.t["revision_falladas"], size="4", margin_bottom="2"),
                    rx.flex(rx.foreach(ExamState.falladas, _fallada), direction="column", gap="3"),
                    width="100%",
                ),
                rx.fragment(),
            ),
            rx.flex(
                rx.link(rx.button(LangState.t["volver_inicio"], variant="soft"), href="/"),
                rx.link(rx.button(LangState.t["nav_dashboard"]), href="/dashboard"),
                gap="3",
                justify="center",
            ),
            direction="column",
            gap="6",
            padding_y="5",
        ),
    )
