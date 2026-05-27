#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sqlite3
from core.organizations import get_or_create_org
from core.identifiers import get_or_create_type
from core.settings import FIELD_ALIAS, ALLOWED_FIELDS_PRD
from database.adapter import PLACEHOLDER

#GET OR CREATE COMPLETE PRODUCT WITH DICTIONARY
def get_or_create_complete_product(conn, input_dict: dict):
    cursor = conn.cursor()
    events = []
    data = {}
    #RULES
    if not input_dict:
        return {"error": "invalid input"}
    #VALIDATE + MAP INPUT
    for field in ALLOWED_FIELDS_PRD:
        data.setdefault(field, None)