from app.data.conductor_dao import ConductorDAO
from app.models.condcutor import Conductor

class ConductorRepository:
    def __init__(self, db_connection):
        self.dao = ConductorDAO(db_connection)

    def guardar_nuevo_conductor(self, conductor_obj):
        """
        Guarda un nuevo conductor en Firebase.
        """
        try:
            # Convertir el objeto a diccionario
            datos = conductor_obj.to_dict()
            
            # Si tiene UID de Auth, usar ese ID específico
            if conductor_obj.id_conductor:
                self.dao.insertar_con_id(conductor_obj.id_conductor, datos)
                print(f"✅ Conductor guardado con UID: {conductor_obj.id_conductor}")
            else:
                # Si no tiene UID, generar uno automático (modo legacy)
                resultado = self.dao.insertar(datos)
                print(f"✅ Conductor guardado con ID auto-generado: {resultado['name']}")
            
            return True
        except Exception as e:
            print(f"❌ Error al guardar conductor: {e}") 
            return False
            
    def obtener_todos(self):
        """Devuelve una lista de objetos Conductor"""
        lista = []
        try:
            respuesta = self.dao.leer_todos()
            
            if respuesta.each():
                for item in respuesta.each():
                    id_firebase = item.key() 
                    datos = item.val() 
                    
                    conductor = Conductor.from_dict(id_firebase, datos)
                    lista.append(conductor)
                    
        except Exception as e:
            print(f"Error al obtener datos (puede que esté vacía): {e}")
            
        return lista
    
    def obtener_por_id(self, id_conductor):
        """
        Obtiene un conductor específico por su ID.
        """
        try:
            respuesta = self.dao.leer_por_id(id_conductor)
            
            if respuesta.val():
                return Conductor.from_dict(id_conductor, respuesta.val())
            else:
                return None
                
        except Exception as e:
            print(f"Error al obtener conductor por ID: {e}")
            return None
    
    def eliminar_conductor(self, id_conductor):
        try:
            self.dao.eliminar(id_conductor)
            return True
        except Exception as e:
            print(f"Error al eliminar: {e}")
            return False

    def actualizar_conductor(self, conductor_obj):
        try:
            # Importante: Usamos el ID del objeto para saber cuál actualizar
            datos = conductor_obj.to_dict()
            self.dao.actualizar(conductor_obj.id_conductor, datos)
            return True
        except Exception as e:
            print(f"Error al actualizar: {e}")
            return False
