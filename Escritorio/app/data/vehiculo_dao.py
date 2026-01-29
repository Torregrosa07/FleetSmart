class VehiculoDAO:
    def __init__(self, db_connection):
        self.db = db_connection
        self.collection_name = "vehiculos"

    def insertar(self, vehiculo_dict):
        """Envía el diccionario a Firebase y devuelve el resultado"""
        return self.db.child(self.collection_name).push(vehiculo_dict)
    
    def leer_todos(self):
        """Descarga todos los vehículos de la nube"""
        return self.db.child(self.collection_name).get()
    
    def leer_uno(self, id_vehiculo):
        """Obtiene un vehículo específico por su ID"""
        return self.db.child(self.collection_name).child(id_vehiculo).get().val()
    
    def eliminar(self, id_vehiculo):
        """Borra el nodo del vehículo"""
        return self.db.child(self.collection_name).child(id_vehiculo).remove()

    def actualizar(self, id_vehiculo, datos_dict):
        """Actualiza los datos de un vehículo existente"""
        return self.db.child(self.collection_name).child(id_vehiculo).update(datos_dict)