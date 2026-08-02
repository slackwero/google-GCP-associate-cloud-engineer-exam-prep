"""Barra de navegación con selector de idioma siempre visible."""

import reflex as rx

from ..states.lang_state import LangState


def _boton_idioma(codigo: str, etiqueta: str) -> rx.Component:
    return rx.button(
        etiqueta,
        size="1",
        variant=rx.cond(LangState.idioma_activo == codigo, "solid", "soft"),
        on_click=LangState.cambiar_idioma(codigo),
    )


def navbar() -> rx.Component:
    return rx.flex(
        rx.link(
            rx.heading(LangState.t["app_titulo"], size="5"),
            href="/",
            underline="none",
            color=rx.color("gray", 12),
        ),
        rx.spacer(),
        rx.hstack(
            rx.link(LangState.t["nav_inicio"], href="/", size="2"),
            rx.link(LangState.t["nav_dashboard"], href="/dashboard", size="2"),
            rx.separator(orientation="vertical", size="1"),
            _boton_idioma("en", "EN"),
            _boton_idioma("es", "ES"),
            rx.color_mode.button(size="1"),
            align="center",
            gap="3",
        ),
        align="center",
        width="100%",
        padding_x="5",
        padding_y="3",
        border_bottom=f"1px solid {rx.color('gray', 5)}",
    )
