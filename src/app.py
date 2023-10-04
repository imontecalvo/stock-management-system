from model.main import Model
from view.main import View
from controller.main import Controller

class App():
    def __init__(self):
        self.model=Model()
        self.controller=Controller(self.model)
        self.view=View(self.controller)

    def connect_db(self):
        pass

    def run(self):
        self.view.start()