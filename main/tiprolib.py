#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# Version: 0.0.1.110511
# ID: 980001022
#|==============================================================|#

#IMPORT
import sqlite3
import json
from random import randint
import re
from datetime import datetime
import sys  #For ' if __name__ == "__main__" '
from os import get_terminal_size as cli_size #For ' if __name__ == "__main__" '

#SETTINGS
log =[]
results ={}
#TABLE RULES
ALLOWED_TABLES = [
    "products", 
    "price_history"
]
FIELD_ALIAS = {
    "qty": "qty_value",
    "qtyu": "qty_unit",
    "qtyd": "qty_default",
    "cat": "category"
}
ALLOWED_FIELDS = {
    "products" : {
        "gtin", "gtin_type", "code", "brand", "manufacturer", "name",
        "qty_value", "qty_default", "qty_unit", "info", "note",
        "madein", "additionalinfo", "status", "category"
    }
}
ALLOWED_FIELDS_PRODUCTS = ALLOWED_FIELDS["products"]
#START THINGS 1
def create_database(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gtin TEXT UNIQUE,
        gtin_type TEXT,
        code TEXT,
        brand TEXT,
        manufacturer TEXT,
        name TEXT,
        qty_value REAL,
        qty_default REAL,
        qty_unit TEXT,
        category TEXT,
        info TEXT,
        note TEXT,
        madein TEXT,
        status TEXT,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated TEXT,
        additionalinfo TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        price REAL,
        currency TEXT,
        place TEXT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
#START THINGS 2
def initialize(db_path="products.db"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    #cursor = conn.cursor()
    return conn

#DEFAULT TYPE FOR DATE AND TIME
def currentdatetime(mode =0):
    if mode == 0:
        now = str(datetime.now().isoformat("#", "auto"))
        now = now.replace("-",".")
        now = now.replace("#", "-")
    if mode == 1:
        now = str(datetime.now().strftime("%Y.%m.%d %H:%M:%S"))
    return now

#SYSTEM LOGGER
def logger(msg):
    log.append(f"{currentdatetime()} ; {msg}")

#REMOVE SPECIAL CHARAGTERS
def boring_text(input, mode):
    if mode == 0:
        return str("").join(i for i in input if i.isalnum())
    elif mode == 1:
        return re.sub(r"[^a-zA-Z0-9_-.,!# ]", "", input)

#SEPARATE VALUES AND UNITS
def parse_qty_input(value):
    match = re.match(r"^\s*(\d+(?:[.,]\d+)?)\s*([a-zA-Z]+)\s*$", value)
    if not match:
        raise ValueError(f"Invalid qty format: {value}")
    qty = float(match.group(1).replace(",", "."))
    unit = match.group(2).lower()
    return qty, unit

#DEFAULT COMMAND LINE TABLE PRINT
def print_table(headers, rows):
    output =[]
    data = [headers] + rows
    widths = [max(len(str(row[i])) for row in data) for i in range(len(headers))]
    #DATA
    for row in data:
        line = "=] "+ " | ".join(str(row[i]).ljust(widths[i]) for i in range(len(row)))
        line = line.replace("None", "    ")
        output.append(line)
    return output

#IF GTIN = EMPTY -> GENERETED CODE
def generate_internal_gtin(conn):
    cursor = conn.cursor()
    while True: #CHECK FOR NEW ID
        code = str(randint(1000000000, 9999999999))
        cursor.execute("SELECT gtin FROM products WHERE gtin=?", (code,))
        if not cursor.fetchone():
            return code

#GET TABLE
def get_table(conn, name, mode):
    cursor = conn.cursor()
    #RULES
    if name not in ALLOWED_TABLES:
        return {"error":"Invalid table"}
    cursor.execute("SELECT * FROM " + name)
    headers = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    #MORE RULES
    if not rows:
        return {"error":"No data"}
    output = {"title": headers, "content": rows}
    return output

#CREATE PRODUCT
def create_product(input: dict):
    now = currentdatetime()
    events =[]
    data ={}
    #VALIDATE + MAP INPUT
    for field in ALLOWED_FIELDS_PRODUCTS:
        data.setdefault(field, None)
    for field, value in input.items():
        try:
            field = FIELD_ALIAS.get(field, field)
            if field not in ALLOWED_FIELDS_PRODUCTS:
                events.append(f"Error: field not allowed -> {field}")
                continue
            if isinstance(value, str):
                value = value.strip()
            data[field] = value
        except ValueError as e:
            events.append(str(e))
    #MORE RULES
    if not data.get("name"):
        raise ValueError("name_required")
    #IDENTIFIERS
    if not data.get("gtin"):
        data["gtin"] = generate_internal_gtin(conn)
        data["gtin_type"] = "internal"
        output = "Generated GTIN: "+ str(data.get("gtin_type")) +" "+ str(data.get("gtin"))
        events.append(output)
    else:
        gtin = str(data.get("gtin")).replace(" ", "")
        data["gtin"] = boring_text(gtin,0)
        gtin = str(data.get("gtin_type")).replace(" ", "")
        data["gtin_type"] = boring_text(gtin,0)
    #QUANTITY
    raw_qty = data.get("qty_value")
    if isinstance(raw_qty, str):
        if not data.get("qty_unit"):
            if not raw_qty.isnumeric():
                qty_value, unit_symbol = parse_qty_input(raw_qty)
                data["qty_value"] = qty_value
                data["qty_unit"] = unit_symbol
    #SEND
    try:
        with conn:
            conn.execute("""
            INSERT INTO products (
                gtin, 
                gtin_type,
                code,
                brand,
                manufacturer,
                name,
                qty_value,
                qty_default,
                qty_unit,
                category,
                info,
                note,
                madein,
                status,
                created,
                updated
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, 
            (
                str(data["gtin"]), 
                data["gtin_type"],
                data["code"],
                data["brand"], 
                data["manufacturer"],
                data["name"], 
                data["qty_value"],
                data["qty_default"],
                data["qty_unit"],
                data["category"],
                data["info"],
                data["note"],
                data["madein"],      
                "active", 
                now,
                now
            )
        )
        output = {"info":"Product created", "gtin": data["gtin"], "gtin_type": data["gtin_type"], "events": events}
        return output
    except Exception as e:
        print("SQL ERROR:", e)

#UPDATE PRODUCT FIELDS DATA
def update_product(conn, gtin, **fields):
    cursor = conn.cursor()
    now = currentdatetime()
    updates = []
    values = []
    #MORE RULES
    for field, value in fields.items():
        field = FIELD_ALIAS.get(field, field)
        if field not in ALLOWED_FIELDS_PRODUCTS:
            logger(f"Error: field not allowed -> {field}")
            continue
        updates.append(f"{field}=?")
        values.append(value)
    #EVEN MORE RULES
    if not updates:
        logger("Error: no valid fields to update")
        return
    #UPDATE
    updates.append("updated=?")
    values.append(now)
    values.append(gtin)
    sql = f"UPDATE products SET {', '.join(updates)} WHERE gtin=?"
    with conn:
        cursor.execute(sql, values)
    logger(f"Updated product {gtin}")

#CHANGE PRODUCT STATUS (ACTIVE / PASSIVE)
def status_product(conn, pid):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT status FROM products WHERE id=?",
        (pid,)
    )
    now = currentdatetime()
    row = cursor.fetchone()
    if not row:
        logger("Product not found")
        return
    row = boring_text(row)
    output = "Old status:"+ row
    logger(output)
    if row == "active":
        row = "passive"
    else:
        row = "active"
    with conn:
        cursor.execute(
            "UPDATE products SET status=?, updated=? WHERE id=?",
            (row, now, pid)
        )
    output = "New status:"+ row
    logger(output)

#GET PRODUCT DATA
def get_product(conn, gtin, field =""):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE gtin=?", (gtin,))
    row = cursor.fetchone()
    if not row:
        logger("Product not found")
        return None
    #GET ALL DATA
    if field == "":
        #additional = json.loads(row["additionalinfo"] or "{}")
        product = dict(row)
        #product.update(additional)
        return product
    #GET SPECIFIG DATA
    else:
        field = FIELD_ALIAS.get(field, field)
        if field not in ALLOWED_FIELDS_PRODUCTS:
            logger(f"Error: field not allowed -> {field}")
            return
        #DATA
        product = dict(row)
        for i in product:
            if i == field:
                output = {i : product[i]}
                return output
            
#ADD NEW PRICE TO PRODUCT PRICE HISTORY
def add_price(conn, gtin, price, currency ="EUR", place =None):
    cursor = conn.cursor()
    gtin = gtin.replace(" ","")
    if gtin !="":
        try:
            price = float(str(price).replace(",", "."))
            cursor.execute(
                "SELECT id FROM products WHERE gtin=?",
                (gtin,)
            )
            row = cursor.fetchone()
            
            if not row:
                logger("Product not found")
                return
            product_id = int(row[0])

            with conn:
                cursor.execute("""
                INSERT INTO price_history
                (product_id, price, currency, place, date)
                VALUES (?, ?, ?, ?, ?)
                """, (product_id, price, currency, place, currentdatetime(1)))
            logger("Price added")
        except ValueError:
            logger("Invalid price")
    else:
        logger("No gtin code")

#GET PRODUCT PRICE HISTORY DATA
def price_history(conn, gtin):
    cursor = conn.cursor()
    gtin = gtin.replace(" ","")
    if gtin:
        #GET ID
        cursor.execute(
            "SELECT id FROM products WHERE gtin=?",
            (gtin,)
        )
        #RULES
        row = cursor.fetchone()
        if not row:
            logger("Product not found")
            return
        product_id = row[0]
        #GET DATA
        cursor.execute("""
        SELECT price, currency, date, place
        FROM price_history
        WHERE product_id=?
        ORDER BY date DESC
        """, (product_id,))
        #MODIFY
        headers = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return headers, rows
    else:
        return {"error":"No GTIN code"}

#ADD OR GET JSON DATA TO PRODUCT DATABASE
def mod_additional(conn, pid: int, mode: int, input: dict | None = None):
    """
    mode:
        1 = GET
        2 = MODIFY / MERGE
        3 = REPLACE
    """
    # VALIDATE INPUT
    values = {}
    if input:
        for field, value in input.items():
            output = boring_text(field, 0)
            if output:
                values[output] = value
    # GET CURRENT DATA
    cursor = conn.cursor()
    cursor.execute(
        "SELECT additionalinfo FROM products WHERE id=?",
        (pid,)
    )
    row = cursor.fetchone()
    if not row:
        return {"error": "Product not found"}
    # LOAD EXISTING JSON
    current = {}
    if row[0]:
        try:
            current = json.loads(row[0])
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in database"}
    # MODE 1 = GET
    if mode == 1:
        # if input contains keys -> return only requested keys
        if values:
            return {
                key: current.get(key)
                for key in values.keys()
            }
        return current
    # MODE 2 = MODIFY / MERGE
    elif mode == 2:
        current.update(values)
        data = current
    # MODE 3 = REPLACE
    elif mode == 3:
        data = values
    else:
        return {"error": "Invalid mode"}
    # SAVE
    cursor.execute(
        """
        UPDATE products
        SET additionalinfo=?
        WHERE id=?
        """,
        (
            json.dumps(data, ensure_ascii=False),
            pid
        )
    )
    conn.commit()
    return {
        "info": f"Additional info updated to ID: {pid}",
        "data": data
    }

#!
#if this is used only like plugin, these will not be needed from now on \/
#!

#CLI PRINT WITH SCREEN LIMIT
def printer(text: str):
    text = "=] " + str(text)
    try:
        limit = cli_size().columns -1 #SCREEN SIZE
        if len(text) > limit:
            print(text[:limit])
        else:
            print(text)
    except Exception as e:
        print(f"Error printing object: {e}")

#CREATE PRODUCT WIZARD
def create_product_wiz(mode =0):
    # 0 = Products, 1 = JSON
    table ={}
    if mode == 0:
        table = ALLOWED_FIELDS_PRODUCTS
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
        return "Error"

#IF THIS PLUGIN IS STARTED LIKE SOFTWARE
if __name__ == "__main__":
    #TA
    logger("Start")
    results ={}
    conn = initialize()
    dbcheck = create_database(conn)
    #TB
    try:
        if len(sys.argv) < 2:
            printer("")
            printer("            *** Welcome! Available commands ***")
            printer("")
            printer("create                  | Create product to database")
            printer("products                | Show all products from database")
            printer("update GTIN FIELD VALUE | Update product field value")
            printer("status ID               | Change product status (Active / passive)")
            printer("get GTIN VALUE          | Get product data. If value is empty show all")
            printer("extra                   | Get or Add additional info")
            printer("price add GTIN VALUE    | Add price history")
            printer("price history GTIN      | Show price history")
            printer("")
            conn.close()
            sys.exit()
        cmd = sys.argv[1]
        if cmd == "create":
            if len(sys.argv) == 2:
                output = create_product_wiz()
                results = create_product(output)
        elif cmd == "products":
            results = get_table(conn, "products", 1)
            headers = results["title"]
            rows = results["content"]
            skip_cols = ["status", "created", "additionalinfo"]
            indices = [i for i, h in enumerate(headers) if h not in skip_cols]
            filtered_headers = [headers[i] for i in indices]
            filtered_rows = []
            for row in rows:
                filtered_rows.append([row[i] for i in indices])
            results = print_table(filtered_headers, filtered_rows)
        elif cmd == "get":
            if len(sys.argv) == 3:
                results = get_product(conn, sys.argv[2])
            elif len(sys.argv) == 4:
                results = get_product(conn, sys.argv[2], sys.argv[3])
        elif cmd == "update":
            gtin = sys.argv[2]
            field = sys.argv[3]
            value = sys.argv[4]
            update_product(conn, gtin, **{field: value})
        elif cmd == "status":
            status_product(conn, sys.argv[2])
        elif cmd == "price":
            if len(sys.argv) < 3:
                printer("=] Options: ADD or HISTORY")
            else:
                if sys.argv[2] == "add":
                    add_price(conn, sys.argv[3], sys.argv[4])
                elif sys.argv[2] == "history":
                    headers, rows =  price_history(conn, sys.argv[3])
                    results = print_table(headers, rows)
        elif cmd == "extra":
            if len(sys.argv) == 2:
                printer("")
                printer("              *** OPTIONS ***")
                printer("")
                printer("GET, MOD")
                printer("")
            if len(sys.argv) > 3:
                arg1 = sys.argv[2]
                arg2 = sys.argv[3]
                if arg1 == "get":
                    results = mod_additional(conn, arg2, 1, "")
                if arg1 == "mod":
                    output = create_product_wiz(1)
                    results = mod_additional(conn, arg2, 2, output)
        #    add_additional(conn, sys.argv[2])
        elif cmd == "help":
            if sys.argv[2] == "get" or sys.argv[2] == "update":
                printer("")
                printer("              *** OPTIONS ***")
                printer("")
                printer("gtin_type, code, brand, manufacturer, name, category (or cat), ")
                printer("qty_value (or qty), qty_default (or qtyd), qty_unit (or qtu)")
                printer("info, note, madein, status, updated, additionalinfo")
                printer("")
        #TC
        print()
        if results:
            printer("Results:")
            if isinstance(results, list):
                    for i in results:
                        printer(i)
            elif isinstance(results, dict):
                for key, value in results.items():
                    printer(f"{key}: {value}")
            else:
                printer(results)
            print()
        logger("Stop")
        if logger:
            printer("Logger:")
            for i in log:
                printer(i)
        conn.close()
    except:
        conn.close()
        sys.exit()