#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
from enums.status import Status
from database.adapter import PLACEHOLDER
from core.settings import ALLOWED_TABLES

#GET ALL
def get_all(conn, table_name: str, mode: int=0, limit: int =100, offset: int =0):
    #TABLE RULES
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Invalid table '{table_name}'")
    #CONNECTION
    cursor = conn.cursor()
    #SEARCH RESTRICTIONS (API THINGS)
    if mode == 0:
        query = f"""
                SELECT * FROM {table_name} 
                WHERE status_id = {PLACEHOLDER} 
                LIMIT {PLACEHOLDER} OFFSET {PLACEHOLDER}
            """
        params = (Status.ACTIVE.value, limit, offset)
    else:
        query = f"SELECT * FROM {table_name} LIMIT {PLACEHOLDER} OFFSET {PLACEHOLDER}"
        params = (limit, offset)
    #GET DATA
    try:
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error with {table_name}): {e}")
        return {}

#GET BY ID
def get_by_id(conn, table_name, row_id):
    #TABLE RULES
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Invalid table '{table_name}'")
    #CONNECTION
    cursor = conn.cursor()
    #QUERY
    query = f"SELECT * FROM {table_name} WHERE id = {PLACEHOLDER}"
    #GET DATA
    try:
        cursor.execute(query, (row_id,))
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        return None
    except sqlite3.Error as e:
        print(f"Error with {table_name}): {e}")
        return None