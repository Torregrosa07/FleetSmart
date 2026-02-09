"""
VehiculosService - Lógica de negocio de Vehículos

RESPONSABILIDADES:
- Validaciones de datos
- Operaciones CRUD con el repositorio
- Aplicar reglas de negocio

NO SE ENCARGA DE:
- Manejo de UI
- Gestión de tablas
- Mostrar diálogos
"""
from app.models.vehiculo import Vehiculo
from app.repositories.vehiculo_repository import VehiculoRepository
from app.utils.validation_utils import ValidationUtils


class VehiculosService:
    """
    Servicio que encapsula la lógica de negocio de vehículos.
    """
    
    def __init__(self, db_connection):
        self.repo = VehiculoRepository(db_connection)
    
    # =========================================================================
    # VALIDACIONES
    # =========================================================================
    
    def validar_vehiculo(self, vehiculo):
        """
        Valida que un vehículo tenga todos los datos correctos.
        
        Returns:
            (True, "") si es válido
            (False, "mensaje de error") si no es válido
        """
        # Validar matrícula
        valido, mensaje = ValidationUtils.validar_matricula(vehiculo.matricula)
        if not valido:
            return (False, mensaje)
        
        # Validar marca
        if not vehiculo.marca or not vehiculo.marca.strip():
            return (False, "La marca es obligatoria.")
        
        # Validar modelo
        if not vehiculo.modelo or not vehiculo.modelo.strip():
            return (False, "El modelo es obligatorio.")
        
        # Validar estado
        if not vehiculo.estado or not vehiculo.estado.strip():
            return (False, "El estado es obligatorio.")
        
        # Validar año (debe ser un número positivo razonable)
        if vehiculo.ano <= 0:
            return (False, "El año debe ser un número positivo.")
        
        if vehiculo.ano < 1900 or vehiculo.ano > 2100:
            return (False, "El año debe estar entre 1900 y 2100.")
        
        # Validar kilómetros (debe ser positivo o cero)
        if vehiculo.km_actuales < 0:
            return (False, "Los kilómetros no pueden ser negativos.")
        
        # Validar próxima ITV (opcional, pero si existe debe tener formato válido)
        if vehiculo.proxima_itv and vehiculo.proxima_itv.strip():
            # Validación básica de formato fecha
            if len(vehiculo.proxima_itv.strip()) < 8:
                return (False, "La fecha de ITV debe tener formato válido (ej: 15/06/2025).")
        
        return (True, "")
    
    # =========================================================================
    # CREAR VEHÍCULO
    # =========================================================================
    
    def crear_vehiculo(self, vehiculo):
        """
        Crea un nuevo vehículo.
        
        NOTA: Se asume que los datos ya fueron validados en el controlador.
        
        Args:
            vehiculo: Objeto Vehiculo con los datos
            
        Returns:
            (True, vehiculo, "mensaje") si éxito
            (False, None, "mensaje de error") si falla
        """
        try:
            if self.repo.guardar_nuevo_vehiculo(vehiculo):
                return (True, vehiculo, "Vehículo creado exitosamente.")
            else:
                return (False, None, "Error al guardar el vehículo.")
        
        except Exception as e:
            return (False, None, f"Error: {str(e)}")
    
    # =========================================================================
    # ACTUALIZAR VEHÍCULO
    # =========================================================================
    
    def actualizar_vehiculo(self, vehiculo):
        """
        Actualiza un vehículo existente.
        
        NOTA: Se asume que los datos ya fueron validados en el controlador.
        
        Args:
            vehiculo: Objeto Vehiculo con los datos actualizados
            
        Returns:
            (True, "mensaje") si éxito
            (False, "mensaje de error") si falla
        """
        try:
            if self.repo.actualizar_vehiculo(vehiculo):
                return (True, "Vehículo actualizado correctamente.")
            else:
                return (False, "Error al actualizar el vehículo.")
        
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    # =========================================================================
    # ELIMINAR VEHÍCULO
    # =========================================================================
    
    def eliminar_vehiculo(self, id_vehiculo):
        """
        Elimina un vehículo.
        
        Args:
            id_vehiculo: ID del vehículo a eliminar
            
        Returns:
            (True, "mensaje") si éxito
            (False, "mensaje de error") si falla
        """
        try:
            if self.repo.eliminar_vehiculo(id_vehiculo):
                return (True, "Vehículo eliminado correctamente.")
            else:
                return (False, "Error al eliminar el vehículo.")
        
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    # =========================================================================
    # CONSULTAS
    # =========================================================================
    
    def obtener_todos(self):
        """Obtiene todos los vehículos"""
        return self.repo.obtener_todos()
    
    def obtener_por_id(self, id_vehiculo):
        """Obtiene un vehículo por ID"""
        return self.repo.obtener_por_id(id_vehiculo)
    
    def obtener_disponibles(self):
        """Obtiene solo vehículos disponibles"""
        todos = self.repo.obtener_todos()
        return [v for v in todos if v.estado == "Disponible"]