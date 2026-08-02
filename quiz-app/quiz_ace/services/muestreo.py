"""Selección aleatoria de preguntas para modos de estudio y examen."""

import copy
import random
from string import ascii_uppercase

PESOS_BLUEPRINT = {1: 0.20, 2: 0.30, 3: 0.30, 4: 0.20}


def seleccionar_estudio(
    preguntas: list[dict],
    curso: str | None = None,
    servicio: str | None = None,
    nivel: str | None = None,
    limite: int | None = None,
    rng: random.Random | None = None,
) -> list[dict]:
    """Filtra por curso/servicio/nivel y devuelve las preguntas barajadas."""
    rng = rng or random.Random()  # noqa: S311 — aleatoriedad de juego, no criptográfica
    seleccion = [
        p
        for p in preguntas
        if (curso is None or p.get("curso") == curso)
        and (servicio is None or servicio in p["servicios"])
        and (nivel is None or p["nivel"] == nivel)
    ]
    rng.shuffle(seleccion)
    return seleccion[:limite] if limite else seleccion


def generar_examen(
    preguntas: list[dict],
    tamano: int,
    ponderado: bool = False,
    rng: random.Random | None = None,
) -> list[dict]:
    """Arma un examen aleatorio sin repetidos.

    Con ponderado=True reparte el tamaño según los pesos del blueprint
    (20/30/30/20); si a una sección le faltan preguntas, completa con el resto.
    """
    rng = rng or random.Random()  # noqa: S311

    if not ponderado:
        seleccion = list(preguntas)
        rng.shuffle(seleccion)
        return seleccion[:tamano]

    por_seccion = {s: [p for p in preguntas if p["seccion_blueprint"] == s] for s in PESOS_BLUEPRINT}
    examen: list[dict] = []
    for seccion, peso in PESOS_BLUEPRINT.items():
        cupo = round(tamano * peso)
        grupo = por_seccion[seccion]
        rng.shuffle(grupo)
        examen.extend(grupo[:cupo])

    if len(examen) < tamano:
        ids_usados = {p["id"] for p in examen}
        restantes = [p for p in preguntas if p["id"] not in ids_usados]
        rng.shuffle(restantes)
        examen.extend(restantes[: tamano - len(examen)])

    rng.shuffle(examen)
    return examen[:tamano]


def barajar_opciones(pregunta: dict, rng: random.Random | None = None) -> dict:
    """Devuelve una copia con las opciones barajadas y la respuesta remapeada."""
    rng = rng or random.Random()  # noqa: S311
    barajada = copy.deepcopy(pregunta)
    indices = list(range(len(barajada["opciones"])))
    rng.shuffle(indices)

    correctos_originales = {ascii_uppercase.index(letra) for letra in barajada["respuesta"]}
    barajada["opciones"] = [pregunta["opciones"][i] for i in indices]
    barajada["respuesta"] = sorted(
        ascii_uppercase[nueva_pos] for nueva_pos, original in enumerate(indices) if original in correctos_originales
    )
    return barajada
