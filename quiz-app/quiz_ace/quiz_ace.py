"""Punto de entrada: registra tema, páginas y modelos."""

import reflex as rx

from . import pages  # noqa: F401 — registra las páginas decoradas con @rx.page
from .models import registro  # noqa: F401 — registra los modelos para las migraciones
from .styles import COLOR_ACENTO

app = rx.App(
    theme=rx.theme(
        appearance="inherit",
        accent_color=COLOR_ACENTO,
        radius="medium",
    ),
)
