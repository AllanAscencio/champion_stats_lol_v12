import psycopg2
from migration.settings import *
from decimal import Decimal


class Champion:
    @staticmethod
    def all_stats():
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()
        cursor.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'champion_stats'")
        stats = cursor.fetchall()
        cleaned_stats = [item[0] for item in stats]
        return cleaned_stats

    @staticmethod
    def search_champ_stats(champ_name):
        stats = Champion.all_stats()
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM champion_stats WHERE name ILIKE %s", (champ_name,))
        champ = cursor.fetchone()
        if champ:
            result_dict = {stat[0]: Champion.clean_stat_value(stat[1]) for stat in zip(stats, champ)}
            return result_dict
        else:
            return None
        
    @staticmethod
    def clean_stat_value(value):
        if isinstance(value, Decimal):
            return f'{value:.2f}%'
        else:
            return value

    @staticmethod
    def all_champs():
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM champion_stats")
        champions = cursor.fetchall()
        if champions:
            result_dict = [champ[0] for champ in champions]
            return result_dict
        else:
            return None
       

