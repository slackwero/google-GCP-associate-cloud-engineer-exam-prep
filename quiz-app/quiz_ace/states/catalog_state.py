"""Carga única del banco de preguntas y catálogos para toda la app."""

from pathlib import Path

import reflex as rx

from ..services.banco import Banco, Catalogos, cargar_banco, cargar_catalogos

DATA_DIR = Path(__file__).parent.parent.parent / "data"

# El banco es de solo lectura: se carga una vez al importar el módulo y se
# comparte entre sesiones. Los states solo guardan vistas ligeras de él.
CATALOGOS: Catalogos = cargar_catalogos(DATA_DIR)
BANCO: Banco = cargar_banco(DATA_DIR)


class CatalogState(rx.State):
    """Expone catálogos como datos serializables para la UI."""

    @rx.var
    def cursos(self) -> list[dict]:
        return [
            {
                "slug": c["slug"],
                "tipo": c["tipo"],
                "nombre_en": c["nombre"]["en"],
                "nombre_es": c["nombre"]["es"],
                "disponibles": len(BANCO.por_curso.get(c["slug"], [])),
            }
            for c in sorted(CATALOGOS.cursos.values(), key=lambda c: c["orden"])
        ]

    @rx.var
    def servicios(self) -> list[dict]:
        servicios = []
        for s in CATALOGOS.servicios.values():
            disponibles = len(BANCO.por_servicio.get(s["slug"], []))
            if disponibles:
                servicios.append(
                    {
                        "slug": s["slug"],
                        "nombre_en": s["nombre"]["en"],
                        "nombre_es": s["nombre"]["es"],
                        "disponibles": disponibles,
                    }
                )
        return sorted(servicios, key=lambda s: -s["disponibles"])

    @rx.var
    def total_preguntas(self) -> int:
        return len(BANCO.preguntas)
