import os
from PySide6.QtWidgets import QApplication

class StyleManager:
    @staticmethod
    def aplicar_tema(app: QApplication, tema: str):
        """
        Carga el archivo .qss correspondiente y lo aplica a la app global.
        tema: 'Claro' o 'Oscuro'
        """
        # 1. Seleccionar archivo
        archivo = "light.qss"  # Por defecto
        
        if tema == "Oscuro":
            archivo = "dark.qss"
        elif tema == "Claro":
            archivo = "light.qss"
            
        # 2. CALCULAR RUTA ABSOLUTA (Esta es la corrección clave)
        # Obtenemos la carpeta donde está ESTE archivo (style_manager.py)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Y le añadimos el nombre del archivo .qss
        ruta_estilo = os.path.join(base_dir, archivo)
        
        # Debug: Imprimir ruta para verificar

        try:
            with open(ruta_estilo, "r") as f:
                estilo = f.read()
                # 3. Aplicar estilo a la aplicación
                app.setStyleSheet(estilo)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de estilos en: {ruta_estilo}")
        except Exception as e:
            print(f"Error aplicando estilos: {e}")