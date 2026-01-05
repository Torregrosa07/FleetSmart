from app.data.gestor_dao import GestorDAO
from app.models.gestor import Gestor

class GestorRepository:
    """
    Repositorio para la entidad Gestor.
    Contiene la lógica de negocio y convierte entre objetos Gestor y datos de Firebase.
    """
    
    def __init__(self, db_connection):
        """
        Inicializa el repositorio con la conexión a Firebase.
        
        Args:
            db_connection: Conexión a Firebase Database
        """
        self.dao = GestorDAO(db_connection)

    def guardar_nuevo_gestor(self, gestor_obj):
        """
        Guarda un nuevo gestor en Firebase.
        IMPORTANTE: Este método asume que el gestor ya tiene un id_gestor
        (el UID de Firebase Auth).
        
        Args:
            gestor_obj: Objeto Gestor a guardar
        
        Returns:
            True si se guardó correctamente, False si hubo error
        """
        try:
            if not gestor_obj.id_gestor:
                print("Error: El gestor debe tener un id_gestor (UID de Firebase Auth)")
                return False
            
            # Convertimos el objeto a diccionario
            datos = gestor_obj.to_dict()
            
            # Guardamos con el UID específico
            self.dao.insertar_con_id(gestor_obj.id_gestor, datos)
            
            print(f"Éxito: Gestor guardado con ID: {gestor_obj.id_gestor}")
            return True
        except Exception as e:
            print(f"Error al guardar gestor: {e}") 
            return False
            
    def obtener_todos(self):
        """
        Obtiene todos los gestores de Firebase.
        
        Returns:
            Lista de objetos Gestor
        """
        lista = []
        try:
            respuesta = self.dao.leer_todos()
            
            if respuesta.each():
                for item in respuesta.each():
                    id_firebase = item.key() 
                    datos = item.val() 
                    
                    gestor = Gestor.from_dict(id_firebase, datos)
                    lista.append(gestor)
                    
        except Exception as e:
            print(f"Error al obtener gestores (puede que esté vacía): {e}")
            
        return lista
    
    def obtener_por_id(self, id_gestor):
        """
        Obtiene un gestor específico por su ID.
        
        Args:
            id_gestor: ID del gestor a buscar
        
        Returns:
            Objeto Gestor si existe, None si no existe
        """
        try:
            respuesta = self.dao.leer_por_id(id_gestor)
            
            if respuesta.val():
                return Gestor.from_dict(id_gestor, respuesta.val())
            else:
                return None
                
        except Exception as e:
            print(f"Error al obtener gestor por ID: {e}")
            return None
    
    def eliminar_gestor(self, id_gestor):
        """
        Elimina un gestor de Firebase.
        
        Args:
            id_gestor: ID del gestor a eliminar
        
        Returns:
            True si se eliminó correctamente, False si hubo error
        """
        try:
            self.dao.eliminar(id_gestor)
            return True
        except Exception as e:
            print(f"Error al eliminar gestor: {e}")
            return False

    def actualizar_gestor(self, gestor_obj):
        """
        Actualiza los datos de un gestor existente.
        
        Args:
            gestor_obj: Objeto Gestor con los datos actualizados
        
        Returns:
            True si se actualizó correctamente, False si hubo error
        """
        try:
            if not gestor_obj.id_gestor:
                print("Error: El gestor debe tener un id_gestor")
                return False
            
            datos = gestor_obj.to_dict()
            self.dao.actualizar(gestor_obj.id_gestor, datos)
            return True
        except Exception as e:
            print(f"Error al actualizar gestor: {e}")
            return False