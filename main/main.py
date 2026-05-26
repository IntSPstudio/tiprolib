#|==============================================================|#
# Made by IntSPstudio
# TIPROLIB PDB
# Thank you for using this plugin!
# Version: 0.0.0.0
# ID: 980001023
#|==============================================================|#

"""
    |========================== INFO ==========================|

    TABLES:               | INFO:
    product_identifiers   | Gtin's, unique product id's, links
    product_data          | Product data reference
    product_inventory     | Stock inventory
    quantity_history      | Counts the quantities of products in inventory
    price_history         | Product price history
    categories            | Product categories
    organizations         | All the organizations, brands or manufactures etc
    locations             | Location of organizations

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