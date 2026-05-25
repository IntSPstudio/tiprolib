#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
#
# ID: 980001023
#|==============================================================|#

"""
    |========================== INFO ==========================|

    TABLES:               | INFO:
    product_identifiers   | 
    product_data          | 
    product_inventory     | 
    quantity_history      | 
    price_history         |
    categories            |
    organizations         |
    locations             |
"""

#SETTINGS
from database import get_conn
from database.schema import create_database
from cli.commands import run_cli

#MAIN LOOP
def main():
    conn = get_conn()
    create_database(conn)
    run_cli(conn)

#START
if __name__ == "__main__":
    main()