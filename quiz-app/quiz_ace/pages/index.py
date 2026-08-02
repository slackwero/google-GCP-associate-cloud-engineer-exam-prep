"""Home: dónde estás parado y cuál es el siguiente paso."""

import reflex as rx

from ..components import ui
from ..components.pregunta import texto_bilingue
from ..components.tarjetas import cifra, etiqueta_estado, fila_accion
from ..states.catalog_state import CatalogState
from ..states.exam_state import ExamState
from ..states.lang_state import LangState
from ..states.progress_state import ProgressState
from ..templates.base_layout import base_layout


def _panel_con_datos() -> rx.Component:
    """Tu promedio, contra el corte real, y el tema que más te conviene atacar."""
    return ui.panel(
        rx.el.div(
            rx.el.div(
                cifra(
                    ProgressState.promedio_examenes.to_string() + "%",
                    LangState.t["promedio"],
                    tono="brand",
                ),
                rx.el.div(
                    ui.meter(ProgressState.promedio_examenes, estado="brand"),
                    rx.el.p(
                        LangState.t["meta_aprobacion"],
                        class_name="g-body-sm",
                        color="var(--g-on-surface-variant)",
                        margin="8px 0 0",
                    ),
                    flex="1",
                    min_width="180px",
                ),
                display="flex",
                align_items="flex-end",
                gap="24px",
                flex_wrap="wrap",
                flex="1",
                min_width="260px",
            ),
            rx.el.div(
                rx.el.span(
                    LangState.t["punto_debil"],
                    class_name="g-label",
                    color="var(--g-on-surface-variant)",
                    text_transform="uppercase",
                ),
                rx.el.p(
                    texto_bilingue(ProgressState.foco_nombre_en, ProgressState.foco_nombre_es),
                    class_name="g-title",
                    margin="6px 0 10px",
                ),
                ui.state_badge(ProgressState.foco_estado, etiqueta_estado(ProgressState.foco_estado)),
                background="var(--g-surface-container-low)",
                border="1px solid var(--g-outline-variant)",
                border_radius="var(--g-corner-lg)",
                padding="16px",
                min_width="240px",
                flex="1",
            ),
            display="flex",
            gap="24px",
            flex_wrap="wrap",
            width="100%",
        ),
        ui.cluster(
            ui.link_button(LangState.t["ver_avances"], href="/dashboard", variante="filled"),
            ui.link_button(LangState.t["practicar"], href="/estudiar/curso", variante="outlined"),
            margin_top="20px",
        ),
    )


def _panel_vacio() -> rx.Component:
    """Primera ejecución: alguien que acaba de clonar el repo y no te conoce."""
    return ui.panel(
        ui.title(LangState.t["como_vas"], nivel=2, margin="0"),
        rx.el.p(
            LangState.t["primer_paso"],
            class_name="g-body g-measure",
            color="var(--g-on-surface-variant)",
            margin="10px 0 20px",
        ),
        ui.cluster(
            ui.button(
                LangState.t["examen_corto"],
                on_click=ExamState.iniciar("corto"),
                variante="filled",
            ),
            ui.link_button(LangState.t["practicar"], href="/estudiar/curso", variante="outlined"),
        ),
    )


def _seccion_practicar() -> rx.Component:
    return ui.section(
        ui.title(LangState.t["practicar"], nivel=2, margin="0"),
        rx.el.p(
            LangState.t["practicar_desc"],
            class_name="g-body-sm",
            color="var(--g-on-surface-variant)",
            margin="0 0 4px",
        ),
        fila_accion(
            LangState.t["por_curso"],
            LangState.t["por_curso_desc"],
            ui.link_button(LangState.t["comenzar"], href="/estudiar/curso", variante="tonal"),
        ),
        fila_accion(
            LangState.t["por_servicio"],
            LangState.t["por_servicio_desc"],
            ui.link_button(LangState.t["comenzar"], href="/estudiar/servicio", variante="tonal"),
        ),
    )


def _seccion_examenes() -> rx.Component:
    return ui.section(
        ui.title(LangState.t["simulacros"], nivel=2, margin="0"),
        rx.el.p(
            LangState.t["simulacros_desc"],
            class_name="g-body-sm",
            color="var(--g-on-surface-variant)",
            margin="0 0 4px",
        ),
        fila_accion(
            LangState.t["examen_corto"],
            LangState.t["examen_corto_desc"],
            ui.button(LangState.t["comenzar"], on_click=ExamState.iniciar("corto"), variante="tonal"),
        ),
        fila_accion(
            LangState.t["examen_medio"],
            LangState.t["examen_medio_desc"],
            ui.button(LangState.t["comenzar"], on_click=ExamState.iniciar("medio"), variante="tonal"),
        ),
        fila_accion(
            LangState.t["examen_full"],
            LangState.t["examen_full_desc"],
            ui.button(LangState.t["comenzar"], on_click=ExamState.iniciar("full"), variante="filled"),
        ),
    )


@rx.page(route="/", title="Google Cloud Associate Cloud Engineer Certification Exam", on_load=ProgressState.cargar)
def index() -> rx.Component:
    return base_layout(
        ui.stack(
            rx.el.div(
                ui.headline(LangState.t["app_subtitulo"], margin="0", class_name="g-measure"),
                rx.el.p(
                    CatalogState.total_preguntas,
                    " ",
                    LangState.t["banco_total"],
                    " · ",
                    LangState.t["sobre_el_examen"],
                    class_name="g-body-sm",
                    color="var(--g-on-surface-variant)",
                    margin="8px 0 0",
                ),
            ),
            rx.cond(ProgressState.hay_datos, _panel_con_datos(), _panel_vacio()),
            _seccion_practicar(),
            _seccion_examenes(),
            gap="32px",
            padding_bottom="8px",
        ),
    )
