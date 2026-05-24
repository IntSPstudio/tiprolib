#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
import sys
from utils.printer import printer
from utils.prompt import cli_screen_clear
from cli.dictionary import create_dictionary_wiz
from core.products import create_product

#COMMAND LINE INTERFACE
def run_cli(conn):
    try:
        #
        # INDEX
        #
        if len(sys.argv) < 2:
            printer("")
            printer("/Index")
            printer("            *** Welcome! Available commands ***")
            printer("")
        #START
        cli_screen_clear()
        results ={}
        master = sys.argv[1]
        #
        # PRODUCTS
        #
        if master == "product" or master == "products" or master == "prd":
            if len(sys.argv) < 3:
                printer("")
                printer("/Products")
                printer("            *** Welcome! Available commands ***")
                printer("")
            else:
                #CREATE PRODUCT
                if len(sys.argv) == 3 and sys.argv[2] == "create":
                    #CREATING CONTENT
                    dict = create_dictionary_wiz()
                    results = create_product(conn,dict)
        #
        # INVENTORY
        #
        elif master == "inventory" or master == "inv":
            if len(sys.argv) < 3:
                printer("")
                printer("/Inventory")
                printer("            *** Welcome! Available commands ***")
                printer("")
    except:
        printer("Error")