"""Agregaciones del dashboard: dominio con recencia, cobertura y enfoque.

Trabaja sobre listas de dicts planos (las filas desnormalizadas de la tabla
Respuesta), sin depender de Reflex ni de la base de datos.
"""

import math
from collections import defaultdict
from datetime import datetime

UMBRAL_FUERTE = 80.0
UMBRAL_MEDIO = 60.0
VIDA_MEDIA_DIAS = 14.0


def clasificar_dominio(pct: float | None) -> str:
    if pct is None:
        return "sin_practicar"
    if pct >= UMBRAL_FUERTE:
        return "fuerte"
    if pct >= UMBRAL_MEDIO:
        return "medio"
    return "debil"


def calcular_dominio(respuestas: list[dict], dimension: str, ahora: datetime) -> dict:
    """% de acierto ponderado por recencia (vida media de 14 días) por dimensión.

    Para dimensiones multivalor (servicios, subtopicos) el valor viene como
    slugs separados por coma y la respuesta cuenta para cada uno.
    """
    aciertos = defaultdict(float)
    totales = defaultdict(float)

    for respuesta in respuestas:
        edad_dias = max((ahora - respuesta["fecha"]).total_seconds() / 86400, 0.0)
        peso = math.pow(0.5, edad_dias / VIDA_MEDIA_DIAS)
        for clave in _claves(respuesta, dimension):
            totales[clave] += peso
            if respuesta["correcta"]:
                aciertos[clave] += peso

    dominio = {}
    for clave, total in totales.items():
        pct = round(aciertos[clave] * 100 / total, 1) if total else None
        dominio[clave] = {"pct": pct, "estado": clasificar_dominio(pct)}
    return dominio


def calcular_cobertura(respuestas: list[dict], banco_por_clave: dict[str, list[str]], campo: str) -> dict:
    """Preguntas distintas ya practicadas vs. total del banco, por clave."""
    vistas_por_clave = defaultdict(set)
    for respuesta in respuestas:
        for clave in _claves(respuesta, campo):
            vistas_por_clave[clave].add(respuesta["pregunta_id"])

    cobertura = {}
    for clave, ids_banco in banco_por_clave.items():
        total = len(ids_banco)
        vistas = len(vistas_por_clave.get(clave, set()) & set(ids_banco))
        cobertura[clave] = {"vistas": vistas, "total": total, "pct": round(vistas * 100 / total, 1) if total else 0.0}
    return cobertura


def calcular_enfoque(dominio: dict, cobertura: dict, pesos: dict) -> list[dict]:
    """Ordena las claves por dónde conviene más estudiar.

    Prioridad = (100 - dominio) x peso x (1 + falta de cobertura). Las claves
    sin practicar van primero: sin datos no se puede asumir dominio.
    """
    enfoque = []
    for clave, peso in pesos.items():
        info = dominio.get(clave)
        pct = info["pct"] if info else None
        cob = cobertura.get(clave, {}).get("pct", 0.0)
        if pct is None:
            prioridad = math.inf
        else:
            prioridad = (100.0 - pct) * peso * (1.0 + (100.0 - cob) / 100.0)
        enfoque.append(
            {
                "clave": clave,
                "estado": clasificar_dominio(pct),
                "dominio_pct": pct,
                "cobertura_pct": cob,
                "peso": peso,
                "prioridad": prioridad,
            }
        )
    return sorted(enfoque, key=lambda e: (-e["prioridad"], -e["peso"]))


def _claves(respuesta: dict, dimension: str) -> list:
    valor = respuesta[dimension]
    if isinstance(valor, str) and dimension in ("servicios", "subtopicos"):
        return [v for v in valor.split(",") if v]
    return [valor]
