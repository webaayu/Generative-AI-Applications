import sqlite3

# Define database file
DB_PATH = "city_attractions.db"

# Cities and their attractions
attractions_data = {
    "paris": [
        "Eiffel Tower",
        "Louvre Museum",
        "Notre-Dame Cathedral",
        "Seine River Cruise",
        "Montmartre"
    ],
    "tokyo": [
        "Shibuya Crossing",
        "Tokyo Tower",
        "Meiji Shrine",
        "Asakusa Temple",
        "Akihabara District"
    ],
    "rome": [
        "Colosseum",
        "Trevi Fountain",
        "Pantheon",
        "Roman Forum",
        "Vatican Museums"
    ],
    "new york": [
        "Statue of Liberty",
        "Central Park",
        "Times Square",
        "Empire State Building",
        "Broadway Shows"
    ],
    "london": [
        "Tower of London",
        "London Eye",
        "Buckingham Palace",
        "British Museum",
        "Big Ben"
    ]
}

# Connect to the SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the attractions table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attractions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL,
        attraction TEXT NOT NULL
    )
""")

# Insert data into the table
for city, attractions in attractions_data.items():
    for attraction in attractions:
        cursor.execute("INSERT INTO attractions (city, attraction) VALUES (?, ?)", (city.lower(), attraction))

# Save changes and close connection
conn.commit()
conn.close()

print("✅ city_attractions.db created and populated successfully.")
