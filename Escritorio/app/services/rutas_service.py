"""
RutasService - Lógica de negocio de Rutas

RESPONSABILIDADES:
- Validaciones de datos de rutas
- Operaciones CRUD con el repositorio
- Aplicar reglas de negocio de rutas

NO SE ENCARGA DE:
- Geocodificación (eso está en geocoding_utils)
- Creación de mapas (eso está en map_utils)
- Manejo de UI
"""
from app.models.ruta import Ruta
from app.repositories.ruta_repository import RutaRepository


class RutasService:
    """
    Servicio que encapsula la lógica de negocio de rutas.
    """
    
    def __init__(self, db_connection):
        self.repo = RutaRepository(db_connection)
    
    # =========================================================================
    # VALIDACIONES
    # =========================================================================
    
    def validar_ruta(self, nombre, origen, paradas, fecha, hora_inicio, hora_fin):
        """
        Valida que una ruta tenga todos los datos correctos.
        
        Args:
            nombre: Nombre de la ruta
            origen: Dirección de origen
            paradas: Lista de paradas
            fecha: Fecha de la ruta
            hora_inicio: Hora de inicio
            hora_fin: Hora de fin
            
        Returns:
            (True, "") si es válido
            (False, "mensaje de error") si no es válido
        """
        # Validar nombre
        if not nombre or not nombre.strip():
            return (False, "La ruta necesita un nombre.")
        
        # Validar origen
        if not origen or not origen.strip():
            return (False, "Define un punto de origen.")
        
        # Validar paradas
        if not paradas or len(paradas) == 0:
            return (False, "Añade al menos una parada.")
        
        # Validar que las paradas tengan el formato correcto
        for i, parada in enumerate(paradas):
            if 'direccion' not in parada or 'coords' not in parada:
                return (False, f"La parada {i+1} no tiene el formato correcto.")
        
        # Validar fecha (básico)
        if not fecha or not fecha.strip():
            return (False, "La fecha es obligatoria.")
        
        # Validar horas
        if not hora_inicio or not hora_fin:
            return (False, "Las horas de inicio y fin son obligatorias.")
        
        # Validar que hora inicio sea antes que hora fin
        # Convertir a formato comparable (HH:mm)
        try:
            h_inicio = hora_inicio.split(":")
            h_fin = hora_fin.split(":")
            
            inicio_minutos = int(h_inicio[0]) * 60 + int(h_inicio[1])
            fin_minutos = int(h_fin[0]) * 60 + int(h_fin[1])
            
            if inicio_minutos >= fin_minutos:
                return (False, "La hora de inicio debe ser anterior a la hora de fin.")
        except:
            return (False, "Formato de hora inválido.")
        
        return (True, "")
    
    # =========================================================================
    # CREAR RUTA
    # =========================================================================
    
    def crear_ruta(self, ruta):
        """
        Crea una nueva ruta.
        
        NOTA: Se asume que los datos ya fueron validados en el controlador.
        
        Args:
            ruta: Objeto Ruta con los datos
            
        Returns:
            (True, ruta, "mensaje") si éxito
            (False, None, "mensaje de error") si falla
        """
        try:
            if self.repo.guardar_ruta(ruta):
                return (True, ruta, "Ruta creada correctamente.")
            else:
                return (False, None, "Error al guardar la ruta.")
        
        except Exception as e:
            return (False, None, f"Error: {str(e)}")
    
    # =========================================================================
    # ACTUALIZAR RUTA
    # =========================================================================
    
    def actualizar_ruta(self, ruta):
        """
        Actualiza una ruta existente.
        
        NOTA: Se asume que los datos ya fueron validados en el controlador.
        
        Args:
            ruta: Objeto Ruta con los datos actualizados
            
        Returns:
            (True, "mensaje") si éxito
            (False, "mensaje de error") si falla
        """
        try:
            if self.repo.actualizar_ruta(ruta):
                return (True, "Ruta actualizada correctamente.")
            else:
                return (False, "Error al actualizar la ruta.")
        
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    # =========================================================================
    # ELIMINAR RUTA
    # =========================================================================
    
    def eliminar_ruta(self, id_ruta):
        """
        Elimina una ruta.
        
        Args:
            id_ruta: ID de la ruta a eliminar
            
        Returns:
            (True, "mensaje") si éxito
            (False, "mensaje de error") si falla
        """
        try:
            if self.repo.eliminar_ruta(id_ruta):
                return (True, "Ruta eliminada correctamente.")
            else:
                return (False, "Error al eliminar la ruta.")
        
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    # =========================================================================
    # CONSULTAS
    # =========================================================================
    
    def obtener_todas(self):
        """Obtiene todas las rutas"""
        return self.repo.obtener_todas()
    
    def obtener_por_id(self, id_ruta):
        """Obtiene una ruta por ID"""
        return self.repo.obtener_por_id(id_ruta)
    
    def obtener_pendientes(self):
        """Obtiene solo rutas pendientes"""
        todas = self.repo.obtener_todas()
        return [r for r in todas if r.estado == "Pendiente"]