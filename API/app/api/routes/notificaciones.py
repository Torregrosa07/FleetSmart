"""
Endpoints REST para notificaciones
"""
from fastapi import APIRouter, HTTPException, status
from app.models.notificacion import (
    RutaAsignadaRequest,
    IncidenciaRequest,
    NotificacionResponse
)
from app.services.notificacion_service import NotificacionService

router = APIRouter()
notificacion_service = NotificacionService()


@router.post("/ruta-asignada", response_model=NotificacionResponse)
async def notificar_ruta_asignada(request: RutaAsignadaRequest):
    resultado = await notificacion_service.notificar_ruta_asignada(
        request.id_conductor, request.id_ruta
    )
    
    if not resultado['success']:
        raise HTTPException(status_code=400, detail=resultado)
    
    return NotificacionResponse(**resultado)


@router.post("/incidencia-nueva", response_model=NotificacionResponse)
async def notificar_incidencia_nueva(request: IncidenciaRequest):
    resultado = await notificacion_service.notificar_incidencia_nueva(
        request.id_incidencia
    )
    
    if not resultado['success']:
        raise HTTPException(status_code=400, detail=resultado)
    
    return NotificacionResponse(**resultado)


@router.post("/incidencia-asignada", response_model=NotificacionResponse)
async def notificar_incidencia_asignada(request: IncidenciaRequest):
    resultado = await notificacion_service.notificar_incidencia_asignada(
        request.id_incidencia
    )

    if not resultado['success']:
        raise HTTPException(status_code=400, detail=resultado)

    return NotificacionResponse(**resultado)


@router.post("/incidencia-actualizada", response_model=NotificacionResponse)
async def notificar_incidencia_actualizada(request: IncidenciaRequest):
    resultado = await notificacion_service.notificar_incidencia_actualizada(
        request.id_incidencia
    )
    
    if not resultado['success']:
        raise HTTPException(status_code=400, detail=resultado)
    
    return NotificacionResponse(**resultado)