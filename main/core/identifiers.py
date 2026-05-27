#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
from random import randint
from database.adapter import PLACEHOLDER

#IF NOT CODE -> INTERNAL CODE
def generate_internal_code(conn):
    cursor = conn.cursor()
    while True:
        code = str(
            randint(1000000000, 9999999999)
        )
        cursor.execute(
            f"SELECT identifiers FROM product_identifiers WHERE identifiers={PLACEHOLDER}",
            (code,)
        )
        if not cursor.fetchone():
            return code

#GET OR CREATE
def get_or_create_iden(conn, input: dict):
    cursor = conn.cursor()

#SCANNER
def get_by_identifier(conn, identifier: str):
    cursor = conn.cursor()
    query = f"""
        SELECT p.*, o.name as brand_name, i.value as identifier
        FROM product_data p
        JOIN identifiers i ON p.id = i.product_id
        JOIN organizations o ON p.organization_id = o.id
        WHERE i.value = {PLACEHOLDER} AND p.status_id = 1
    """
    cursor.execute(query, (identifier,))
    row = cursor.fetchone()
    return {"results":row}

#GET OR CREATE IDENTIFIER TYPE
def get_or_create_type(conn, type_input: str):
    cursor = conn.cursor()
    #RULES
    code = str(type_input).strip().lower()
    if not code:
        return {"error": "Identifier code is required"}
    #CHECK
    cursor.execute(f"SELECT id FROM identifier_types WHERE code = {PLACEHOLDER}", (code,))
    row = cursor.fetchone()
    #IF EXISTS
    if row:
        return {"id": row[0], "status": "exists"}
    #CREATE
    try:
        cursor.execute(f"INSERT INTO identifier_types (code) VALUES ({PLACEHOLDER})", (code,))
        conn.commit()
        return {"id": cursor.lastrowid, "status": "created"}
    #ERROR
    except sqlite3.Error as e:
        return {"error": str(e)}