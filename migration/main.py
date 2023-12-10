# import pandas as pd
import psycopg2
from flask import Flask, jsonify
import sqlite3

# Connection Testing
conn = psycopg2.connect(database="games_db", user="postgres", password="afrocs221994")
cursor = conn.cursor()
cursor.execute("SELECT * FROM champion_stats;")
rows = cursor.fetchall()

# Flask App

app = Flask(__name__)


@app.route('/champions')
def champions():
    conn = psycopg2.connect(database="games_db", user="postgres", password="afrocs221994")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM champion_stats;")
    rows = cursor.fetchall()
    return jsonify(rows)

@app.route('/champions/<champ_name>')
def search_by_champ_name(champ_name):
    conn = psycopg2.connect(database="games_db", user="postgres", password="afrocs221994")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM champion_stats WHERE name ILIKE %s;", (champ_name,))
    champ = cursor.fetchone()
    return jsonify(champ)

@app.route('/champions/by_class/<champ_class>')
def search_by_class(champ_class):
    conn = psycopg2.connect(database="games_db", user="postgres", password="afrocs221994")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM champion_stats WHERE class ILIKE %s;", (champ_class,))
    champs_by_class = cursor.fetchall()
    return jsonify(champs_by_class)

# cursor.execute(f"SELECT * FROM movies WHERE genre = %s;", (genre,))
    # movies = cursor.fetchall()

app.run(debug= True)

