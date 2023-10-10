from model.main import Model
from view.main import View
from controller.main import Controller

from sqlalchemy import create_engine, text
from utils.db import db


class App():
    def __init__(self):
        try:
            engine = self.connect_db()
        except:
            #TODO Mostrar error por pantalla -> conectar con Vista
            print("ERROR: No se pudo conectar a la base de datos")
            return

        self.model=Model(engine)
        self.controller=Controller(self.model)
        self.view=View(self.controller)

    def connect_db(self):
        user="root"
        password="root"
        db_name="Gestor"
        database_url = f"mysql+pymysql://{user}:{password}@localhost:3306/"
        engine = create_engine(database_url)

        connection = engine.connect()
        create_database_sql = "CREATE DATABASE IF NOT EXISTS Gestor;"
        connection.execute(text(create_database_sql))

        engine = create_engine(database_url+db_name)
        
        db.metadata.create_all(engine)

        return engine

    def run(self):
        self.view.start()