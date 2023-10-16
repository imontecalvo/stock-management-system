from sqlalchemy import Column, Integer, String
from utils.db import db

class Proveedor(db):
    __tablename__ = "Proveedores"

    id = Column(Integer(), primary_key=True)
    nombre = Column(String(255),nullable=False, unique=True)


    def __init__(self, name, id=None):
        #TODO agregar chequeo campos
        if id:
            self.id=id
        self.nombre=name
        
    def update_data(self, name):
        self.codigo=name