"""
ConductoresService - Lógica de negocio de Conductores

RESPONSABILIDADES:
- Validaciones de datos
- Generación de contraseñas
- Orquestación entre Auth y Repository
- Aplicar reglas de negocio

NO SE ENCARGA DE:
- Manejo de UI (eso es del controlador)
- Gestión de tablas (eso es del controlador)
- Mostrar diálogos (eso es del controlador)
"""
import random
import string
from app.models.condcutor import Conductor
from app.repositories.conductor_repository import ConductorRepository
from app.services.auth_service import AuthService
from app.utils.validation_utils import ValidationUtils


class ConductoresService:
    """
    Servicio que encapsula la lógica de negocio de conductores.
    Código simple y fácil de entender.
    """
    
    def __init__(self, db_connection):
        self.repo = ConductorRepository(db_connection)
        self.auth_service = AuthService()
    
    # =========================================================================
    # VALIDACIONES
    # =========================================================================
    
    def validar_conductor(self, conductor):
        """
        Valida que un conductor tenga todos los datos correctos.
        
        Returns:
            (True, "") si es válido
            (False, "mensaje de error") si no es válido
        """
        # Validar nombre
        if not conductor.nombre or not conductor.nombre.strip():
            return (False, "El nombre es obligatorio.")
        
        # Validar DNI
        valido, mensaje = ValidationUtils.validar_dni(conductor.dni)
        if not valido:
            return (False, mensaje)
        
        # Validar email
        valido, mensaje = ValidationUtils.validar_email(conductor.email)
        if not valido:
            return (False, mensaje)
        
        # Validar teléfono
        valido, mensaje = ValidationUtils.validar_telefono(conductor.telefono)
        if not valido:
            return (False, mensaje)
        
        # Validar licencia
        if not conductor.licencia or not conductor.licencia.strip():
            return (False, "La licencia de conducir es obligatoria.")
        
        return (True, "")
    
    # =========================================================================
    # GENERACIÓN DE CONTRASEÑAS
    # =========================================================================
    
    def generar_password(self):
        """
        Genera una contraseña temporal: Fleet + 4 números aleatorios.
        
        Returns:
            String con la contraseña (ej: "Fleet1234")
        """
        numeros = ''.join(random.choices(string.digits, k=4))
        return f"Fleet{numeros}"
    
    # =========================================================================
    # CREAR CONDUCTOR
    # =========================================================================
    
    def crear_conductor(self, conductor, password):
        """
        Crea un conductor con cuenta de Firebase Auth.
        
        NOTA: Se asume que los datos ya fueron validados en el controlador.
        
        Args:
            conductor: Objeto Conductor con los datos
            password: Contraseña para la cuenta
            
        Returns:
            (True, conductor, "mensaje") si éxito
            (False, None, "mensaje de error") si falla
        """
        # 1. Crear cuenta en Auth
        try:
            resultado_auth = self.auth_service.crear_conductor(
                conductor.email.strip(),
                password
            )
            uid = resultado_auth['uid']
            conductor.id_conductor = uid
            
        except Exception as e:
            mensaje_error = self._interpretar_error_auth(e)
            return (False, None, mensaje_error)
        
        # 2. Guardar en Firebase Database
        try:
            if self.repo.guardar_nuevo_conductor(conductor):
                return (True, conductor, "Conductor creado exitosamente.")
            else:
                return (False, None, "Error al guardar el perfil del conductor.")
        
        except Exception as e:
            return (False, None, f"Error al guardar: {str(e)}")
    
    # =========================================================================
    # ACTUALIZAR CONDUCTOR
    # =========================================================================
    
    def actualizar_conductor(self, conductor):
        """
        Actualiza un conductor existente.
        
        NOTA: Se asume que los datos ya fueron validados en el controlador.
        
        Args:
            conductor: Objeto Conductor con los datos actualizados
            
        Returns:
            (True, "mensaje") si éxito
            (False, "mensaje de error") si falla
        """
        # Actualizar en Firebase
        try:
            if self.repo.actualizar_conductor(conductor):
                return (True, "Conductor actualizado correctamente.")
            else:
                return (False, "Error al actualizar el conductor.")
        
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    # =========================================================================
    # ELIMINAR CONDUCTOR
    # =========================================================================
    
    def eliminar_conductor(self, id_conductor):
        """
        Elimina un conductor.
        
        Args:
            id_conductor: ID del conductor a eliminar
            
        Returns:
            (True, "mensaje") si éxito
            (False, "mensaje de error") si falla
        """
        try:
            if self.repo.eliminar_conductor(id_conductor):
                return (True, "Conductor eliminado correctamente.")
            else:
                return (False, "Error al eliminar el conductor.")
        
        except Exception as e:
            return (False, f"Error: {str(e)}")
    
    # =========================================================================
    # CONSULTAS
    # =========================================================================
    
    def obtener_todos(self):
        """Obtiene todos los conductores"""
        return self.repo.obtener_todos()
    
    def obtener_por_id(self, id_conductor):
        """Obtiene un conductor por ID"""
        return self.repo.obtener_por_id(id_conductor)
    
    def obtener_disponibles(self):
        """Obtiene solo conductores disponibles"""
        todos = self.repo.obtener_todos()
        return [c for c in todos if c.estado == "Disponible"]
    
    # =========================================================================
    # MÉTODOS AUXILIARES
    # =========================================================================
    
    def _interpretar_error_auth(self, error):
        """
        Convierte errores de Firebase Auth en mensajes amigables.
        
        Args:
            error: Excepción capturada
            
        Returns:
            Mensaje de error comprensible
        """
        error_text = str(error)
        
        if "EMAIL_EXISTS" in error_text:
            return "Ya existe una cuenta con este email."
        
        if "WEAK_PASSWORD" in error_text:
            return "La contraseña debe tener al menos 6 caracteres."
        
        if "INVALID_EMAIL" in error_text:
            return "El formato del email no es válido."
        
        return f"Error de autenticación: {error_text}"