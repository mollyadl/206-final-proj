# # SI 206: COVID-19 Final Project
# # Group Members: Molly Adler and Felicia Chen
# # API Link (1 of 2): 

import sqlite3
import requests

def create_database():
    conn = sqlite3.connect("covid_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DailyStats (
            date INTEGER PRIMARY KEY,
            states INTEGER,
            positive INTEGER,
            negative INTEGER,
            death INTEGER,
            totalTestResults INTEGER
        )
    ''')

    # Create HospitalData table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HospitalData (
            date INTEGER PRIMARY KEY,
            hospitalizedCurrently INTEGER,
            hospitalizedCumulative INTEGER,
            inIcuCurrently INTEGER,
            onVentilatorCurrently INTEGER,
            FOREIGN KEY(date) REFERENCES DailyStats(date)
        )
    ''')

    conn.commit()
    conn.close()

def insert_data_from_api(api_url, limit=25):
    conn = sqlite3.connect("covid_data.db")
    cursor = conn.cursor()
    response = requests.get(api_url)
    if response.status_code != 200:
        print("Failed to fetch data from API")
        return

    data = response.json()
    count = 0

    for row in data:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO DailyStats (date, states, positive, negative, death, totalTestResults)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (int(row['date']), int(row.get('states', 0)), int(row.get('positive', 0)), int(row.get('negative', 0)),
                  int(row.get('death', 0)), int(row.get('totalTestResults', 0))))

            cursor.execute('''
                INSERT OR IGNORE INTO HospitalData (date, hospitalizedCurrently, hospitalizedCumulative, inIcuCurrently, onVentilatorCurrently)
                VALUES (?, ?, ?, ?, ?)
            ''', (int(row['date']), int(row.get('hospitalizedCurrently', 0)),
                  int(row.get('hospitalizedCumulative', 0)), int(row.get('inIcuCurrently', 0)),
                  int(row.get('onVentilatorCurrently', 0))))

            count += 1
            if count >= limit:
                break
        except ValueError:
            continue

    conn.commit()
    conn.close()

def populate_database(api_url, total_required=100, batch_size=25):
    conn = sqlite3.connect("covid_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM DailyStats")
    current_count = cursor.fetchone()[0]

    conn.close()

    while current_count < total_required:
        insert_data_from_api(api_url, limit=batch_size)
        conn = sqlite3.connect("covid_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM DailyStats")
        current_count = cursor.fetchone()[0]
        conn.close()

# Create the database and tables
create_database()

api_url = 'https://api.covidtracking.com/v1/us/daily.json'
populate_database(api_url, total_required=100, batch_size=25)


