"""Carga, validación e índices del banco de preguntas bilingüe.

Lógica pura sin dependencias de Reflex: la app la consume desde los states
y los tests la ejercitan directamente.
"""

import json
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from string import ascii_uppercase

logger = logging.getLogger(__name__)

IDIOMAS = ("en", "es")
NIVELES = ("principiante", "intermedio", "avanzado")
TIPOS = ("unica", "multiple")
DOC_PREFIJOS = ("https://cloud.google.com/", "https://developers.google.com/", "https://kubernetes.io/")


@dataclass(frozen=True)
class Catalogos:
    cursos: dict[str, dict]
    servicios: dict[str, dict]
    secciones: list[dict]
    subtopicos: dict[str, dict]


@dataclass(frozen=True)
class PreguntaExcluida:
    id: str
    archivo: str
    errores: list[str]


@dataclass
class Banco:
    preguntas: list[dict] = field(default_factory=list)
    excluidas: list[PreguntaExcluida] = field(default_factory=list)
    por_curso: dict[str, list[dict]] = field(default_factory=dict)
    por_servicio: dict[str, list[dict]] = field(default_factory=dict)
    por_nivel: dict[str, list[dict]] = field(default_factory=dict)
    por_seccion: dict[int, list[dict]] = field(default_factory=dict)
    por_subtopico: dict[str, list[dict]] = field(default_factory=dict)


def cargar_catalogos(data_dir: Path | str) -> Catalogos:
    data_dir = Path(data_dir)
    cursos = _leer_json(data_dir / "cursos.json")["cursos"]
    servicios = _leer_json(data_dir / "servicios.json")["servicios"]
    blueprint = _leer_json(data_dir / "blueprint.json")
    return Catalogos(
        cursos={c["slug"]: c for c in cursos},
        servicios={s["slug"]: s for s in servicios},
        secciones=blueprint["secciones"],
        subtopicos={s["id"]: s for s in blueprint["subtopicos"]},
    )


def validar_pregunta(pregunta: dict, catalogos: Catalogos) -> list[str]:
    """Devuelve la lista de errores de la pregunta; vacía si es válida."""
    errores: list[str] = []

    if not pregunta.get("id"):
        errores.append("falta id")
    # curso nulo = pregunta de refuerzo del blueprint (no pertenece al path)
    if pregunta.get("curso") is not None and pregunta["curso"] not in catalogos.cursos:
        errores.append(f"curso desconocido: {pregunta['curso']}")
    for servicio in pregunta.get("servicios") or []:
        if servicio not in catalogos.servicios:
            errores.append(f"servicio desconocido: {servicio}")
    if not pregunta.get("servicios"):
        errores.append("falta al menos un servicio")
    for subtopico in pregunta.get("subtopicos") or []:
        if subtopico not in catalogos.subtopicos:
            errores.append(f"subtopico desconocido: {subtopico}")
    if not pregunta.get("subtopicos"):
        errores.append("falta al menos un subtopico")

    secciones_validas = {s["numero"] for s in catalogos.secciones}
    if pregunta.get("seccion_blueprint") not in secciones_validas:
        errores.append(f"seccion_blueprint inválida: {pregunta.get('seccion_blueprint')}")
    if pregunta.get("nivel") not in NIVELES:
        errores.append(f"nivel inválido: {pregunta.get('nivel')}")
    if pregunta.get("tipo") not in TIPOS:
        errores.append(f"tipo inválido: {pregunta.get('tipo')}")

    errores += _validar_bilingue("pregunta", pregunta.get("pregunta"))
    opciones = pregunta.get("opciones") or []
    if len(opciones) < 2:
        errores.append("se requieren al menos 2 opciones")
    for i, opcion in enumerate(opciones):
        errores += _validar_bilingue(f"opciones[{i}]", opcion)
    errores += _validar_bilingue("explicacion", pregunta.get("explicacion"))

    letras_validas = set(ascii_uppercase[: len(opciones)])
    respuesta = pregunta.get("respuesta") or []
    if not respuesta or not set(respuesta) <= letras_validas:
        errores.append(f"respuesta fuera de opciones: {respuesta}")
    elif pregunta.get("tipo") == "unica" and len(respuesta) != 1:
        errores.append("tipo unica exige exactamente 1 respuesta")
    elif pregunta.get("tipo") == "multiple" and len(respuesta) < 2:
        errores.append("tipo multiple exige 2+ respuestas")

    doc = pregunta.get("doc") or ""
    if not doc.startswith(DOC_PREFIJOS):
        errores.append(f"doc debe ser documentación oficial: {doc}")

    return errores


def cargar_banco(data_dir: Path | str) -> Banco:
    """Carga todas las preguntas de data/preguntas/, valida e indexa."""
    data_dir = Path(data_dir)
    catalogos = cargar_catalogos(data_dir)
    banco = Banco()
    ids_vistos: set[str] = set()

    for archivo in sorted((data_dir / "preguntas").glob("*.json")):
        for pregunta in _leer_json(archivo)["preguntas"]:
            errores = validar_pregunta(pregunta, catalogos)
            if pregunta.get("id") in ids_vistos:
                errores.append(f"id duplicado: {pregunta.get('id')}")
            if errores:
                excluida = PreguntaExcluida(id=pregunta.get("id", "?"), archivo=archivo.name, errores=errores)
                banco.excluidas.append(excluida)
                logger.warning("Pregunta excluida %s (%s): %s", excluida.id, archivo.name, "; ".join(errores))
                continue
            ids_vistos.add(pregunta["id"])
            banco.preguntas.append(pregunta)

    _indexar(banco)
    return banco


def _indexar(banco: Banco) -> None:
    por_curso = defaultdict(list)
    por_servicio = defaultdict(list)
    por_nivel = defaultdict(list)
    por_seccion = defaultdict(list)
    por_subtopico = defaultdict(list)
    for pregunta in banco.preguntas:
        if pregunta.get("curso"):
            por_curso[pregunta["curso"]].append(pregunta)
        por_nivel[pregunta["nivel"]].append(pregunta)
        por_seccion[pregunta["seccion_blueprint"]].append(pregunta)
        for servicio in pregunta["servicios"]:
            por_servicio[servicio].append(pregunta)
        for subtopico in pregunta["subtopicos"]:
            por_subtopico[subtopico].append(pregunta)
    banco.por_curso = dict(por_curso)
    banco.por_servicio = dict(por_servicio)
    banco.por_nivel = dict(por_nivel)
    banco.por_seccion = dict(por_seccion)
    banco.por_subtopico = dict(por_subtopico)


def _validar_bilingue(campo: str, valor: dict | None) -> list[str]:
    if not isinstance(valor, dict):
        return [f"{campo}: falta texto bilingüe"]
    faltantes = [idioma for idioma in IDIOMAS if not (valor.get(idioma) or "").strip()]
    if faltantes:
        return [f"{campo}: falta idioma {'/'.join(faltantes)}"]
    return []


def _leer_json(ruta: Path) -> dict:
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)
