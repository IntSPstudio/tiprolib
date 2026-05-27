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
    identifier_types      | UPC, EAN13, EAN8, ISBN etc
    identifiers           | Gtin's, unique product id's, links 
    products              | Product data reference
    categories            | Product categories
    stock                 | Stock inventory
    stock_logs            | Counts the quantities of products in stock inventory
    stock_slots           | Stock inventory locations
    price_history         | Product price history
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