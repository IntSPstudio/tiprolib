#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from utils.printer import (printer)
from core.settings import ALLOWED_FIELDS

#MAIN
def create_dictionary_wiz(help: str = None):
    table = ALLOWED_FIELDS[help]
    #START
    loop =1
    continuity =1
    data ={}
    printer("Add properties by writing: key = value")
    printer("Type 'exit' to quit and 'info' for key values")
    #ADD DATA
    while loop == 1:
        while continuity == 1:
            raw_input = input("=] Add new: ")
            if str.lower(raw_input) == "exit" or str.lower(raw_input) == "quit":
                continuity =0
            elif str.lower(raw_input) == "info" or str.lower(raw_input) == "help":
                if table:
                    a ="=]"
                    c =0
                    d =""
                    for b in table:
                        c +=1
                        a = a +" "+str(c)+". "+ str(b)
                    print(a)
            else:
                parts = raw_input.split("=", 1)
                if len(parts) != 2:
                    printer("Invalid format! Use: key = value")
                    continue
                key = parts[0].strip()
                value = parts[1].strip()
                data[key] = value
        #SHOW AND CONFIRM DATA
        if data:
            print("=]")
            printer("Selected data:")
            for key, value in data.items():
                output = str(key) +" = "+ str(value)
                printer(output)
            print("=]")
            raw_input = input("=] Send it! Yes or no? (Or 'edit') ")
            #PROCESS
            if str.lower(raw_input) == "yes" or str.lower(raw_input) == "y":
                #START FUNCTION
                continuity =0
                loop =0
                return data
            #EDIT
            elif str.lower(raw_input) == "edit" or str.lower(raw_input) == "e": 
                continuity =1
            #STOP
            else:
                loop =0
                printer("Event cancelled")
        return None