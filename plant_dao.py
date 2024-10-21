import sqlite3
from plant import Plant

class PlantDao:
    def __init__(self, db_name="garden.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS garden
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, planted_date TEXT)''')
        conn.commit()
        conn.close()

    def add_plant(self, plant):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO garden (name, planted_date) VALUES (?, ?)",
                  (plant.name, plant.planted_date))
        plant.plant_id = c.lastrowid
        conn.commit()
        conn.close()

    def get_all_plants(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT id, name, planted_date FROM garden")
        rows = c.fetchall()
        conn.close()
        return [Plant(row[0], row[1], row[2]) for row in rows]

    def get_plant(self, plant_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT id, name, planted_date FROM garden WHERE id=?", (plant_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return Plant(row[0], row[1], row[2])
        return None

    def update_plant(self, plant):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("UPDATE garden SET name=?, planted_date=? WHERE id=?",
                  (plant.name, plant.planted_date, plant.plant_id))
        conn.commit()
        updated = c.rowcount > 0
        conn.close()
        return updated

    def delete_plant(self, plant_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("DELETE FROM garden WHERE id=?", (plant_id,))
        conn.commit()
        deleted = c.rowcount > 0
        conn.close()
        return deleted
