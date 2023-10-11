from sqlalchemy import Column, Integer, String
from utils.db import db

class Articulo(db):
    __tablename__ = "Articulos"

    id = Column(Integer(), primary_key=True)
    codigo = Column(String(10), unique=True)
    descripcion = Column(String(255),nullable=False)
    id_proveedor = Column(Integer())
    id_marca = Column(Integer())
    id_tipo = Column(Integer())
    precio_lista = Column(Integer())
    stock = Column(Integer(), default=0)
    pto_reposicion = Column(Integer())


    def __init__(self, data):
        #TODO agregar chequeo campos
        self.codigo=data["codigo"]
        self.descripcion=data["descripcion"]
        self.id_proveedor=data["id_proveedor"]
        self.id_marca=data["id_marca"]
        self.id_tipo=data["id_tipo"]
        self.precio_lista=data["precio_lista"]
        self.stock=data["stock"]
        self.pto_reposicion=data["pto_reposicion"]
        