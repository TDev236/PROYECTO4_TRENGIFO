import os
from dotenv import load_dotenv


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY','mi_clave_secreta')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:1723KingFa@localhost/proyecto_heladeria')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    