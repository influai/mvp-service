# db.py: Database Interaction and Filtering
import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Database connection setup
def get_db_connection():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    
    connection_string = f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"
    return psycopg2.connect(connection_string, cursor_factory=RealDictCursor)

# Filter channels based on JSON filters
def filter_channels_from_db(filters):
    query = """
        SELECT * FROM channels_warm_db
        WHERE category = %(category)s
        AND estimated_price BETWEEN %(min_price)s AND %(max_price)s
        AND subs_count BETWEEN %(min_subs)s AND %(max_subs)s;
    """
    params = {
        "category": filters.get("category"),
        "min_price": filters.get("price_range", [0, float("inf")])[0],
        "max_price": filters.get("price_range", [0, float("inf")])[1],
        "min_subs": filters.get("min_subs", 0),
        "max_subs": filters.get("max_subs", float("inf")),
    }
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
