"""
Servicio FCM para enviar notificaciones
"""
from typing import Optional, Dict
from app.core.firebase import firebase_client


class FCMService:
    
    def __init__(self):
        self.messaging = firebase_client.messaging
    
    async def enviar_notificacion(
        self,
        token: str,
        titulo: str,
        mensaje: str,
        datos: Optional[Dict[str, str]] = None,
        tipo: str = "general"
    ) -> bool:
        try:
            message = self.messaging.Message(
                notification=self.messaging.Notification(
                    title=titulo,
                    body=mensaje,
                ),
                data={'tipo': tipo, **(datos or {})},
                token=token,
                android=self.messaging.AndroidConfig(
                    priority='high',
                    notification=self.messaging.AndroidNotification(
                        icon='ic_notification',
                        color='#2196F3',
                        sound='default'
                    )
                )
            )
            
            response = self.messaging.send(message)
            print(f"✅ Notificación enviada: {response}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False