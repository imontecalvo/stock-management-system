from .articulos import Articulo
from sqlalchemy.orm import sessionmaker

from sqlalchemy import insert

class Model():
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)
        # self.Articulo = Articulo
    
    # Recibe diccionario con todos los campos de Articulo y lo inserta en la tabla de Articulo
    def add_articulo(self, data):
        print(f"Data: {data}")
        session = self.Session()
        new_articulo = Articulo(data)
        print(f"Articulo: {new_articulo}")

        session.add(new_articulo)
        # insert(Articulo).values(data)
        session.commit()


    # Recibe una lista de diccionarios con todos los campos de Articulo y los inserta en la tabla de Articulo
    def add_multiple_articulos(self, data):
        session = self.Session()
        for data_articulo in data:
            new_articulo = Articulo.from_dic(data_articulo)
            session.add(new_articulo)
        session.commit()