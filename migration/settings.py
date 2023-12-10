import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())        


DB_NAME = os.getenv("DATABASE")
DB_USER = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")