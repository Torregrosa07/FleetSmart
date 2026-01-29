"""
Repository para acceso a Firebase Database
"""
from typing import Optional, Dict, Any
from app.core.firebase import firebase_client


class FirebaseRepository:
    
    def __init__(self):
        self.db = firebase_client.database
    
    def obtener_conductor(self, id_conductor: str) -> Optional[Dict[str, Any]]:
        try:
            return self.db.child('conductores').child(id_conductor).get()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def obtener_ruta(self, id_ruta: str) -> Optional[Dict[str, Any]]:
        try:
            return self.db.child('rutas').child(id_ruta).get()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def obtener_incidencia(self, id_incidencia: str) -> Optional[Dict[str, Any]]:
        try:
            return self.db.child('incidencias').child(id_incidencia).get()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def obtener_gestor(self, id_gestor: str) -> Optional[Dict[str, Any]]:
        try:
            return self.db.child('gestores').child(id_gestor).get()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def obtener_token_conductor(self, id_conductor: str) -> Optional[str]:
        conductor = self.obtener_conductor(id_conductor)
        return conductor.get('fcm_token') if conductor else None
    
    def obtener_token_gestor(self, id_gestor: str) -> Optional[str]:
        gestor = self.obtener_gestor(id_gestor)
        return gestor.get('fcm_token') if gestor else None