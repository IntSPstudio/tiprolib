#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from random import randint

#IF NOT CODE -> INTERNAL CODE
def generate_internal_code(conn):
    cursor = conn.cursor()
    while True:
        code = str(
            randint(1000000000, 9999999999)
        )
        cursor.execute(
            "SELECT identifiers FROM product_identifiers WHERE identifiers=?",
            (code,)
        )
        if not cursor.fetchone():
            return code