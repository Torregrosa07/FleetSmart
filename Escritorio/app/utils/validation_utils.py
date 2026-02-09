"""
ValidationUtils - Validaciones básicas y sencillas

Solo validaciones simples para evitar código duplicado en controladores.
"""
import re


class ValidationUtils:
    """
    Validaciones simples que devuelven (bool, mensaje).
    Sin complejidad, fácil de entender.
    """
    
    # =========================================================================
    # VALIDACIONES BÁSICAS
    # =========================================================================
    
    @staticmethod
    def validar_no_vacio(valor, nombre_campo="Campo"):
        """
        Valida que un campo no esté vacío.
        
        Returns:
            (True, "") si válido
            (False, "mensaje de error") si inválido
        """
        if not valor or not valor.strip():
            return (False, f"{nombre_campo} es obligatorio.")
        return (True, "")
    
    @staticmethod
    def validar_email(email):
        """
        Valida formato de email.
        
        Returns:
            (True, "") si válido
            (False, "mensaje de error") si inválido
        """
        email = email.strip()
        
        if not email:
            return (False, "El email es obligatorio.")
        
        if '@' not in email or '.' not in email:
            return (False, "El email debe tener formato válido (ejemplo@dominio.com).")
        
        return (True, "")
    
    @staticmethod
    def validar_dni(dni):
        """
        Valida que DNI tenga al menos 8 caracteres.
        
        Returns:
            (True, "") si válido
            (False, "mensaje de error") si inválido
        """
        dni = dni.strip()
        
        if not dni:
            return (False, "El DNI es obligatorio.")
        
        if len(dni) < 8:
            return (False, "El DNI debe tener al menos 8 caracteres.")
        
        return (True, "")
    
    @staticmethod
    def validar_telefono(telefono):
        """
        Valida que teléfono tenga al menos 9 dígitos.
        
        Returns:
            (True, "") si válido
            (False, "mensaje de error") si inválido
        """
        telefono = telefono.strip()
        
        if not telefono:
            return (False, "El teléfono es obligatorio.")
        
        # Quitar espacios y guiones
        telefono_limpio = telefono.replace(" ", "").replace("-", "")
        
        # Contar solo dígitos
        digitos = ''.join(c for c in telefono_limpio if c.isdigit())
        
        if len(digitos) < 9:
            return (False, "El teléfono debe tener al menos 9 dígitos.")
        
        return (True, "")
    
    @staticmethod
    def validar_matricula(matricula):
        """
        Valida que matrícula no esté vacía y tenga al menos 6 caracteres.
        
        Returns:
            (True, "") si válido
            (False, "mensaje de error") si inválido
        """
        matricula = matricula.strip()
        
        if not matricula:
            return (False, "La matrícula es obligatoria.")
        
        if len(matricula) < 6:
            return (False, "La matrícula debe tener al menos 6 caracteres.")
        
        return (True, "")