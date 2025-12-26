from app.data.vehiculo_dao import VehiculoDAO
from app.models.vehiculo import Vehiculo

class VehiculoRepository:
    def __init__(self, db_connection):
        self.dao = VehiculoDAO(db_connection)

    def guardar_nuevo_vehiculo(self, vehiculo_obj):
        try:
            # 1. Convertimos el objeto Modelo a Diccionario
            datos = vehiculo_obj.to_dict()
            
            # 2. Usamos el DAO para enviar los datos
            resultado = self.dao.insertar(datos)
            
            print(f"Éxito: Vehículo guardado con ID: {resultado['name']}")
            return True
        except Exception as e:
            print(f"Error al guardar: {e}") 
            
            
    def obtener_todos(self):
        """Devuelve una lista de objetos Vehiculo"""
        lista = []
        try:
            respuesta = self.dao.leer_todos()
            
            if respuesta.each():
                for item in respuesta.each():
                    id_firebase = item.key() 
                    datos = item.val() # el diccionario con matrícula, etc.
                    
                    vehiculo = Vehiculo.from_dict(id_firebase, datos)
                    lista.append(vehiculo)
                    
        except Exception as e:
            print(f"Error al obtener datos (puede que esté vacía): {e}")
            
        return lista
    
    
    def eliminar_vehiculo(self, id_vehiculo):
        try:
            self.dao.eliminar(id_vehiculo)
            return True
        except Exception as e:
            print(f"Error al eliminar: {e}")
            return False


    def actualizar_vehiculo(self, vehiculo_obj):
        try:
            # Importante: Usamos el ID del objeto para saber cuál actualizar
            datos = vehiculo_obj.to_dict()
            self.dao.actualizar(vehiculo_obj.id_vehiculo, datos)
            return True
        except Exception as e:
            print(f"Error al actualizar: {e}")
            return False