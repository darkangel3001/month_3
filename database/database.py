import sqlite3

class Database:
    def __init__(self, path: str) -> None:
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS reviews (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(15) NOT NULL,
                        phone_number TEXT NOT NULL,
                        visit_date TEXT NOT NULL,
                        food_rating INTEGER NOT NULL,
                        cleanliness_rating INTEGER NOT NULL,
                        extra_comments TEXT NOT NULL
                    )   
                """
            )
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS dish_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                    )
                """
            )

            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS dishes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    cooking_time INTEGER NOT NULL,
                    categories TEXT NOT NULL
                    )
                """
            )
            conn.commit()

    def execute(self, query: str, params: tuple):
        with sqlite3.connect(self.path) as conn:
            conn.execute(query, params)
            conn.commit()

    def fetch(self, query: str, params: tuple = None):
        with sqlite3.connect(self.path) as conn:
            if not params:
                params = tuple()
            result = conn.execute(query, params)
            result.row_factory = sqlite3.Row
            data = result.fetchall()
            return [dict(r) for r in data]