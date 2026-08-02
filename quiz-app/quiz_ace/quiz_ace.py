"""Punto de entrada: registra páginas y prepara la base de datos."""

import reflex as rx

from . import pages  # noqa: F401 — registra las páginas decoradas con @rx.page
from .services.db import init_db

init_db()

# theme.css define los tokens Material 3 sobre la paleta de Google y remapea las
# escalas de Radix, para que los componentes de stock hereden el mismo mundo.
app = rx.App(stylesheets=["/theme.css"])
