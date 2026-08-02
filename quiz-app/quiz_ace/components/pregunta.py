"""Componentes compartidos para mostrar preguntas y opciones bilingües."""

import reflex as rx

from ..states.lang_state import LangState


def texto_bilingue(en: rx.Var | str, es: rx.Var | str) -> rx.Var:
    """Elige el texto según el idioma activo."""
    return rx.cond(LangState.idioma_activo == "es", es, en)


def encabezado_pregunta(numero: rx.Var, total: rx.Var, extra: rx.Component | None = None) -> rx.Component:
    return rx.flex(
        rx.text(
            LangState.t["pregunta"], " ", numero, " ", LangState.t["de"], " ", total,
            size="2",
            color=rx.color("gray", 11),
        ),
        rx.spacer(),
        extra if extra is not None else rx.fragment(),
        align="center",
        width="100%",
    )


def tarjeta_enunciado(texto_en: rx.Var, texto_es: rx.Var, tipo: rx.Var) -> rx.Component:
    return rx.box(
        rx.text(texto_bilingue(texto_en, texto_es), size="4", weight="medium"),
        rx.cond(
            tipo == "multiple",
            rx.badge("Select all that apply / Selecciona todas las que apliquen", color_scheme="amber", margin_top="2"),
            rx.fragment(),
        ),
        width="100%",
    )


def boton_opcion(
    opcion: rx.Var,
    seleccion: rx.Var,
    on_click,
    respuesta_correcta: rx.Var | None = None,
    mostrando_feedback: rx.Var | bool = False,
) -> rx.Component:
    """Opción como botón de ancho completo; colorea aciertos/errores en feedback."""
    letra = opcion["letra"]
    seleccionada = seleccion.contains(letra)
    if respuesta_correcta is not None:
        es_correcta_var = respuesta_correcta.contains(letra)
        color_fondo = rx.cond(
            mostrando_feedback,
            rx.cond(
                es_correcta_var,
                rx.color("green", 4),
                rx.cond(seleccionada, rx.color("red", 4), "transparent"),
            ),
            rx.cond(seleccionada, rx.color("accent", 4), "transparent"),
        )
    else:
        color_fondo = rx.cond(seleccionada, rx.color("accent", 4), "transparent")

    return rx.button(
        rx.flex(
            rx.badge(letra, variant="solid"),
            rx.text(texto_bilingue(opcion["en"], opcion["es"]), size="3", text_align="left", white_space="normal"),
            gap="3",
            align="center",
        ),
        on_click=on_click,
        variant="outline",
        width="100%",
        height="auto",
        padding="3",
        justify_content="flex-start",
        background=color_fondo,
    )
