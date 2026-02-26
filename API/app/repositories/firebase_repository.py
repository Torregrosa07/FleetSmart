from typing import Optional, Dict, Any
from firebase_admin import db


class FirebaseRepository:
    
    DATABASE_URL = "https://fleetsmart-1-default-rtdb.europe-west1.firebasedatabase.app"
    
    def _ref(self, path: str):
        return db.reference(path)
    
    def obtener_conductor(self, id_conductor: str) -> Optional[Dict[str, Any]]:
        try:
            return self._ref(f'conductores/{id_conductor}').get()
        except Exception as e:
            print(f"Error obteniendo conductor: {e}")
            return None
    
    def obtener_ruta(self, id_ruta: str) -> Optional[Dict[str, Any]]:
        try:
            return self._ref(f'rutas/{id_ruta}').get()
        except Exception as e:
            print(f"Error obteniendo ruta: {e}")
            return None
    
    def obtener_incidencia(self, id_incidencia: str) -> Optional[Dict[str, Any]]:
        try:
            return self._ref(f'incidencias/{id_incidencia}').get()
        except Exception as e:
            print(f"Error obteniendo incidencia: {e}")
            return None
    
    def obtener_gestor(self, id_gestor: str) -> Optional[Dict[str, Any]]:
        try:
            return self._ref(f'gestores/{id_gestor}').get()
        except Exception as e:
            print(f"Error obteniendo gestor: {e}")
            return None
    
    def obtener_token_conductor(self, id_conductor: str) -> Optional[str]:
        conductor = self.obtener_conductor(id_conductor)
        if not conductor:
            print(f"⚠️ Conductor {id_conductor} no encontrado")
            return None
        token = conductor.get('fcm_token')
        if not token:
            print(f"⚠️ Conductor {id_conductor} sin fcm_token. Datos: {conductor}")
        return token
    
    def obtener_token_gestor(self, id_gestor: str) -> Optional[str]:
        gestor = self.obtener_gestor(id_gestor)
        if not gestor:
            print(f"⚠️ Gestor {id_gestor} no encontrado")
            return None
        return gestor.get('fcm_token')