#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
import database.adapter as adpt
from core.settings import FIELD_ALIAS_BASIC
from core.settings import ALLOWED_FIELDS_LOC

#GET OR CREATE
def get_or_create_loc(conn, input: dict):
    cursor = conn.cursor()
    events =[]
    data ={}
    if not input:
        return {"error": "invalid input"}
    #VALIDATE + MAP INPUT
    for field in ALLOWED_FIELDS_LOC:
        data.setdefault(field, None)
    for field, value in input.items():
        try:
            field = FIELD_ALIAS_BASIC.get(field, field)
            if field not in ALLOWED_FIELDS_LOC:
                events.append(f"Error: field not allowed -> {field}")
                continue
            if isinstance(value, str):
                value = value.strip()
            data[field] = value
        except ValueError as e:
            events.append(str(e))
    # NOW WHAT...