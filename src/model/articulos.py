from sqlalchemy import Column, Integer, String, ForeignKey
from utils.db import db

class Articulo(db):
    __tablename__ = "Articulos"

    id = Column(Integer(), primary_key=True)
    codigo = Column(String(10), unique=True)
    descripcion = Column(String(255),nullable=False)
    id_proveedor = Column(Integer(),ForeignKey('Proveedores.id'))
    id_marca = Column(Integer(),ForeignKey('Marcas.id'))
    id_tipo = Column(Integer(),ForeignKey('Tipos.id'))
    precio_lista = Column(Integer())
    stock = Column(Integer(), default=0)
    pto_reposicion = Column(Integer())


    def __init__(self, data):
        #TODO agregar chequeo campos
        if "id" in data.keys():
            self.id = data["id"]
        self.codigo=data["codigo"]
        self.descripcion=data["descripcion"]
        self.id_proveedor=data["id_proveedor"]
        self.id_marca=data["id_marca"]
        self.id_tipo=data["id_tipo"]
        self.precio_lista=data["precio_lista"]
        self.stock=data["stock"]
        self.pto_reposicion=data["pto_reposicion"]
        
    def update_data(self, data):
        self.codigo=data["codigo"]
        self.descripcion=data["descripcion"]
        self.id_proveedor=data["id_proveedor"]
        self.id_marca=data["id_marca"]
        self.id_tipo=data["id_tipo"]
        self.precio_lista=data["precio_lista"]
        self.stock=data["stock"]
        self.pto_reposicion=data["pto_reposicion"]