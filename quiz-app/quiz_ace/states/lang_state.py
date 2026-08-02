"""Estado del idioma: inglés por defecto, cambiable a español (es-419)."""

import reflex as rx

from ..i18n import IDIOMA_DEFAULT, IDIOMAS, textos_para


class LangState(rx.State):
    idioma: str = rx.LocalStorage(IDIOMA_DEFAULT, name="quiz_ace_idioma")

    @rx.event
    def cambiar_idioma(self, idioma: str):
        if idioma in IDIOMAS:
            self.idioma = idioma

    @rx.var
    def idioma_activo(self) -> str:
        return self.idioma if self.idioma in IDIOMAS else IDIOMA_DEFAULT

    @rx.var
    def t(self) -> dict[str, str]:
        """Todos los textos de UI en el idioma activo."""
        return textos_para(self.idioma_activo)
