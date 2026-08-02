"""Layout base que envuelve todas las páginas."""

import reflex as rx

from ..components.navbar import navbar
from ..styles import ANCHO_CONTENIDO


def _pie() -> rx.Component:
    """Deslinde visible: el proyecto no es oficial ni está afiliado a Google."""
    return rx.el.footer(
        rx.el.p(
            'Not affiliated with Google. "Google Cloud" and "Associate Cloud '
            'Engineer" are trademarks of Google LLC, referenced descriptively.',
            class_name="g-body-sm",
            color="var(--g-on-surface-variant)",
            margin="0",
        ),
        border_top="1px solid var(--g-outline-variant)",
        margin="56px auto 0",
        padding="20px",
        width="100%",
        max_width=ANCHO_CONTENIDO,
    )


def base_layout(*children) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            *children,
            width="100%",
            max_width=ANCHO_CONTENIDO,
            margin="0 auto",
            padding=rx.breakpoints(initial="20px 16px 0", sm="28px 20px 0"),
        ),
        _pie(),
        display="flex",
        flex_direction="column",
        min_height="100vh",
        background="var(--g-background)",
        color="var(--g-on-surface)",
    )
