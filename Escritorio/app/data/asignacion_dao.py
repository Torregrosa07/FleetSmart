class AsignacionDAO:
    def __init__(self, db_connection):
        self.db = db_connection
        self.collection_name = "asignaciones"

    def insertar(self, data):
        return self.db.child(self.collection_name).push(data)

    def leer_todos(self):
        return self.db.child(self.collection_name).get()