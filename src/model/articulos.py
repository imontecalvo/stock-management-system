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
    d1 = Column(Integer())
    d2 = Column(Integer())
    d3 = Column(Integer())
    d4 = Column(Integer())
    iva = Column(Integer())
    precio_costo = Column(Integer())
    g1 = Column(Integer())
    g2 = Column(Integer())
    g3 = Column(Integer())
    g4 = Column(Integer())
    precio_venta = Column(Integer())
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
        self.d1 = data["d1"]
        self.d2 = data["d2"]
        self.d3 = data["d3"]
        self.d4 = data["d4"]
        self.iva = data["iva"]
        self.g1 = data["g1"]
        self.g2 = data["g2"]
        self.g3 = data["g3"]
        self.g4 = data["g4"]
        self.stock=data["stock"]
        self.pto_reposicion=data["pto_reposicion"]
        self.calculate_prices()
        
    def update_data(self, data):
        self.codigo=data["codigo"]
        self.descripcion=data["descripcion"]
        self.id_proveedor=data["id_proveedor"]
        self.id_marca=data["id_marca"]
        self.id_tipo=data["id_tipo"]
        self.precio_lista=data["precio_lista"]
        self.d1 = data["d1"]
        self.d2 = data["d2"]
        self.d3 = data["d3"]
        self.d4 = data["d4"]
        self.iva = data["iva"]
        self.g1 = data["g1"]
        self.g2 = data["g2"]
        self.g3 = data["g3"]
        self.g4 = data["g4"]
        self.stock=data["stock"]
        self.pto_reposicion=data["pto_reposicion"]
        self.calculate_prices()

    def calculate_prices(self):
        self.precio_costo = self.precio_lista
        for d in [self.d1, self.d2, self.d3, self.d4]:
            self.precio_costo -= (self.precio_costo*d/100)

        self.precio_costo += (self.precio_costo*self.iva/100)

        self.precio_venta = self.precio_costo
        for g in [self.g1, self.g2, self.g3, self.g4]:
            self.precio_venta += (self.precio_venta*g/100)
        
        self.precio_costo = round(self.precio_costo,2)
        self.precio_venta = round(self.precio_venta,2)