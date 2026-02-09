from app.repositories.incidencia_repository import IncidenciaRepository
from app.repositories.vehiculo_repository import VehiculoRepository
from app.repositories.conductor_repository import ConductorRepository


class IncidenciasService:
    
    # Estados posibles en orden de progresión
    ESTADOS = ["Pendiente", "En Proceso", "Resuelta"]
    
    def __init__(self, db_connection):
        self.repo_incidencias = IncidenciaRepository(db_connection)
        self.repo_vehiculos = VehiculoRepository(db_connection)
        self.repo_conductores = ConductorRepository(db_connection)
    
    # =========================================================================
    # VALIDACIONES
    # =========================================================================
    
    def validar_creacion_incidencia(self):
        """
        Valida que existan vehículos antes de crear una incidencia.
        
        Returns:
            (True, vehiculos, conductores) si válido
            (False, None, None) si no hay vehículos
        """
        vehiculos = self.repo_vehiculos.obtener_todos()
        conductores = self.repo_conductores.obtener_todos()
        
        if not vehiculos:
            return (False, None, None)
        
        return (True, vehiculos, conductores)
    
    # =========================================================================
    # LÓGICA DE ESTADOS
    # =========================================================================
    
    def obtener_siguiente_estado(self, estado_actual):
        """
        Obtiene el siguiente estado en la progresión.
        
        Args:
            estado_actual: Estado actual de la incidencia
            
        Returns:
            (True, nuevo_estado) si hay siguiente estado
            (False, None) si ya está en el estado final
        """
        try:
            indice_actual = self.ESTADOS.index(estado_actual)
            
            if indice_actual == len(self.ESTADOS) - 1:
                # Ya está en el estado final
                return (False, None)
            
            nuevo_estado = self.ESTADOS[indice_actual + 1]
            return (True, nuevo_estado)
        
        except ValueError:
            # Estado no reconocido
            return (False, None)
    
    def puede_cambiar_estado(self, estado_actual):
        """
        Verifica si una incidencia puede cambiar de estado.
        
        Returns:
            (True, "") si puede cambiar
            (False, "mensaje") si no puede cambiar
        """
        puede, _ = self.obtener_siguiente_estado(estado_actual)
        
        if not puede:
            return (False, "Esta incidencia ya está en estado 'Resuelta'.")
        
        return (True, "")
    
    # =========================================================================
    # CREAR INCIDENCIA
    # =========================================================================
    
    def crear_incidencia(self, incidencia):
        """
        Crea una nueva incidencia.
        
        Args:
            incidencia: Objeto Incidencia con los datos
            
        Returns:
            (True, incidencia, "mensaje") si éxito
            (False, None, "mensaje de error") si falla
        """
        try:
            if self.repo_incidencias.guardar_incidencia(incidencia):
                return (True, incidencia, "Incidencia registrada correctamente.")
            else:
                return (False, None, "Error al guardar la incidencia.")
        
        except Exception as e:
            return (False, None, f"Error: {str(e)}")
    
    # =========================================================================
    # ACTUALIZAR INCIDENCIA
    # =========================================================================
    
    def actualizar_incidencia(self, incidencia):
        """
        Actualiza una incidencia existente.
        
        Args:
            incidencia: Objeto Incidencia con los datos actualizados
            
        Returns:
            (True, "mensaje") si éxito
            (False, "mensaje de error") si falla
        """
        try:
            if self.repo_incidencias.actualizar_incidencia(incidencia):
                return (True, "Incidencia actualizada correctamente.")
            else:
                return (False, "Error al actualizar la incidencia.")
        
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    def cambiar_estado_incidencia(self, incidencia):
        """
        Cambia el estado de una incidencia al siguiente estado.
        
        Args:
            incidencia: Objeto Incidencia (se modifica directamente)
            
        Returns:
            (True, nuevo_estado, "mensaje") si éxito
            (False, None, "mensaje de error") si falla
        """
        # Validar que pueda cambiar
        puede, mensaje_error = self.puede_cambiar_estado(incidencia.estado)
        if not puede:
            return (False, None, mensaje_error)
        
        # Obtener siguiente estado
        _, nuevo_estado = self.obtener_siguiente_estado(incidencia.estado)
        estado_anterior = incidencia.estado
        
        # Actualizar estado
        incidencia.estado = nuevo_estado
        
        # Guardar en Firebase
        try:
            if self.repo_incidencias.actualizar_incidencia(incidencia):
                return (True, nuevo_estado, f"Estado cambiado a: {nuevo_estado}")
            else:
                # Revertir cambio si falla
                incidencia.estado = estado_anterior
                return (False, None, "Error al actualizar el estado.")
        
        except Exception as e:
            # Revertir cambio si falla
            incidencia.estado = estado_anterior
            return (False, None, f"Error: {str(e)}")
    
    # =========================================================================
    # ELIMINAR INCIDENCIA
    # =========================================================================
    
    def eliminar_incidencia(self, id_incidencia):
        """
        Elimina una incidencia.
        
        Args:
            id_incidencia: ID de la incidencia a eliminar
            
        Returns:
            (True, "mensaje") si éxito
            (False, "mensaje de error") si falla
        """
        try:
            if self.repo_incidencias.eliminar_incidencia(id_incidencia):
                return (True, "Incidencia eliminada correctamente.")
            else:
                return (False, "Error al eliminar la incidencia.")
        
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    # =========================================================================
    # CONSULTAS
    # =========================================================================
    
    def obtener_todas(self):
        """Obtiene todas las incidencias"""
        return self.repo_incidencias.obtener_todas()
    
    def obtener_por_id(self, id_incidencia):
        """Obtiene una incidencia por ID"""
        return self.repo_incidencias.obtener_por_id(id_incidencia)
    
    def obtener_por_estado(self, estado):
        """
        Obtiene incidencias filtradas por estado.
        
        Args:
            estado: Estado a filtrar (o "Todas")
            
        Returns:
            Lista de incidencias filtradas
        """
        todas = self.repo_incidencias.obtener_todas()
        
        if estado == "Todas":
            return todas
        
        return [inc for inc in todas if inc.estado == estado]
    
    def obtener_pendientes(self):
        """Obtiene solo incidencias pendientes"""
        return self.obtener_por_estado("Pendiente")
    
    def obtener_en_proceso(self):
        """Obtiene solo incidencias en proceso"""
        return self.obtener_por_estado("En Proceso")
    
    def obtener_resueltas(self):
        """Obtiene solo incidencias resueltas"""
        return self.obtener_por_estado("Resuelta")