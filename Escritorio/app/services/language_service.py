# app/services/language_service.py
from app.config.translations import TRANSLATIONS

class LanguageService:
    @staticmethod
    def get_text(key, idioma_seleccionado):
        """
        Recibe la clave (ej: 'vehicles') y el idioma del app_state (Ej: 'Español', 'Inglés').
        Devuelve el texto traducido.
        """
        # 1. Mapear el nombre del combo ("Español") al código del diccionario ("es")
        codigos = {
            "Español": "es",
            "Inglés": "en",
            "English": "en" # Por si acaso
        }
        
        # Si no encuentra el código, usa español por defecto
        code = codigos.get(idioma_seleccionado, "es")
        
        # 2. Obtener el diccionario del idioma
        diccionario = TRANSLATIONS.get(code, {})
        
        # 3. Devolver la traducción o la clave si no existe
        return diccionario.get(key, key)