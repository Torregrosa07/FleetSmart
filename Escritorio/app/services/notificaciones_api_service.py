"""
NotificacionesAPIService - Servicio para enviar notificaciones via API

Este servicio se comunica con la API de notificaciones para enviar
push notifications a los conductores cuando se les asigna una ruta
o cuando hay actualizaciones de incidencias.
"""
import requests
from typing import Tuple, Optional
from app.config.config import API_NOTIFICACIONES_URL


class NotificacionesAPIService:
    """
    Servicio para enviar notificaciones push via API REST.
    
    Endpoints:
    - POST /ruta-asignada: Notifica a conductor de nueva ruta
    - POST /incidencia-nueva: Notifica a gestor de nueva incidencia
    - POST /incidencia-actualizada: Notifica a conductor de actualizacion
    """
    
    def __init__(self):
        self.base_url = API_NOTIFICACIONES_URL
        self.timeout = 2  # segundos
    
    def _hacer_peticion(self, endpoint: str, datos: dict) -> Tuple[bool, str]:
        """
        Realiza una peticion POST a la API.
        
        Args:
            endpoint: Ruta del endpoint (ej: "/ruta-asignada")
            datos: Diccionario con los datos a enviar
            
        Returns:
            Tupla (exito, mensaje)
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.post(
                url,
                json=datos,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                resultado = response.json()
                return True, resultado.get("mensaje", "Notificacion enviada")
            else:
                # Error de la API
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", {}).get("mensaje", str(error_data))
                except:
                    error_msg = f"Error HTTP {response.status_code}"
                return False, error_msg
                
        except requests.exceptions.ConnectionError:
            return False, "No se pudo conectar con el servidor de notificaciones"
        except requests.exceptions.Timeout:
            return False, "Tiempo de espera agotado al conectar con la API"
        except Exception as e:
            return False, f"Error al enviar notificacion: {str(e)}"
    
    def notificar_ruta_asignada(self, id_conductor: str, id_ruta: str) -> Tuple[bool, str]:
        """
        Notifica a un conductor que se le ha asignado una ruta.
        
        Args:
            id_conductor: ID del conductor en Firebase
            id_ruta: ID de la ruta asignada
            
        Returns:
            Tupla (exito, mensaje)
        """
        datos = {
            "id_conductor": id_conductor,
            "id_ruta": id_ruta
        }
        return self._hacer_peticion("/ruta-asignada", datos)
    
    def notificar_incidencia_asignada(self, id_incidencia: str) -> Tuple[bool, str]:
        """
        Notifica al conductor de una nueva incidencia registrada por el gestor.

        Args:
            id_incidencia: ID de la incidencia creada

        Returns:
            Tupla (exito, mensaje)
        """
        datos = {
            "id_incidencia": id_incidencia
        }
        return self._hacer_peticion("/incidencia-asignada", datos)

    def notificar_incidencia_nueva(self, id_incidencia: str) -> Tuple[bool, str]:
        """
        Notifica al gestor que se ha creado una nueva incidencia.
        
        Args:
            id_incidencia: ID de la incidencia creada
            
        Returns:
            Tupla (exito, mensaje)
        """
        datos = {
            "id_incidencia": id_incidencia
        }
        return self._hacer_peticion("/incidencia-nueva", datos)
    
    def notificar_incidencia_actualizada(self, id_incidencia: str) -> Tuple[bool, str]:
        """
        Notifica al conductor que su incidencia ha sido actualizada.
        
        Args:
            id_incidencia: ID de la incidencia actualizada
            
        Returns:
            Tupla (exito, mensaje)
        """
        datos = {
            "id_incidencia": id_incidencia
        }
        return self._hacer_peticion("/incidencia-actualizada", datos)


# Instancia global del servicio (singleton)
notificaciones_api = NotificacionesAPIService()
