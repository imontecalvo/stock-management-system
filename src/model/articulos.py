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
    iva = Column(Integer())
    d1 = Column(Integer())
    d2 = Column(Integer())
    d3 = Column(Integer())
    d4 = Column(Integer())
    g1 = Column(Integer())
    g2 = Column(Integer())
    g3 = Column(Integer())
    g4 = Column(Integer())


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
        self.iva = data["iva"]
        self.d1 = data["d1"]
        self.d2 = data["d2"]
        self.d3 = data["d3"]
        self.d4 = data["d4"]
        self.g1 = data["g1"]
        self.g2 = data["g2"]
        self.g3 = data["g3"]
        self.g4 = data["g4"]
        
    def update_data(self, data):
        self.codigo=data["codigo"]
        self.descripcion=data["descripcion"]
        self.id_proveedor=data["id_proveedor"]
        self.id_marca=data["id_marca"]
        self.id_tipo=data["id_tipo"]
        self.precio_lista=data["precio_lista"]
        self.stock=data["stock"]
        self.pto_reposicion=data["pto_reposicion"]
        self.iva = data["iva"]
        self.d1 = data["d1"]
        self.d2 = data["d2"]
        self.d3 = data["d3"]
        self.d4 = data["d4"]
        self.g1 = data["g1"]
        self.g2 = data["g2"]
        self.g3 = data["g3"]
        self.g4 = data["g4"]