class Controller():
    def __init__(self, model):
        self.model=model

    def add_articulo(self, articulo):
        self.model.add_articulo(articulo)