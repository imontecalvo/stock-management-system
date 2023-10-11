class Controller():
    def __init__(self, model):
        self.model=model

    def add_articulo(self, articulo):
        self.model.add_articulo(articulo)

    # Recibe lista de filtros, los chequea y hace casteos y devuelve lista de Articulos
    def get_articulos(self, filters={}):
        filter_by = ["descripcion","id_proveedor","id_marca","id_tipo","precio_min","precio_max"]
        for k in filters.keys():
            if not k in filter_by or filters[k] == "":
                del filters[k]

            if k in filter_by[1:]:
                filters[k]=int(filters[k])

        return self.model.get_articulos(filters)
        