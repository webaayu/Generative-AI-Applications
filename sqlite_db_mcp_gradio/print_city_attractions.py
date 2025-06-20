import sqlite3

DB_PATH = "city_attractions.db"

def print_attractions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT city, attraction FROM attractions ORDER BY city")
    rows = cursor.fetchall()

    if not rows:
        print("No data found in city_attractions.db.")
    else:
        print("📍 City Attractions:\n")
        for city, attraction in rows:
            print(f"City: {city.title()} — Attraction: {attraction}")

    conn.close()

if __name__ == "__main__":
    print_attractions()
