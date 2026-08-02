"""Dashboard de avances: evolución, dominio, cobertura y enfoque."""

import reflex as rx

from ..components import ui
from ..components.pregunta import texto_bilingue
from ..components.tarjetas import cifra, etiqueta_estado
from ..states.lang_state import LangState
from ..states.progress_state import ProgressState
from ..styles import META_APROBACION, META_PERSONAL
from ..templates.base_layout import base_layout


def _grafica_evolucion() -> rx.Component:
    """Tus intentos contra las dos líneas de referencia: el corte y tu meta."""
    return ui.card(
        rx.el.h2(LangState.t["evolucion"], class_name="g-title", margin="0 0 12px"),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke="var(--g-outline-variant)", vertical=False),
            rx.recharts.line(
                data_key="puntaje",
                stroke="var(--g-blue)",
                stroke_width=2,
                dot={"fill": "var(--g-blue)", "r": 3},
            ),
            rx.recharts.reference_line(
                y=META_APROBACION,
                stroke="var(--g-medium)",
                stroke_dasharray="4 4",
                label=LangState.t["meta_aprobacion"],
            ),
            rx.recharts.reference_line(
                y=META_PERSONAL,
                stroke="var(--g-strong)",
                stroke_dasharray="4 4",
                label=LangState.t["meta_personal"],
            ),
            rx.recharts.x_axis(data_key="fecha", stroke="var(--g-on-surface-variant)"),
            rx.recharts.y_axis(domain=[0, 100], stroke="var(--g-on-surface-variant)"),
            rx.recharts.graphing_tooltip(),
            data=ProgressState.evolucion,
            height=280,
            width="100%",
        ),
        width="100%",
    )


def _fila_dominio(fila: rx.Var) -> rx.Component:
    """Nombre, barra y estado: el porcentaje se lee sin buscarlo."""
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                texto_bilingue(fila["nombre_en"], fila["nombre_es"]),
                class_name="g-body-sm",
                flex="1",
                min_width="0",
            ),
            rx.el.span(
                fila["pct"],
                "%",
                class_name="g-body-sm g-numeral",
                color="var(--g-on-surface-variant)",
            ),
            display="flex",
            align_items="baseline",
            gap="12px",
            margin_bottom="6px",
        ),
        ui.meter(fila["pct"], estado=fila["estado"]),
        padding="10px 0",
    )


def _lista_dominio(titulo: rx.Var, filas: rx.Var) -> rx.Component:
    return ui.card(
        rx.el.h2(titulo, class_name="g-title", margin="0 0 4px"),
        rx.foreach(filas, _fila_dominio),
        flex="1",
        min_width="280px",
    )


def _fila_cobertura(fila: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                texto_bilingue(fila["nombre_en"], fila["nombre_es"]),
                class_name="g-body-sm",
                flex="1",
                min_width="0",
            ),
            rx.el.span(
                fila["vistas"],
                " / ",
                fila["total"],
                class_name="g-body-sm g-numeral",
                color="var(--g-on-surface-variant)",
            ),
            display="flex",
            align_items="baseline",
            gap="12px",
            margin_bottom="6px",
        ),
        ui.meter(fila["pct"], estado="brand"),
        padding="10px 0",
    )


def _fila_enfoque(fila: rx.Var, indice: rx.Var) -> rx.Component:
    """Orden de ataque: lo que más te conviene estudiar ahora, y por qué."""
    return ui.row(
        rx.el.span(
            indice + 1,
            class_name="g-option-letter g-numeral",
            aria_hidden="true",
        ),
        rx.el.span(
            texto_bilingue(fila["nombre_en"], fila["nombre_es"]),
            class_name="g-body-sm",
            flex="1",
            min_width="0",
        ),
        ui.state_badge(fila["estado"], etiqueta_estado(fila["estado"])),
        flex_wrap="wrap",
    )


def _cifra(cantidad: rx.Var, singular: str, plural: str) -> rx.Component:
    """A count with its noun. Both languages break the plural at one."""
    return rx.el.span(
        cantidad,
        " ",
        rx.cond(cantidad == 1, LangState.t[singular], LangState.t[plural]),
        class_name="g-numeral",
    )


def _alcance(intentos: rx.Var, respuestas: rx.Var) -> rx.Component:
    """How much the deletion takes away, in figures, before confirming it."""
    return ui.body_sm(
        LangState.t["reset_alcance"],
        " ",
        _cifra(intentos, "intento_min", "intentos_min"),
        " · ",
        _cifra(respuestas, "respuesta_min", "respuestas_min"),
        color="var(--g-on-surface-variant)",
        margin="12px 0 0",
    )


def _dialogo_reset(
    etiqueta: rx.Var,
    descripcion: rx.Var,
    alcance: rx.Component,
    accion,
    variante: str,
    deshabilitado: rx.Var | bool = False,
) -> rx.Component:
    """Confirmation for a deletion, same pattern as the exam submit dialog."""
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            ui.button(etiqueta, variante=variante, disabled=deshabilitado),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title(etiqueta),
            rx.alert_dialog.description(descripcion),
            alcance,
            ui.cluster(
                rx.alert_dialog.cancel(
                    ui.button(LangState.t["cancelar"], variante="text"),
                ),
                rx.alert_dialog.action(
                    ui.button(LangState.t["borrar"], on_click=accion, variante="danger"),
                ),
                justify_content="flex-end",
                margin_top="20px",
            ),
        ),
    )


def _mantenimiento() -> rx.Component:
    """Local history reset. Only rendered when there is something to delete."""
    return ui.section(
        ui.divider(margin="8px 0 20px"),
        ui.title(LangState.t["mantenimiento"], nivel=2, margin="0 0 4px"),
        ui.muted(LangState.t["mantenimiento_desc"], class_name="g-body-sm g-measure"),
        ui.cluster(
            _dialogo_reset(
                LangState.t["limpiar_incompletos"],
                LangState.t["reset_incompletos_desc"],
                _alcance(
                    ProgressState.historial_incompletos,
                    ProgressState.historial_respuestas_incompletas,
                ),
                ProgressState.limpiar_incompletos,
                variante="outlined",
                deshabilitado=ProgressState.historial_incompletos == 0,
            ),
            _dialogo_reset(
                LangState.t["borrar_historial"],
                LangState.t["reset_todo_desc"],
                _alcance(ProgressState.historial_intentos, ProgressState.historial_respuestas),
                ProgressState.resetear_todo,
                variante="danger",
            ),
            margin_top="16px",
        ),
    )


def _con_datos() -> rx.Component:
    return ui.stack(
        ui.panel(
            ui.cluster(
                cifra(ProgressState.intentos_totales, LangState.t["intentos"], tono="neutro"),
                cifra(
                    ProgressState.promedio_examenes.to_string() + "%",
                    LangState.t["promedio"],
                    tono="brand",
                ),
                gap="48px",
            ),
        ),
        _grafica_evolucion(),
        ui.section(
            ui.title(LangState.t["enfoque_recomendado"], nivel=2, margin="0"),
            ui.stack(rx.foreach(ProgressState.enfoque, _fila_enfoque), gap="8px"),
        ),
        # flex-start y no stretch: forzar la misma altura dejaba media columna
        # vacía cuando una lista es mucho más larga que la otra.
        ui.cluster(
            _lista_dominio(LangState.t["dominio_seccion"], ProgressState.dominio_seccion),
            _lista_dominio(LangState.t["dominio_servicio"], ProgressState.dominio_servicio),
            align_items="flex-start",
            gap="16px",
        ),
        _lista_dominio(LangState.t["dominio_curso"], ProgressState.dominio_curso),
        ui.card(
            rx.el.h2(LangState.t["cobertura"], class_name="g-title", margin="0 0 4px"),
            rx.foreach(ProgressState.cobertura_curso, _fila_cobertura),
        ),
        _mantenimiento(),
        gap="28px",
    )


def _sin_datos() -> rx.Component:
    return ui.panel(
        rx.el.p(LangState.t["sin_datos"], class_name="g-title g-measure", margin="0 0 16px"),
        ui.cluster(
            ui.link_button(LangState.t["practicar"], href="/study/course", variante="filled"),
            ui.link_button(LangState.t["volver_inicio"], href="/", variante="outlined"),
        ),
    )


@rx.page(route="/dashboard", title="Progress · Google Cloud ACE Certification Exam", on_load=ProgressState.cargar)
def dashboard() -> rx.Component:
    return base_layout(
        ui.stack(
            ui.headline(LangState.t["dashboard_titulo"], margin="0"),
            rx.cond(ProgressState.hay_datos, _con_datos(), _sin_datos()),
            gap="24px",
        ),
    )
