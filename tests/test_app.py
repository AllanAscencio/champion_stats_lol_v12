from models.champions import Champion
import pytest
from flask import json
import psycopg2
from migration.settings import *



def test_all_champs():
    champs_len = sorted(list(set(Champion.all_champs())))
    assert len(champs_len) == 157
    
def test_search_champ_stats():
    test_champ_list = [{'name': 'Blitzcrank', 'class': 'Tank', 'role': 'SUPPORT', 'tier': 'S', 'score': '67.80%', 'trend': '-0.81%', 'win_perc': '51.87%', 'role_perc': '99.49%', 'pick_perc': '8.61%', 'ban_perc': '18.23%', 'kda': '2.44%'},
                  {'name': 'Nasus', 'class': 'Fighter', 'role': 'TOP', 'tier': 'S', 'score': '64.96%', 'trend': '7.18%', 'win_perc': '51.83%', 'role_perc': '85.10%', 'pick_perc': '4.49%', 'ban_perc': '4.36%', 'kda': '1.98%'},
                  {'name': 'Jhin', 'class': 'Marksman', 'role': 'ADC', 'tier': 'God', 'score': '94.23%', 'trend': '3.23%', 'win_perc': '51.03%', 'role_perc': '99.02%', 'pick_perc': '24.55%', 'ban_perc': '5.81%', 'kda': '3.01%'},
                  {'name': 'Samira', 'class': 'Marksman', 'role': 'ADC', 'tier': 'B', 'score': '44.40%', 'trend': '-3.44%', 'win_perc': '48.52%', 'role_perc': '98.10%', 'pick_perc': '7.22%', 'ban_perc': '11.15%', 'kda': '2.19%'}]
    champions_names = ['Blitzcrank', 'Nasus', 'Jhin', 'Samira']
    sample_dict = []
    for i in champions_names:
        sample_dict.append(Champion.search_champ_stats(i))
    assert sample_dict == test_champ_list
    
def test_all_stats():
    test_all_stats = ['name', 'class', 'role', 'tier', 'score', 'trend', 'win_perc', 'role_perc', 'pick_perc', 'ban_perc', 'kda']
    assert test_all_stats == Champion.all_stats()


# Fixture to create a test database connection
# @pytest.fixture
# def setup_database():
#     conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE champion_stats (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     class VARCHAR(255) NOT NULL,
#     role VARCHAR(255) NOT NULL,
#     tier VARCHAR(255) NOT NULL,
#     score NUMERIC(5, 2) NOT NULL,
#     trend NUMERIC(5, 2) NOT NULL,
#     win_perc NUMERIC(5, 2) NOT NULL,
#     role_perc NUMERIC(5, 2) NOT NULL,
#     pick_perc NUMERIC(5, 2) NOT NULL,
#     ban_perc NUMERIC(5, 2) NOT NULL,
#     kda NUMERIC(5, 2) NOT NULL''')
#     yield conn
    
@pytest.fixture
def setup_database():
    conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    yield conn  # This is where the test will run
    conn.close()  # Close the connection after the test

@pytest.fixture
def setup_test_data1(setup_database):
    conn = setup_database
    cursor = conn.cursor()
    
    sample_data = [
        ('Blitzcrank', 'Tank', 'SUPPORT', 'S', 67.80, -0.81, 51.87, 99.49, 8.61, 18.23, 2.44),
        ('Nasus', 'Fighter', 'TOP', 'S', 64.96, 7.18, 51.83, 85.10, 4.49, 4.36, 1.98),
        ('Jhin', 'Marksman', 'ADC', 'God', 94.23, 3.23, 51.03, 99.02, 24.55, 5.81, 3.01),
        ('Samira', 'Marksman', 'ADC', 'B', 44.40, -3.44, 48.52, 98.10, 7.22, 11.15, 2.19)
    ]
    
    cursor.executemany("""
        INSERT INTO test_champion_stats (name, class, role, tier, score, trend, win_perc, role_perc, pick_perc, ban_perc, kda)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", sample_data)

    conn.commit()
    yield cursor
    cursor.close()

@pytest.fixture
def setup_test_data2(setup_database):
    conn = setup_database
    cursor = conn.cursor()
    
    sample_data = [
        ('Aurelion Sol', 'Mage', 'MID', 'B', 42.15, -2.74, 50.81, 91.23, 0.89, 0.25, 2.55),
        ('Annie', 'Mage', 'MID', 'A', 48.81, 6.23, 52.45, 85.00, 2.17, 0.71, 2.39),
        ('Zilean', 'Support', 'MID', 'A', 52.20, 1.35, 54.19, 14.12, 0.56, 1.40, 3.46),
        ('Brand', 'Mage', 'SUPPORT', 'B', 45.21, -4.17, 49.18, 79.04, 4.68, 5.87, 1.77),
        ('Jhin', 'Marksman', 'ADC', 'God', 94.23, 3.23, 51.03, 99.02, 24.55, 5.81, 3.01)
    ]
    clean_up_data = "DELETE * FROM test_champion_stats"
    cursor.execute(clean_up_data)
    
    sql = '''
        INSERT INTO test_champion_stats (name, class, role, tier, score, trend, win_perc, role_perc, pick_perc, ban_perc, kda)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    for record in sample_data:
        cursor.execute(sql, record)

    conn.commit()
    yield cursor
    
    final_clean_up_data = "DELETE * FROM test_champion_stats"
    cursor.execute(final_clean_up_data)

    cursor.close()

# Fixture to set up and tear down the database state for testing
def test_with_sample_data2(setup_test_data2):
    # Test to make sure that there are 5 items in the database
    cursor = setup_test_data2
    cursor.execute('SELECT * FROM test_champion_stats')
    inserted_records = cursor.fetchall()
    assert len(inserted_records) == 5

    # Optional: Print or inspect the inserted records
    print(inserted_records)


