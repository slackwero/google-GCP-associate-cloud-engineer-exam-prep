"""Textos de UI en inglés (default) y español de Latinoamérica (es-419).

Los textos de las preguntas NO viven aquí: van bilingües dentro de cada
registro del banco (data/preguntas/*.json).
"""

IDIOMA_DEFAULT = "en"
IDIOMAS = ("en", "es")

TEXTOS: dict[str, dict[str, str]] = {
    "app_titulo": {"en": "ACE Quiz", "es": "Quiz ACE"},
    "app_subtitulo": {
        "en": "Google Associate Cloud Engineer exam prep",
        "es": "Preparación para el examen Google Associate Cloud Engineer",
    },
    "nav_inicio": {"en": "Home", "es": "Inicio"},
    "nav_dashboard": {"en": "Progress", "es": "Avances"},
    "estudiar": {"en": "Study", "es": "Estudiar"},
    "estudiar_desc": {
        "en": "Instant feedback with explanations after each question",
        "es": "Feedback inmediato con explicación tras cada pregunta",
    },
    "por_curso": {"en": "By course", "es": "Por curso"},
    "por_curso_desc": {
        "en": "Questions from each activity of the official learning path",
        "es": "Preguntas de cada actividad del path oficial"
    },
    "por_servicio": {"en": "By service", "es": "Por servicio"},
    "por_servicio_desc": {
        "en": "Questions filtered by Google Cloud service",
        "es": "Preguntas filtradas por servicio de Google Cloud"
    },
    "examen": {"en": "Exam", "es": "Examen"},
    "examen_desc": {
        "en": "Random, timed, no feedback until you submit",
        "es": "Aleatorio, cronometrado, sin feedback hasta enviar",
    },
    "examen_corto": {"en": "Short exam", "es": "Examen corto"},
    "examen_corto_desc": {"en": "20 questions · 25 min", "es": "20 preguntas · 25 min"},
    "examen_medio": {"en": "Medium exam", "es": "Examen medio"},
    "examen_medio_desc": {"en": "40 questions · 50 min", "es": "40 preguntas · 50 min"},
    "examen_full": {"en": "Full exam", "es": "Examen full"},
    "examen_full_desc": {
        "en": "50 questions · 2 h · real blueprint weights",
        "es": "50 preguntas · 2 h · pesos reales del blueprint",
    },
    "nivel": {"en": "Level", "es": "Nivel"},
    "nivel_todos": {"en": "All levels", "es": "Todos los niveles"},
    "nivel_principiante": {"en": "Beginner", "es": "Principiante"},
    "nivel_intermedio": {"en": "Intermediate", "es": "Intermedio"},
    "nivel_avanzado": {"en": "Advanced", "es": "Avanzado"},
    "comenzar": {"en": "Start", "es": "Comenzar"},
    "pregunta": {"en": "Question", "es": "Pregunta"},
    "de": {"en": "of", "es": "de"},
    "responder": {"en": "Answer", "es": "Responder"},
    "siguiente": {"en": "Next", "es": "Siguiente"},
    "anterior": {"en": "Previous", "es": "Anterior"},
    "correcto": {"en": "Correct!", "es": "¡Correcto!"},
    "incorrecto": {"en": "Incorrect", "es": "Incorrecto"},
    "explicacion": {"en": "Explanation", "es": "Explicación"},
    "ver_doc": {"en": "Official docs", "es": "Documentación oficial"},
    "marcar_revision": {"en": "Mark for review", "es": "Marcar para revisar"},
    "marcada": {"en": "Marked", "es": "Marcada"},
    "enviar_examen": {"en": "Submit exam", "es": "Enviar examen"},
    "confirmar_envio": {
        "en": "Submit now? Unanswered questions count as incorrect.",
        "es": "¿Enviar ahora? Las preguntas sin responder cuentan como incorrectas.",
    },
    "tiempo_restante": {"en": "Time left", "es": "Tiempo restante"},
    "resultado": {"en": "Result", "es": "Resultado"},
    "puntaje": {"en": "Score", "es": "Puntaje"},
    "aprobado": {"en": "Passed", "es": "Aprobado"},
    "reprobado": {"en": "Not passed", "es": "Reprobado"},
    "correctas": {"en": "correct", "es": "correctas"},
    "desglose_seccion": {"en": "By exam section", "es": "Por sección del examen"},
    "desglose_servicio": {"en": "By service", "es": "Por servicio"},
    "revision_falladas": {"en": "Review missed questions", "es": "Revisión de preguntas falladas"},
    "tu_respuesta": {"en": "Your answer", "es": "Tu respuesta"},
    "respuesta_correcta": {"en": "Correct answer", "es": "Respuesta correcta"},
    "sin_respuesta": {"en": "No answer", "es": "Sin respuesta"},
    "volver_inicio": {"en": "Back to home", "es": "Volver al inicio"},
    "reintentar": {"en": "Try again", "es": "Reintentar"},
    "dashboard_titulo": {"en": "Study progress", "es": "Avances de estudio"},
    "evolucion": {"en": "Score evolution", "es": "Evolución del puntaje"},
    "meta_aprobacion": {"en": "Passing threshold (70%)", "es": "Corte de aprobación (70%)"},
    "meta_personal": {"en": "Personal goal (95%)", "es": "Meta personal (95%)"},
    "dominio_seccion": {"en": "Mastery by exam section", "es": "Dominio por sección del examen"},
    "dominio_servicio": {"en": "Mastery by service", "es": "Dominio por servicio"},
    "dominio_curso": {"en": "Mastery by course", "es": "Dominio por curso"},
    "cobertura": {"en": "Bank coverage", "es": "Cobertura del banco"},
    "enfoque_recomendado": {"en": "Recommended focus", "es": "Enfoque recomendado"},
    "sin_practicar": {"en": "Not practiced", "es": "Sin practicar"},
    "refuerzo_blueprint": {"en": "Blueprint reinforcement", "es": "Refuerzo del blueprint"},
    "fuerte": {"en": "Strong", "es": "Fuerte"},
    "medio": {"en": "Medium", "es": "Medio"},
    "debil": {"en": "Weak", "es": "Débil"},
    "intentos": {"en": "Attempts", "es": "Intentos"},
    "promedio": {"en": "Average", "es": "Promedio"},
    "sin_datos": {
        "en": "No attempts yet — take a quiz to see your progress here",
        "es": "Aún no hay intentos — haz un quiz para ver tu avance aquí",
    },
    "sin_preguntas": {
        "en": "No questions available for this filter yet",
        "es": "Aún no hay preguntas disponibles para este filtro",
    },
    "abandonado": {"en": "Abandoned", "es": "Abandonado"},
    "modo_estudio_curso": {"en": "Study · course", "es": "Estudio · curso"},
    "modo_estudio_servicio": {"en": "Study · service", "es": "Estudio · servicio"},
    "modo_examen_corto": {"en": "Short exam", "es": "Examen corto"},
    "modo_examen_medio": {"en": "Medium exam", "es": "Examen medio"},
    "modo_examen_full": {"en": "Full exam", "es": "Examen full"},
    "preguntas_disponibles": {"en": "questions available", "es": "preguntas disponibles"},
    "terminar_sesion": {"en": "Finish session", "es": "Terminar sesión"},
    "sesion_completada": {"en": "Session complete", "es": "Sesión completada"},
}


def textos_para(idioma: str) -> dict[str, str]:
    """Aplana el diccionario de textos al idioma pedido (fallback a inglés)."""
    if idioma not in IDIOMAS:
        idioma = IDIOMA_DEFAULT
    return {clave: valores[idioma] for clave, valores in TEXTOS.items()}
