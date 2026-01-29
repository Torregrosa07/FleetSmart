"""
Modelos Pydantic para notificaciones
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict
from enum import Enum


class TipoNotificacion(str, Enum):
    RUTA_ASIGNADA = "ruta_asignada"
    INCIDENCIA_NUEVA = "incidencia_nueva"
    INCIDENCIA_ACTUALIZADA = "incidencia_actualizada"


class RutaAsignadaRequest(BaseModel):
    id_conductor: str
    id_ruta: str


class IncidenciaRequest(BaseModel):
    id_incidencia: str


class NotificacionResponse(BaseModel):
    success: bool
    mensaje: str
    error: Optional[str] = None