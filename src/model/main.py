from .articulos import Articulo
from .proveedores import Proveedor
from .marcas import Marca
from .tipos import Tipo
from utils.response import Response

from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


class Model():
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)
        # self.Articulo = Articulo
    
    # Recibe diccionario con todos los campos de Articulo y lo inserta en la tabla de Articulo
    def add_articulo(self, data):
        try:
            session = self.Session()
            new_articulo = Articulo(data)
            session.add(new_articulo)
            session.commit()
            return Response(True)
        except:
            return Response(False, "ERROR: No se pudo añadir el artículo.")

    # Recibe una lista de diccionarios con todos los campos de Articulo y los inserta en la tabla de Articulo
    def add_multiple_articulos(self, data):
        #TODO No romper cuando haya codigo repetido + otros casos de error (tipos de datos, etc)
        try:
            session = self.Session()
            for data_articulo in data:
                new_articulo = Articulo.from_dic(data_articulo)
                session.add(new_articulo)
            session.commit()
            return Response(True)
        except:
            return Response(False, "ERROR: No se pudieron añadir todos los artículos.")


    def __get_select_query(self,filters={}):
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
            
            if filters[k]==None:
                query+= f"{k} IS NULL"

            else:
                query+= f"{k} LIKE '{filters[k]}%'"

            first_cond = False
        
        query+=";"
        return query

    # Recibe un diccionario con filtros válidos, construye la query SQL y retorna lista de Articulos
    def get_articulos(self, filters={}):
        query = self.__get_select_query(filters)

        try:
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

            return Response(True, articulos)
        except:
            return Response(False,"ERROR: No se pudo obtener todos los artículos.")
    

    #Recibe una TUPLA con las ID de los articulos a eliminar y los elimina de la tabla Articulo
    def delete_articulos_by_id(self, id_articulos):
        query=f"DELETE FROM Articulos WHERE id IN ({', '.join(map(str,id_articulos))});"

        try:
            session = self.Session()
            r=session.execute(text(query))
            session.commit()
            session.close()
            return Response(True)       
        except:
            return Response(False,"ERROR: No se pudo eliminar los artículos seleccionados.")


    #Recibe un diccionario 'values' con todos los campos con los valores nuevos y la actualiza en la base de datos
    def update_articulo(self, values):
        try:
            session = self.Session()
            articulo = session.query(Articulo).get(values["id"])
            if articulo:
                articulo.update_data(values)
                session.commit()
            return Response(True)            
        except:
            return Response(False,"ERROR: No se pudo actualizar el artículo.")


    #Devuelve una lista con todos los proveedores 
    def get_proveedores(self):
        try:
            session = self.Session()
            res = session.query(Proveedor)
            session.close()
            return Response(True, res)
        except:
            return Response(False,"ERROR: No se pudo cargar los proveedores.")
        
    
    #Devuelve una lista con todas las marcas
    def get_marcas(self):
        try:
            session = self.Session()
            res = session.query(Marca)
            session.close()
            return Response(True, res)
        except:
            return Response(False,"ERROR: No se pudo cargar las marcas.")


    #Devuelve una lista con todos los tipos
    def get_tipos(self):
        try:
            session = self.Session()
            res = session.query(Tipo)
            session.close()
            return Response(True, res)
        except:
            return Response(False,"ERROR: No se pudo cargar los tipos.")

    # Recibe diccionario con todos los campos de Articulo y lo inserta en la tabla de Articulo
    def add_proveedor(self, name):
        try:
            session = self.Session()
            new_proveedor = Proveedor(name)
            x = session.add(new_proveedor)
            y = session.commit()
            print(x)
            print(y)
            return Response(True)
        except:
            return Response(False, "ERROR: No se pudo añadir el proveedor.")