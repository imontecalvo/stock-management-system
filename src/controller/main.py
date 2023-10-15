class Controller():
    def __init__(self, model):
        self.model=model

    def add_articulo(self, articulo):
        self.model.add_articulo(articulo)

    # Recibe lista de filtros, los chequea y hace casteos y devuelve lista de Articulos
    def get_articulos(self, filters={}):
        filter_by = ["descripcion","id_proveedor","id_marca","id_tipo","precio_min","precio_max"]
        useless_keys = []
        for k in filters.keys():
            if not k in filter_by or filters[k] == "":
                useless_keys.append(k)

            elif k in filter_by[1:]:
                filters[k]=int(filters[k])

        for k in useless_keys:
            del filters[k]

        return self.model.get_articulos(filters)
        

    def delete_articulos_by_id(self, id_articulos):
        if type(id_articulos) is tuple:
            self.model.delete_articulos_by_id(id_articulos)
        else:
            #TODO Retornar error
            pass

    def update_articulo(self, values):
        self.model.update_articulo(values)