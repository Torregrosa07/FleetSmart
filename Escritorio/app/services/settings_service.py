import json
import os

class SettingsService:
    def __init__(self):
        # Calculamos la ruta absoluta al archivo settings.json
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(base_dir, "config", "settings.json")
        
        # Estado por defecto
        self.app_state = {
            "language": "Español",
            "theme": "Oscuro", 
            "empresa_direccion": "",
            "empresa_coords": None,
            "user": None
        }
        
        # Aseguramos que la carpeta config exista
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        self.load()

    def load(self):
        """Carga la configuración desde el archivo JSON si existe."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    
                    # Filtramos 'user' para no cargarlo de un json antiguo si existiera
                    if "user" in datos:
                        del datos["user"]
                        
                    self.app_state.update(datos)
                print("Configuración cargada correctamente.")
            except Exception as e:
                print(f"Error cargando settings: {e}")
        else:
            print("No se encontró archivo de configuración, usando valores por defecto.")

    def save(self):
        """Guarda la configuración actual en el archivo JSON."""
        try:
            # Creamos una copia para no guardar datos de sesión (como el usuario logueado)
            datos_a_guardar = self.app_state.copy()
            if "user" in datos_a_guardar:
                del datos_a_guardar["user"]

            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(datos_a_guardar, f, indent=4)
            print("Configuración guardada en disco.")
        except Exception as e:
            print(f"Error guardando settings: {e}")