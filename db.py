import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="funny",
        user="postgres",
        password="Ashokreddy@11"
    )