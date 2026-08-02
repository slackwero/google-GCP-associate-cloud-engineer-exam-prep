"""Punto de entrada: registra páginas y prepara la base de datos."""

import reflex as rx

from . import pages  # noqa: F401 — registra las páginas decoradas con @rx.page
from .services.db import init_db

init_db()

app = rx.App()
