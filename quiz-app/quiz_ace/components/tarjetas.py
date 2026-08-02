"""Tarjetas reutilizables para home y dashboard."""

import reflex as rx


def tarjeta_modo(titulo: rx.Var, descripcion: rx.Var, accion: rx.Component) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.heading(titulo, size="4"),
            rx.text(descripcion, size="2", color=rx.color("gray", 11)),
            accion,
            direction="column",
            gap="3",
            height="100%",
        ),
        width="100%",
    )


def stat_card(titulo: rx.Var, valor: rx.Var) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.text(titulo, size="2", color=rx.color("gray", 11)),
            rx.heading(valor, size="6"),
            direction="column",
            gap="1",
        ),
        width="100%",
    )


def badge_estado(estado: rx.Var, etiqueta: rx.Var) -> rx.Component:
    return rx.badge(
        etiqueta,
        color_scheme=rx.match(
            estado,
            ("fuerte", "green"),
            ("medio", "amber"),
            ("debil", "red"),
            "gray",
        ),
    )
