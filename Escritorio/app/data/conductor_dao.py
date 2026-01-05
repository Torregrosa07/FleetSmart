class ConductorDAO:
    def __init__(self, db_connection):
        self.db = db_connection
        self.collection_name = "conductores"

    def insertar(self, conductor_dict):
        return self.db.child(self.collection_name).push(conductor_dict)
    
    def insertar_con_id(self, id_conductor, conductor_dict):
        
        return self.db.child(self.collection_name).child(id_conductor).set(conductor_dict)
    
    def leer_todos(self):
        return self.db.child(self.collection_name).get()
    
    def leer_por_id(self, id_conductor):
        
        return self.db.child(self.collection_name).child(id_conductor).get()
    
    def eliminar(self, id_conductor):
        return self.db.child(self.collection_name).child(id_conductor).remove()

    def actualizar(self, id_conductor, datos_dict):
        return self.db.child(self.collection_name).child(id_conductor).update(datos_dict)