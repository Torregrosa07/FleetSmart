from app.data.conductor_dao import ConductorDAO
from app.models.condcutor import Conductor

class ConductorRepository:
    def __init__(self, db_connection):
        self.dao = ConductorDAO(db_connection)

    def guardar_nuevo_conductor(self, conductor_obj):
        try:
            # 1. Convertimos el objeto Modelo a Diccionario
            datos = conductor_obj.to_dict()
            
            # 2. Usamos el DAO para enviar los datos
            resultado = self.dao.insertar(datos)
            
            print(f"Éxito: Conductor guardado con ID: {resultado['name']}")
            return True
        except Exception as e:
            print(f"Error al guardar: {e}") 
            
            
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