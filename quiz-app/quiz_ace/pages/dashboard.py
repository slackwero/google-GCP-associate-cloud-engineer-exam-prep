"""Dashboard de avances: evolución, dominio, cobertura y enfoque."""

import reflex as rx

from ..components.pregunta import texto_bilingue
from ..components.tarjetas import badge_estado, stat_card
from ..states.lang_state import LangState
from ..states.progress_state import ProgressState
from ..styles import META_APROBACION, META_PERSONAL
from ..templates.base_layout import base_layout


def _grafica_evolucion() -> rx.Component:
    return rx.box(
        rx.heading(LangState.t["evolucion"], size="4", margin_bottom="2"),
        rx.recharts.line_chart(
            rx.recharts.line(data_key="puntaje", stroke=rx.color("accent", 9), stroke_width=2),
            rx.recharts.reference_line(
                y=META_APROBACION,
                stroke=rx.color("amber", 9),
                stroke_dasharray="4 4",
                label=LangState.t["meta_aprobacion"],
            ),
            rx.recharts.reference_line(
                y=META_PERSONAL,
                stroke=rx.color("green", 9),
                stroke_dasharray="4 4",
                label=LangState.t["meta_personal"],
            ),
            rx.recharts.x_axis(data_key="fecha"),
            rx.recharts.y_axis(domain=[0, 100]),
            rx.recharts.graphing_tooltip(),
            data=ProgressState.evolucion,
            height=280,
            width="100%",
        ),
        width="100%",
    )


def _fila_dominio(fila: rx.Var) -> rx.Component:
    return rx.flex(
        rx.text(texto_bilingue(fila["nombre_en"], fila["nombre_es"]), size="2"),
        rx.spacer(),
        rx.text(fila["pct"], "%", size="2", color=rx.color("gray", 11)),
        badge_estado(
            fila["estado"],
            rx.match(
                fila["estado"],
                ("fuerte", LangState.t["fuerte"]),
                ("medio", LangState.t["medio"]),
                ("debil", LangState.t["debil"]),
                LangState.t["sin_practicar"],
            ),
        ),
        align="center",
        gap="3",
        width="100%",
    )


def _lista_dominio(titulo: rx.Var, filas: rx.Var) -> rx.Component:
    return rx.card(
        rx.heading(titulo, size="3", margin_bottom="2"),
        rx.flex(rx.foreach(filas, _fila_dominio), direction="column", gap="2"),
        width="100%",
    )


def _fila_cobertura(fila: rx.Var) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.text(texto_bilingue(fila["nombre_en"], fila["nombre_es"]), size="2"),
            rx.spacer(),
            rx.text(fila["vistas"], " / ", fila["total"], size="2", color=rx.color("gray", 11)),
            width="100%",
        ),
        rx.progress(value=fila["pct"], width="100%"),
        width="100%",
    )


def _fila_enfoque(fila: rx.Var, indice: rx.Var) -> rx.Component:
    return rx.flex(
        rx.badge(indice + 1, variant="solid"),
        rx.text(texto_bilingue(fila["nombre_en"], fila["nombre_es"]), size="2"),
        rx.spacer(),
        badge_estado(
            fila["estado"],
            rx.match(
                fila["estado"],
                ("fuerte", LangState.t["fuerte"]),
                ("medio", LangState.t["medio"]),
                ("debil", LangState.t["debil"]),
                LangState.t["sin_practicar"],
            ),
        ),
        align="center",
        gap="3",
        width="100%",
    )


@rx.page(route="/dashboard", title="Progress · ACE Quiz", on_load=ProgressState.cargar)
def dashboard() -> rx.Component:
    return base_layout(
        rx.flex(
            rx.heading(LangState.t["dashboard_titulo"], size="7"),
            rx.cond(
                ProgressState.hay_datos,
                rx.flex(
                    rx.grid(
                        stat_card(LangState.t["intentos"], ProgressState.intentos_totales),
                        stat_card(LangState.t["promedio"], rx.text(ProgressState.promedio_examenes, "%")),
                        columns="2",
                        gap="4",
                        width="100%",
                    ),
                    _grafica_evolucion(),
                    rx.card(
                        rx.heading(LangState.t["enfoque_recomendado"], size="3", margin_bottom="2"),
                        rx.flex(
                            rx.foreach(ProgressState.enfoque, _fila_enfoque),
                            direction="column",
                            gap="2",
                        ),
                        width="100%",
                    ),
                    rx.grid(
                        _lista_dominio(LangState.t["dominio_seccion"], ProgressState.dominio_seccion),
                        _lista_dominio(LangState.t["dominio_servicio"], ProgressState.dominio_servicio),
                        columns="2",
                        gap="4",
                        width="100%",
                    ),
                    _lista_dominio(LangState.t["dominio_curso"], ProgressState.dominio_curso),
                    rx.card(
                        rx.heading(LangState.t["cobertura"], size="3", margin_bottom="2"),
                        rx.flex(
                            rx.foreach(ProgressState.cobertura_curso, _fila_cobertura),
                            direction="column",
                            gap="3",
                        ),
                        width="100%",
                    ),
                    direction="column",
                    gap="5",
                    width="100%",
                ),
                rx.center(rx.text(LangState.t["sin_datos"], color=rx.color("gray", 11)), padding_y="9"),
            ),
            direction="column",
            gap="5",
            padding_y="4",
        ),
    )
