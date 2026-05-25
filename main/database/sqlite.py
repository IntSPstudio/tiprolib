#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#DATABASE
import sqlite3
from config import DATABASES

#BASIC CONNECTION
def get_conn():
    conn = sqlite3.connect(
        DATABASES["sqlite"]["path"]
    )
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn