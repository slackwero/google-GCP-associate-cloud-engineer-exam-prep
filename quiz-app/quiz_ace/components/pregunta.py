"""Componentes compartidos para mostrar preguntas y opciones bilingües."""

import reflex as rx

from ..states.lang_state import LangState


def texto_bilingue(en: rx.Var | str, es: rx.Var | str) -> rx.Var:
    """Elige el texto según el idioma activo."""
    return rx.cond(LangState.idioma_activo == "es", es, en)


def encabezado_pregunta(numero: rx.Var, total: rx.Var, extra: rx.Component | None = None) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            LangState.t["pregunta"], " ", numero, " ", LangState.t["de"], " ", total,
            class_name="g-label g-numeral",
            color="var(--g-on-surface-variant)",
            text_transform="uppercase",
        ),
        rx.el.div(flex="1"),
        extra if extra is not None else rx.fragment(),
        display="flex",
        align_items="center",
        gap="12px",
        width="100%",
    )


def tarjeta_enunciado(texto_en: rx.Var, texto_es: rx.Var, tipo: rx.Var) -> rx.Component:
    """El enunciado manda: es lo más grande de la pantalla, con medida legible."""
    return rx.el.div(
        rx.el.p(
            texto_bilingue(texto_en, texto_es),
            class_name="g-title-lg g-measure",
            color="var(--g-on-surface)",
            margin="0",
        ),
        rx.cond(
            tipo == "multiple",
            rx.el.p(
                LangState.t["multiple_aviso"],
                class_name="g-body-sm",
                color="var(--g-medium-text)",
                background="var(--g-medium-container)",
                border_radius="var(--g-corner-sm)",
                padding="6px 12px",
                margin="12px 0 0",
                display="inline-block",
            ),
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
    """Opción de respuesta.

    Con feedback activo cada opción declara su veredicto — correcta, fallada o
    descartada — y el CSS lo revela con un barrido. Ese es el único momento de
    movimiento autorizado del sistema: enseñar el descarte es el producto.
    """
    letra = opcion["letra"]
    seleccionada = seleccion.contains(letra)

    if respuesta_correcta is not None:
        es_correcta = respuesta_correcta.contains(letra)
        veredicto = rx.cond(
            mostrando_feedback,
            rx.cond(
                es_correcta,
                "correcta",
                rx.cond(seleccionada, "fallada", "descartada"),
            ),
            "",
        )
    else:
        veredicto = ""

    return rx.el.button(
        rx.el.span(letra, class_name="g-option-letter", aria_hidden="true"),
        rx.el.span(
            texto_bilingue(opcion["en"], opcion["es"]),
            class_name="g-body-sm",
            style={"white_space": "normal"},
        ),
        on_click=on_click,
        type="button",
        class_name="g-option",
        custom_attrs={
            "data-selected": rx.cond(seleccionada, "true", "false"),
            "data-verdict": veredicto,
        },
        aria_pressed=rx.cond(seleccionada, "true", "false"),
    )
