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
from core.organizations import get_or_create_org
from core.locations import get_or_create_loc

#COMMAND LINE INTERFACE
def run_cli(conn):
    #START
    cli_screen_clear()
    #
    # INDEX
    #
    if len(sys.argv) < 2:
        printer("")
        printer("/Index")
        printer("            *** Welcome! Available commands ***")
        printer("")
        printer(" -Products")
        printer(" -Inventory")
        printer(" -Organizations")

        printer("")
    #OPTIONS
    else:
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
                printer(" -Create")
            else:
                #CREATE PRODUCT
                if len(sys.argv) == 3 and sys.argv[2] == "create":
                    #CREATING CONTENT
                    dict = create_dictionary_wiz("products")
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
        #
        # ORGANIZATIONS
        #
        elif master == "organizations" or master == "org":
            if len(sys.argv) < 3:
                printer("")
                printer("/Organizations")
                printer("            *** Welcome! Available commands ***")
                printer("")
                printer(" -Create NAME INFO")
            else:
                #GET OR CREATE ORGANIZATIONS
                if len(sys.argv) == 4 and sys.argv[2] == "create" and sys.argv[3]:
                    results = get_or_create_org(conn,sys.argv[3],"")
                    printer("ID", results)
                elif len(sys.argv) == 5 and sys.argv[2] == "create" and sys.argv[3] and sys.argv[4]:
                    results = get_or_create_org(conn, sys.argv[3], sys.argv[4])
                    printer("ID", results)
        #
        # LOCATIONS
        #
        elif master == "locations" or master == "loc":
            if len(sys.argv) < 3:
                printer("")
                printer("/Locations")
                printer("            *** Welcome! Available commands ***")
                printer("")
            else:
                #GET OR CREATE ORGANIZATIONS
                if len(sys.argv) == 3 and sys.argv[2] == "create":
                    output = create_dictionary_wiz("locations")
                    results = get_or_create_loc(conn,output)
        #
        # OUTPUT
        #
        printer(f"Results: {results}")