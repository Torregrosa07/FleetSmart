"""
Servicio de lógica de negocio para notificaciones
"""
from typing import Dict
from app.repositories.firebase_repository import FirebaseRepository
from app.services.fcm_service import FCMService


class NotificacionService:
    
    def __init__(self):
        self.firebase_repo = FirebaseRepository()
        self.fcm_service = FCMService()
    
    async def notificar_ruta_asignada(self, id_conductor: str, id_ruta: str) -> Dict:
        try:
            token = self.firebase_repo.obtener_token_conductor(id_conductor)
            if not token:
                return {"success": False, "mensaje": "Sin token FCM", "error": "NO_TOKEN"}
            
            ruta = self.firebase_repo.obtener_ruta(id_ruta)
            if not ruta:
                return {"success": False, "mensaje": "Ruta no encontrada", "error": "NO_RUTA"}
            
            titulo = "🚗 Nueva Ruta Asignada"
            mensaje = f"{ruta.get('nombre', '')}\n{ruta.get('origen')} → {ruta.get('destino')}"
            datos = {'id_ruta': id_ruta}
            
            enviado = await self.fcm_service.enviar_notificacion(
                token, titulo, mensaje, datos, "ruta_asignada"
            )
            
            return {
                "success": enviado,
                "mensaje": "Notificación enviada" if enviado else "Error al enviar",
                "error": None if enviado else "FCM_ERROR"
            }
        except Exception as e:
            return {"success": False, "mensaje": "Error interno", "error": str(e)}
    
    async def notificar_incidencia_nueva(self, id_incidencia: str) -> Dict:
        try:
            incidencia = self.firebase_repo.obtener_incidencia(id_incidencia)
            if not incidencia:
                return {"success": False, "mensaje": "Incidencia no encontrada", "error": "NO_INCIDENCIA"}
            
            id_gestor = incidencia.get('id_gestor')
            token = self.firebase_repo.obtener_token_gestor(id_gestor)
            if not token:
                return {"success": False, "mensaje": "Gestor sin token", "error": "NO_TOKEN"}
            
            titulo = f"⚠️ Nueva Incidencia - {incidencia.get('gravedad', 'Media')}"
            mensaje = f"{incidencia.get('tipo', '')}\n{incidencia.get('descripcion', '')[:50]}"
            datos = {'id_incidencia': id_incidencia}
            
            enviado = await self.fcm_service.enviar_notificacion(
                token, titulo, mensaje, datos, "incidencia_nueva"
            )
            
            return {
                "success": enviado,
                "mensaje": "Notificación enviada" if enviado else "Error",
                "error": None if enviado else "FCM_ERROR"
            }
        except Exception as e:
            return {"success": False, "mensaje": "Error interno", "error": str(e)}
    
    async def notificar_incidencia_asignada(self, id_incidencia: str) -> Dict:
        try:
            incidencia = self.firebase_repo.obtener_incidencia(id_incidencia)
            if not incidencia:
                return {"success": False, "mensaje": "Incidencia no encontrada", "error": "NO_INCIDENCIA"}

            id_conductor = incidencia.get('id_conductor')
            if not id_conductor:
                return {"success": False, "mensaje": "Sin conductor asignado", "error": "NO_CONDUCTOR"}

            token = self.firebase_repo.obtener_token_conductor(id_conductor)
            if not token:
                return {"success": False, "mensaje": "Conductor sin token FCM", "error": "NO_TOKEN"}

            titulo = "⚠️ Nueva Incidencia Registrada"
            mensaje = f"{incidencia.get('tipo', '')}: {incidencia.get('descripcion', '')[:50]}"
            datos = {'id_incidencia': id_incidencia}

            enviado = await self.fcm_service.enviar_notificacion(
                token, titulo, mensaje, datos, "incidencia_asignada"
            )

            return {
                "success": enviado,
                "mensaje": "Notificación enviada" if enviado else "Error al enviar",
                "error": None if enviado else "FCM_ERROR"
            }
        except Exception as e:
            return {"success": False, "mensaje": "Error interno", "error": str(e)}

    async def notificar_incidencia_actualizada(self, id_incidencia: str) -> Dict:
        try:
            incidencia = self.firebase_repo.obtener_incidencia(id_incidencia)
            if not incidencia:
                return {"success": False, "mensaje": "Incidencia no encontrada", "error": "NO_INCIDENCIA"}
            
            id_conductor = incidencia.get('id_conductor')
            token = self.firebase_repo.obtener_token_conductor(id_conductor)
            if not token:
                return {"success": False, "mensaje": "Conductor sin token", "error": "NO_TOKEN"}
            
            titulo = "📋 Actualización de Incidencia"
            mensaje = f"Estado: {incidencia.get('estado', '')}\n{incidencia.get('comentarios_gestor', '')[:50]}"
            datos = {'id_incidencia': id_incidencia}
            
            enviado = await self.fcm_service.enviar_notificacion(
                token, titulo, mensaje, datos, "incidencia_actualizada"
            )
            
            return {
                "success": enviado,
                "mensaje": "Notificación enviada" if enviado else "Error",
                "error": None if enviado else "FCM_ERROR"
            }
        except Exception as e:
            return {"success": False, "mensaje": "Error interno", "error": str(e)}