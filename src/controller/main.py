from utils.response import Response

class Controller():
    def __init__(self, model):
        self.model=model

    def check_filters_articulos(self, filters={}):
        filter_by = ["codigo","descripcion","id_proveedor","id_marca","id_tipo","precio_min","precio_max"]
        useless_keys = []
        for k in filters.keys():
            if not k in filter_by or filters[k] == "":
                useless_keys.append(k)

            elif k in filter_by[2:]:#Si es un campo numerico lo casteo a int
                if filters[k]: #Puede ser None -> NULL en la tabla
                    filters[k]=int(filters[k])

        for k in useless_keys:
            del filters[k]
        
        return filters

    def get_no_articulos(self, filters={}):
        filters = self.check_filters_articulos(filters)
        return self.model.get_no_articulos(filters)

    def add_articulo(self, articulo):
        return self.model.add_articulo(articulo)

    # Recibe lista de filtros, los chequea y hace casteos y devuelve lista de Articulos
    def get_articulos(self, filters={}):
        filters = self.check_filters_articulos(filters)
        return self.model.get_articulos(filters)
        
    def get_articulos_in_range(self, limit, offset, filters={}):
        filters = self.check_filters_articulos(filters)
        return self.model.get_articulos(limit, offset, filters)

    def delete_articulos_by_id(self, id_articulos):
        if type(id_articulos) is tuple:
            return self.model.delete_articulos_by_id(id_articulos)
        else:
            return Response(False,"ERROR: No se recibió una tupla con ids de articulos")

    def update_articulo(self, values):
        return self.model.update_articulo(values)

    def get_proveedores(self):
        return self.model.get_proveedores()
    
    def get_marcas(self):
        return self.model.get_marcas()
    
    def get_tipos(self):
        return self.model.get_tipos()
    
    def add_proveedor(self, name):
        return self.model.add_proveedor(name)
    
    def add_marca(self, name):
        return self.model.add_marca(name)
    
    def add_tipo(self, name):
        return self.model.add_tipo(name)