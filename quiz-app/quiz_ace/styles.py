"""Tokens del sistema visual: Material 3 sobre la paleta de marca de Google.

La fuente de verdad de los valores es `assets/theme.css`. Aquí solo viven los
nombres que el código Python necesita citar, para que ningún componente escriba
un color a mano. Cambiar un valor se hace en el CSS, no aquí.
"""

# --- Layout -----------------------------------------------------------------
ANCHO_CONTENIDO = "1120px"
ANCHO_LECTURA = "var(--g-measure)"

# --- Color ------------------------------------------------------------------
# Acción y estructura. El azul de marca (#4285F4) es la firma; el accionable
# (#0B57D0) es el que pasa contraste AA sobre blanco.
PRIMARIO = "var(--g-primary)"
SOBRE_PRIMARIO = "var(--g-on-primary)"
PRIMARIO_CONTENEDOR = "var(--g-primary-container)"
SOBRE_PRIMARIO_CONTENEDOR = "var(--g-on-primary-container)"
MARCA = "var(--g-blue)"

# Superficies tonales.
FONDO = "var(--g-background)"
SUPERFICIE = "var(--g-surface)"
SUPERFICIE_BAJA = "var(--g-surface-container-low)"
SUPERFICIE_CONTENEDOR = "var(--g-surface-container)"
SUPERFICIE_ALTA = "var(--g-surface-container-high)"
TEXTO = "var(--g-on-surface)"
TEXTO_SUAVE = "var(--g-on-surface-variant)"
BORDE = "var(--g-outline-variant)"
BORDE_FUERTE = "var(--g-outline)"

# El trío semántico. Nunca decoran: significan dominio.
COLOR_FUERTE = "var(--g-strong)"
COLOR_MEDIO = "var(--g-medium)"
COLOR_DEBIL = "var(--g-weak)"
COLOR_SIN_DATOS = "var(--g-outline)"
COLOR_CORRECTO = "var(--g-strong)"
COLOR_INCORRECTO = "var(--g-weak)"

# --- Forma ------------------------------------------------------------------
RADIO_SM = "var(--g-corner-sm)"
RADIO_MD = "var(--g-corner-md)"
RADIO_LG = "var(--g-corner-lg)"
RADIO_XL = "var(--g-corner-xl)"
RADIO_FULL = "var(--g-corner-full)"

# --- Elevación --------------------------------------------------------------
ELEV_1 = "var(--g-elev-1)"
ELEV_2 = "var(--g-elev-2)"

# --- Movimiento -------------------------------------------------------------
EASE = "var(--g-ease-emphasized)"
DUR_CORTA = "var(--g-dur-short)"
DUR_MEDIA = "var(--g-dur-medium)"

# --- Umbrales de dominio (lógica, no estilo) --------------------------------
UMBRAL_FUERTE = 80.0
UMBRAL_MEDIO = 60.0
META_APROBACION = 70
META_PERSONAL = 95
