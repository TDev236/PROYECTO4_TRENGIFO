import os
from dotenv import load_dotenv
import pymysql

pymysql.install_as_MySQLdb()


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY','mi_clave_secreta')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")