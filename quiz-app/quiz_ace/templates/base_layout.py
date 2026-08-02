"""Layout base que envuelve todas las páginas."""

import reflex as rx

from ..components.navbar import navbar
from ..styles import ANCHO_CONTENIDO


def base_layout(*children) -> rx.Component:
    return rx.flex(
        navbar(),
        rx.box(
            *children,
            width="100%",
            max_width=ANCHO_CONTENIDO,
            margin_x="auto",
            padding="5",
        ),
        direction="column",
        min_height="100vh",
    )
