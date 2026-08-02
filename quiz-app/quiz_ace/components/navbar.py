"""Barra de aplicación: marca, navegación, idioma y tema."""

import reflex as rx

from ..states.lang_state import LangState
from ..styles import ANCHO_CONTENIDO
from . import ui


def _marca() -> rx.Component:
    """Cuatro puntos en la paleta de Google. Geometría propia, no su logotipo."""
    return rx.el.span(
        rx.el.span(),
        rx.el.span(),
        rx.el.span(),
        rx.el.span(),
        class_name="g-mark",
        aria_hidden="true",
    )


def _enlace_nav(texto, href: str) -> rx.Component:
    return rx.link(
        texto,
        href=href,
        class_name="g-body-sm",
        color="var(--g-on-surface-variant)",
        text_decoration="none",
        padding="8px 12px",
        border_radius="var(--g-corner-sm)",
        _hover={"background": "var(--g-surface-container)", "color": "var(--g-on-surface)"},
    )


def _selector_idioma() -> rx.Component:
    return rx.el.div(
        ui.chip(
            "EN",
            activo=LangState.idioma_activo == "en",
            on_click=LangState.cambiar_idioma("en"),
            style={"border_top_right_radius": "0", "border_bottom_right_radius": "0"},
        ),
        ui.chip(
            "ES",
            activo=LangState.idioma_activo == "es",
            on_click=LangState.cambiar_idioma("es"),
            style={
                "border_top_left_radius": "0",
                "border_bottom_left_radius": "0",
                "margin_left": "-1px",
            },
        ),
        display="flex",
        role="group",
        aria_label="Language / Idioma",
    )


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.link(
                _marca(),
                rx.el.span(
                    LangState.t["app_titulo"],
                    class_name="g-title",
                    color="var(--g-on-surface)",
                    white_space="nowrap",
                    # En pantallas muy angostas el nombre cede el paso a la
                    # navegación; la marca de cuatro puntos sigue visible.
                    display=rx.breakpoints(initial="none", xs="inline"),
                ),
                href="/",
                display="flex",
                align_items="center",
                gap="10px",
                text_decoration="none",
            ),
            rx.el.div(flex="1"),
            rx.el.nav(
                _enlace_nav(LangState.t["nav_inicio"], "/"),
                _enlace_nav(LangState.t["nav_dashboard"], "/dashboard"),
                display="flex",
                align_items="center",
                gap="4px",
                aria_label=LangState.t["nav_inicio"],
            ),
            _selector_idioma(),
            ui.icon_button(
                rx.color_mode_cond(light="moon", dark="sun"),
                etiqueta="Theme / Tema",
                on_click=rx.toggle_color_mode,
            ),
            display="flex",
            align_items="center",
            gap="12px",
            width="100%",
            max_width=ANCHO_CONTENIDO,
            margin="0 auto",
            padding="10px 20px",
        ),
        class_name="g-appbar",
    )
