# import pandas as pd
import psycopg2

conn = psycopg2.connect(database="games_db", user="postgres", password="afrocs221994")
cursor = conn.cursor()
cursor.execute("SELECT * FROM champion_stats;")
rows = cursor.fetchall()

for row in rows:
    print(row)
