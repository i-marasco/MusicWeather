import psycopg2

def get_connection():
    """
    :return
            Connection to PostgreSQL database.
    """
    return psycopg2.connect(
        dbname="music",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )
