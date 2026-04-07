import psycopg2
import os

def get_connection():
    try:
        return psycopg2.connect(
            os.getenv("DATABASE_URL"),
            sslmode="require"
        )
    except Exception as e:
        print("DB CONNECTION ERROR:", e)
        raise e