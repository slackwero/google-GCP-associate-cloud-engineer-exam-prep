"""Primitivas del sistema Material 3.

Todo el estilo vive en `assets/theme.css`; aquí solo se componen elementos HTML
con las clases correctas. Ningún componente de la app debería escribir colores,
radios ni sombras a mano.
"""

from typing import Any

import reflex as rx


# --- Tipografía -------------------------------------------------------------
def display(*hijos, **props) -> rx.Component:
    """Cifra o título de mayor peso. Usa <h1> una sola vez por página."""
    props["class_name"] = f"g-display {props.pop('class_name', '')}".strip()
    return rx.el.h1(*hijos, **props)


def headline(*hijos, **props) -> rx.Component:
    """Título de página."""
    props["class_name"] = f"g-headline {props.pop('class_name', '')}".strip()
    return rx.el.h1(*hijos, **props)


def title(*hijos, nivel: int = 2, **props) -> rx.Component:
    """Título de sección. `nivel` fija la jerarquía real del documento."""
    props["class_name"] = f"g-title-lg {props.pop('class_name', '')}".strip()
    etiqueta = {2: rx.el.h2, 3: rx.el.h3, 4: rx.el.h4}[nivel]
    return etiqueta(*hijos, **props)


def subtitle(*hijos, nivel: int = 3, **props) -> rx.Component:
    """Encabezado menor, dentro de una tarjeta o panel."""
    props["class_name"] = f"g-title {props.pop('class_name', '')}".strip()
    etiqueta = {2: rx.el.h2, 3: rx.el.h3, 4: rx.el.h4}[nivel]
    return etiqueta(*hijos, **props)


def body(*hijos, **props) -> rx.Component:
    props["class_name"] = f"g-body {props.pop('class_name', '')}".strip()
    return rx.el.p(*hijos, **props)


def body_sm(*hijos, **props) -> rx.Component:
    props["class_name"] = f"g-body-sm {props.pop('class_name', '')}".strip()
    return rx.el.p(*hijos, **props)


def muted(*hijos, **props) -> rx.Component:
    """Texto secundario. Tintado desde la superficie, nunca gris puro."""
    props["class_name"] = f"g-body-sm {props.pop('class_name', '')}".strip()
    props.setdefault("color", "var(--g-on-surface-variant)")
    return rx.el.p(*hijos, **props)


# --- Acciones ---------------------------------------------------------------
def button(
    *hijos,
    variante: str = "filled",
    tamano: str = "md",
    bloque: bool = False,
    **props,
) -> rx.Component:
    """Botón M3. Variantes: filled, tonal, outlined, text, danger."""
    clases = ["g-btn", f"g-btn--{variante}"]
    if tamano == "sm":
        clases.append("g-btn--sm")
    if bloque:
        clases.append("g-btn--block")
    extra = props.pop("class_name", "")
    props["class_name"] = " ".join(clases + ([extra] if extra else []))
    props.setdefault("type", "button")
    return rx.el.button(*hijos, **props)


def link_button(*hijos, href: str, variante: str = "filled", bloque: bool = False, **props) -> rx.Component:
    """Enlace con aspecto de botón: navega de verdad, no simula con on_click."""
    clases = ["g-btn", f"g-btn--{variante}"]
    if bloque:
        clases.append("g-btn--block")
    props["class_name"] = " ".join(clases)
    return rx.link(*hijos, href=href, **props)


def icon_button(icono: str, etiqueta: str, **props) -> rx.Component:
    """Control de solo icono. `etiqueta` es obligatoria: va al aria-label."""
    props["class_name"] = "g-iconbtn"
    props["aria_label"] = etiqueta
    props.setdefault("type", "button")
    return rx.el.button(rx.icon(tag=icono, size=20), **props)


def chip(etiqueta: Any, activo: Any = False, **props) -> rx.Component:
    """Chip de filtro (nivel, idioma)."""
    props["class_name"] = "g-chip"
    props["custom_attrs"] = {"data-active": rx.cond(activo, "true", "false")}
    props.setdefault("type", "button")
    props.setdefault("aria_pressed", rx.cond(activo, "true", "false"))
    return rx.el.button(etiqueta, **props)


# --- Superficies ------------------------------------------------------------
def card(*hijos, plana: bool = False, interactiva: bool = False, **props) -> rx.Component:
    clases = ["g-card"]
    if plana:
        clases.append("g-card--flat")
    if interactiva:
        clases.append("g-card--interactive")
    extra = props.pop("class_name", "")
    props["class_name"] = " ".join(clases + ([extra] if extra else []))
    props.setdefault("padding", "20px")
    return rx.el.div(*hijos, **props)


def panel(*hijos, **props) -> rx.Component:
    """Contenedor mayor, esquinas de 28px. Para el bloque de estado de la home."""
    props["class_name"] = f"g-panel {props.pop('class_name', '')}".strip()
    props.setdefault("padding", "24px")
    return rx.el.div(*hijos, **props)


def row(*hijos, **props) -> rx.Component:
    """Fila de lista de acciones: sustituye a la rejilla de tarjetas iguales."""
    props["class_name"] = f"g-row {props.pop('class_name', '')}".strip()
    return rx.el.div(*hijos, **props)


def divider(**props) -> rx.Component:
    props["class_name"] = "g-divider"
    return rx.el.hr(**props)


# --- Estado de dominio ------------------------------------------------------
def state_badge(estado: Any, etiqueta: Any) -> rx.Component:
    """Píldora de dominio. `estado` es fuerte | medio | debil | cualquier otro."""
    clase = rx.match(
        estado,
        ("fuerte", "g-state g-state--fuerte"),
        ("medio", "g-state g-state--medio"),
        ("debil", "g-state g-state--debil"),
        "g-state g-state--none",
    )
    return rx.el.span(etiqueta, class_name=clase)


def meter(pct: Any, estado: Any = "brand", **props) -> rx.Component:
    """Barra de dominio o cobertura, con el mismo trío semántico."""
    clase = rx.match(
        estado,
        ("fuerte", "g-meter g-meter--fuerte"),
        ("medio", "g-meter g-meter--medio"),
        ("debil", "g-meter g-meter--debil"),
        ("brand", "g-meter g-meter--brand"),
        "g-meter g-meter--none",
    )
    return rx.el.div(
        rx.el.i(style={"width": pct.to_string() + "%"}),
        class_name=clase,
        role="progressbar",
        aria_valuenow=pct,
        aria_valuemin=0,
        aria_valuemax=100,
        **props,
    )


# --- Layout -----------------------------------------------------------------
def stack(*hijos, gap: str = "16px", **props) -> rx.Component:
    props.setdefault("display", "flex")
    props.setdefault("flex_direction", "column")
    props.setdefault("gap", gap)
    props.setdefault("width", "100%")
    return rx.el.div(*hijos, **props)


def cluster(*hijos, gap: str = "12px", **props) -> rx.Component:
    """Fila que envuelve en pantallas pequeñas en vez de desbordarse."""
    props.setdefault("display", "flex")
    props.setdefault("flex_wrap", "wrap")
    props.setdefault("align_items", "center")
    props.setdefault("gap", gap)
    return rx.el.div(*hijos, **props)


def section(*hijos, **props) -> rx.Component:
    props.setdefault("display", "flex")
    props.setdefault("flex_direction", "column")
    props.setdefault("gap", "12px")
    props.setdefault("width", "100%")
    return rx.el.section(*hijos, **props)
