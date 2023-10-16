from .articulos import Articulo
from .proveedores import Proveedor
from .marcas import Marca
from .tipos import Tipo
from sqlalchemy.orm import sessionmaker

from sqlalchemy import text

class Model():
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)
        # self.Articulo = Articulo
    
    # Recibe diccionario con todos los campos de Articulo y lo inserta en la tabla de Articulo
    def add_articulo(self, data):
        session = self.Session()
        new_articulo = Articulo(data)

        session.add(new_articulo)
        # insert(Articulo).values(data)
        session.commit()


    # Recibe una lista de diccionarios con todos los campos de Articulo y los inserta en la tabla de Articulo
    def add_multiple_articulos(self, data):
        #TODO No romper cuando haya codigo repetido + otros casos de error (tipos de datos, etc)
        session = self.Session()
        for data_articulo in data:
            new_articulo = Articulo.from_dic(data_articulo)
            session.add(new_articulo)
        session.commit()

    # Recibe un diccionario con filtros válidos, construye la query SQL y retorna lista de Articulos
    def get_articulos(self, filters={}):
        query = "SELECT * FROM Articulos"
        first_cond = True
        for k in filters.keys():
            if first_cond:
                query+=" WHERE "
            else:    
                query+=" AND "

            if k[-4:] == "_min":
                query+= f"{k[:-4]} >= {filters[k]}"

            elif k[-4:] == "_max":
                query+= f"{k[:-4]} <= {filters[k]}"
            
            else:
                query+= f"{k} LIKE '{filters[k]}%'"

            first_cond = False
        
        query+=";"

        session = self.Session()
        res = session.execute(text(query))
        session.close()

        articulos = []
        for r in res:
            data= {
                "id":r[0],
                "codigo":r[1],
                "descripcion":r[2],
                "id_proveedor":r[3],
                "id_marca":r[4],
                "id_tipo":r[5],
                "precio_lista":r[6],
                "stock":r[7],
                "pto_reposicion":r[8]
            }
            articulos.append(Articulo(data))
        
        return articulos
    

    #Recibe una TUPLA con las ID de los articulos a eliminar y los elimina de la tabla Articulo
    def delete_articulos_by_id(self, id_articulos):
        query=f"DELETE FROM Articulos WHERE id IN ({', '.join(map(str,id_articulos))});"

        session = self.Session()
        r=session.execute(text(query))
        session.commit()
        session.close()

    def update_articulo(self, values):
        session = self.Session()
        articulo = session.query(Articulo).get(values["id"])
        if articulo:
            articulo.update_data(values)
            session.commit()

    def get_proveedores(self):
        session = self.Session()
        res = session.query(Proveedor)
        session.close()
        return res
    
    def get_marcas(self):
        session = self.Session()
        res = session.query(Marca)
        session.close()
        return res
    
    def get_tipos(self):
        session = self.Session()
        res = session.query(Tipo)
        session.close()
        return res
