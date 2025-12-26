class ConductorDAO:
    def __init__(self, db_connection):
        self.db = db_connection
        self.collection_name = "conductores"

    def insertar(self, conductor_dict):
        """Envía el diccionario a Firebase y devuelve el resultado"""
        return self.db.child(self.collection_name).push(conductor_dict)
    
    def leer_todos(self):
        """Descarga todos los conductores de la nube"""
        return self.db.child(self.collection_name).get()
    
    def eliminar(self, id_conductor):
        """Borra el nodo del conductor"""
        return self.db.child(self.collection_name).child(id_conductor).remove()

    def actualizar(self, id_conductor, datos_dict):
        """Actualiza los datos de un conductor existente"""
        return self.db.child(self.collection_name).child(id_conductor).update(datos_dict)