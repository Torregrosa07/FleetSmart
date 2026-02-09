
from app.models.asignacion import Asignacion
from app.repositories.asignacion_repository import AsignacionRepository
from app.repositories.ruta_repository import RutaRepository
from app.repositories.conductor_repository import ConductorRepository
from app.repositories.vehiculo_repository import VehiculoRepository


class AsignacionesService:
    
    def __init__(self, db_connection):
        self.repo_asignacion = AsignacionRepository(db_connection)
        self.repo_rutas = RutaRepository(db_connection)
        self.repo_conductores = ConductorRepository(db_connection)
        self.repo_vehiculos = VehiculoRepository(db_connection)
    
    # =========================================================================
    # VALIDACIONES
    # =========================================================================
    
    def validar_asignacion_basica(self, id_ruta, id_conductor, id_vehiculo):
        """
        Validación básica de que los IDs están presentes.
        
        Returns:
            (True, "") si válido
            (False, "mensaje") si inválido
        """
        if not id_ruta:
            return (False, "Selecciona una ruta.")
        
        if not id_conductor:
            return (False, "Selecciona un conductor.")
        
        if not id_vehiculo:
            return (False, "Selecciona un vehículo.")
        
        return (True, "")
    
    def validar_ruta_disponible(self, id_ruta, nombre_ruta):
        """
        Valida que la ruta no esté ya asignada.
        
        Returns:
            (True, "") si disponible
            (False, "mensaje") si ya asignada
        """
        if self.repo_asignacion.ruta_tiene_asignacion(id_ruta):
            return (
                False, 
                f"La ruta '{nombre_ruta}' ya está asignada.\n\n"
                "Primero elimina la asignación existente."
            )
        
        return (True, "")
    
    def validar_conductor(self, id_conductor, nombre_conductor):
        """
        Valida el estado del conductor.
        
        REGLA DE NEGOCIO: Un conductor puede ser reasignado.
        
        Returns:
            (True, "", None) si está libre
            (True, "pregunta", nombre_ruta_actual) si ya tiene asignación (permitir reasignación)
        """
        tiene_ruta, ruta_actual = self.repo_asignacion.conductor_tiene_asignacion_activa(id_conductor)
        
        if tiene_ruta:
            mensaje = (
                f"El conductor '{nombre_conductor}' ya tiene asignada la ruta:\n"
                f"'{ruta_actual}'\n\n"
                "¿Quieres reasignarlo a esta nueva ruta?\n"
                "(La asignación anterior se eliminará)"
            )
            return (True, mensaje, ruta_actual)
        
        return (True, "", None)
    
    def validar_vehiculo(self, id_vehiculo, matricula):
        """
        Valida el estado del vehículo.
        
        REGLA DE NEGOCIO: Un vehículo NO puede ser reasignado automáticamente.
        
        Returns:
            (True, "") si está libre
            (False, "mensaje") si ya tiene asignación
        """
        tiene_ruta, ruta_actual = self.repo_asignacion.vehiculo_tiene_asignacion_activa(id_vehiculo)
        
        if tiene_ruta:
            return (
                False,
                f"El vehículo {matricula} ya está asignado a:\n"
                f"'{ruta_actual}'\n\n"
                "Selecciona otro vehículo o elimina la asignación existente."
            )
        
        return (True, "")
    
    # =========================================================================
    # CREAR ASIGNACIÓN
    # =========================================================================
    
    def crear_asignacion(self, asignacion):
        """
        Crea una nueva asignación.
        
        NOTA: Se asume que las validaciones ya se hicieron en el controlador.
        
        Args:
            asignacion: Objeto Asignacion con los datos
            
        Returns:
            (True, asignacion, "mensaje") si éxito
            (False, None, "mensaje de error") si falla
        """
        try:
            if self.repo_asignacion.guardar_asignacion(asignacion):
                return (True, asignacion, "Ruta asignada correctamente.")
            else:
                return (False, None, "Error al guardar la asignación.")
        
        except Exception as e:
            return (False, None, f"Error: {str(e)}")
    
    # =========================================================================
    # ELIMINAR ASIGNACIÓN
    # =========================================================================
    
    def eliminar_asignacion(self, id_asignacion):
        """
        Elimina una asignación.
        
        Args:
            id_asignacion: ID de la asignación a eliminar
            
        Returns:
            (True, "mensaje") si éxito
            (False, "mensaje de error") si falla
        """
        try:
            if self.repo_asignacion.eliminar_asignacion(id_asignacion):
                return (True, "Asignación eliminada correctamente.")
            else:
                return (False, "Error al eliminar la asignación.")
        
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    # =========================================================================
    # CONSULTAS
    # =========================================================================
    
    def obtener_todas(self):
        """Obtiene todas las asignaciones"""
        return self.repo_asignacion.obtener_todas()
    
    def obtener_todas_rutas(self):
        """Obtiene todas las rutas"""
        return self.repo_rutas.obtener_todas()
    
    def obtener_todos_conductores(self):
        """Obtiene todos los conductores"""
        return self.repo_conductores.obtener_todos()
    
    def obtener_todos_vehiculos(self):
        """Obtiene todos los vehículos"""
        return self.repo_vehiculos.obtener_todos()
    
    def obtener_vehiculos_disponibles(self):
        """Obtiene solo vehículos con estado Disponible"""
        todos = self.repo_vehiculos.obtener_todos()
        return [v for v in todos if getattr(v, 'estado', 'Disponible') == "Disponible"]
    
    def obtener_ruta_por_id(self, id_ruta):
        """Obtiene una ruta por ID"""
        return self.repo_rutas.obtener_por_id(id_ruta)
    
    def obtener_conductor_por_id(self, id_conductor):
        """Obtiene un conductor por ID"""
        return self.repo_conductores.obtener_por_id(id_conductor)
    
    def obtener_vehiculo_por_id(self, id_vehiculo):
        """Obtiene un vehículo por ID"""
        return self.repo_vehiculos.obtener_por_id(id_vehiculo)