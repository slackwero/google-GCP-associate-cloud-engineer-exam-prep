"""Piezas compuestas que se repiten entre páginas."""

import reflex as rx

from ..states.lang_state import LangState
from . import ui


def badge_estado(estado: rx.Var, etiqueta: rx.Var) -> rx.Component:
    """Píldora de dominio: fuerte / medio / débil / sin practicar."""
    return ui.state_badge(estado, etiqueta)


def etiqueta_estado(estado: rx.Var) -> rx.Var:
    """Traduce el estado de dominio al idioma activo."""
    return rx.match(
        estado,
        ("fuerte", LangState.t["fuerte"]),
        ("medio", LangState.t["medio"]),
        ("debil", LangState.t["debil"]),
        LangState.t["sin_practicar"],
    )


def cifra(valor: rx.Var, etiqueta: rx.Var, tono: str = "brand") -> rx.Component:
    """Dato duro con su etiqueta debajo. Cifra tabular para que no baile."""
    color = {
        "brand": "var(--g-primary)",
        "fuerte": "var(--g-strong-text)",
        "medio": "var(--g-medium-text)",
        "debil": "var(--g-weak-text)",
        "neutro": "var(--g-on-surface)",
    }[tono]
    return rx.el.div(
        rx.el.span(
            valor,
            class_name="g-numeral",
            font_size="clamp(2rem, 1.5rem + 1.6vw, 2.75rem)",
            line_height="1.1",
            font_weight="400",
            color=color,
        ),
        rx.el.span(
            etiqueta,
            class_name="g-label",
            color="var(--g-on-surface-variant)",
            text_transform="uppercase",
        ),
        display="flex",
        flex_direction="column",
        gap="4px",
    )


def fila_accion(
    titulo: rx.Var,
    detalle: rx.Var,
    accion: rx.Component,
    estado: rx.Component | None = None,
) -> rx.Component:
    """Fila de lista: título, detalle, estado opcional y una sola acción."""
    return ui.row(
        rx.el.div(
            rx.el.p(titulo, class_name="g-title", margin="0", color="var(--g-on-surface)"),
            rx.el.p(
                detalle,
                class_name="g-body-sm",
                margin="2px 0 0",
                color="var(--g-on-surface-variant)",
            ),
            flex="1",
            min_width="0",
        ),
        estado if estado is not None else rx.fragment(),
        accion,
        flex_wrap="wrap",
    )
