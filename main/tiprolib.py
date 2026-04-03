#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# Version: 0.0.1.110304
# ID: 980001022
#|==============================================================|#

#IMPORT
import sqlite3
import json
import sys
from os import get_terminal_size as cli_size
import random
import re
from datetime import datetime
#SETTINGS
log =[]
results ={}
demo =1

#START THINGS
def initialize(db_path="products.db"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
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
        qty_value INTEGER,
        qty_default INTEGER,
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
    #PRINT / RETURN
    if demo == 1:
        print("=]")
        for i in output:
            #CHECK SCREEN SIZE
            max_width = cli_size().columns
            if len(i) > max_width:
                i = i[:max_width]
            print(i)
        print("=]")
    else:
        return output
#IF GTIN = EMPTY -> GENERETED CODE
def generate_internal_gtin(conn):
    cursor = conn.cursor()
    while True: #CHECK FOR NEW ID
        code = str(random.randint(1000000000, 9999999999))
        cursor.execute("SELECT gtin FROM products WHERE gtin=?", (code,))
        if not cursor.fetchone():
            return code
#GET TABLE
def get_table(conn, name, mode):
    cursor = conn.cursor()
    allowed_tables = ["products", "price_history"]
    #RULES
    if name not in allowed_tables:
        logger("Invalid table")
        return
    cursor.execute("SELECT * FROM " + name)
    headers = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    #MORE RULES
    if not rows:
        logger("Error")
        return
    return headers, rows

#CREATE PRODUCT
def create_product(conn, gtin="", gtin_type="", brand=None, name=None, additional={}):
    cursor = conn.cursor()
    now = currentdatetime()

    gtin = boring_text(gtin,0) #REMOVE UNWANTED CHARACTERS
    gtin_type = boring_text(gtin_type,0) #REMOVE UNWANTED CHARACTERS

    if not gtin: #GENERATED GTIN ID
        gtin = generate_internal_gtin(conn)
        gtin_type = "internal"
        logger("Generated GTIN")
    else:
        gtin_type = gtin_type.lower()
    if not gtin_type:
        gtin_type = None

    with conn:
        cursor.execute("""
        INSERT INTO products
        (gtin, gtin_type, brand, name, status, created, updated, additionalinfo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (gtin, gtin_type, brand, name, "active", now, now, json.dumps(additional)))

    logger(f"Product created: {gtin} {gtin_type}")
    return gtin

#UPDATE PRODUCT FIELDS DATA
def update_product(conn, gtin, **fields):
    cursor = conn.cursor()
    now = currentdatetime()
    #RULES
    field_alias = {
        "qty": "qty_value",
        "qtyu": "qty_unit",
        "qtyd": "qty_default",
        "cat": "category"
    }
    allowed_fields = {
        "gtin_type", "code", "brand", "manufacturer", "name",
        "qty_value", "qty_default", "qty_unit", "info", "note",
        "madein", "additionalinfo", "status"
    }
    updates = []
    values = []
    #MORE RULES
    for field, value in fields.items():
        field = field_alias.get(field, field)
        if field not in allowed_fields:
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
        #RULES
        field_alias = {
            "qty": "qty_value",
            "qtyu": "qty_unit",
            "qtyd": "qty_default",
            "cat": "category"
        }
        allowed_fields = {
            "gtin_type", "code", "brand", "manufacturer", "name",
            "qty_value", "qty_default", "qty_unit", "info", "note",
            "madein", "additionalinfo", "status"
        }
        field = field_alias.get(field, field)
        if field not in allowed_fields:
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
        logger("No gtin code")

#ADD JSON DATA TO PRODUCT DATABASE
def add_additional(conn, pid):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT additionalinfo FROM products WHERE id=?",
        (pid,)
    )
    row = cursor.fetchone()
    if not row:
        logger("Product not found")
        return
    data = json.loads(row[0])
    key = input("Field name: ")
    value = input("Value: ")
    data[key] = value
    cursor.execute("""
    UPDATE products
    SET additionalinfo=?
    WHERE id=?
    """, (json.dumps(data), pid))
    conn.commit()
    output = "Additional info updated to ID:" + str(pid)
    logger(output)

#IF THIS PLUGIN IS STARTED LIKE SOFTWARE
if __name__ == "__main__":
    #TA
    logger("Start")
    results ={}
    conn = initialize()
    #TB
    try:
        if len(sys.argv) < 2:
            print("=]")
            print("=]            *** Welcome! Available commands ***")
            print("=]")
            print("=]  create                  | Create product to database")
            print("=]  products                | Show all products from database")
            print("=]  update GTIN FIELD VALUE | Update product field value")
            print("=]  status ID               | Change product status (Active / passive)")
            print("=]  get GTIN VALUE          | Get product data. If value is empty show all")
            print("=]  extra ID                | Add additional info")
            print("=]  price add GTIN VALUE    | Add price history")
            print("=]  price history GTIN      | Show price history")
            print("=]")
            conn.close()
            sys.exit()
        cmd = sys.argv[1]
        if cmd == "create":
            gtin =""
            gtin_type =""
            brand =""
            name =""
            if len(sys.argv) == 2:
                gtin = input("=] Gtin: ")
                gtin_type = input("=] Gtin type: ")
                brand = input("=] Brand: ")
                name = input("=] Name: ")
            if len(sys.argv) > 2:
                gtin = sys.argv[2]
                if len(sys.argv) > 3:
                    gtin_type = sys.argv[3]
            create_product(conn, gtin, gtin_type, brand, name)
        elif cmd == "products":
            headers, rows = get_table(conn, "products", 1)
            skip_cols = ["status", "created", "additionalinfo"]
            indices = [i for i, h in enumerate(headers) if h not in skip_cols]
            filtered_headers = [headers[i] for i in indices]
            filtered_rows = []
            for row in rows:
                filtered_rows.append([row[i] for i in indices])
            print_table(filtered_headers, filtered_rows)
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
                print("=] Options: ADD or HISTORY")
            else:
                if sys.argv[2] == "add":
                    add_price(conn, sys.argv[3], sys.argv[4])
                elif sys.argv[2] == "history":

                    headers, rows =  price_history(conn, sys.argv[3])
                    print_table(headers, rows)
        elif cmd == "extra":
            add_additional(conn, sys.argv[2])
        elif cmd == "help":
            if sys.argv[2] == "get" or sys.argv[2] == "update":
                print("=]")
                print("=]            *** OPTIONS ***")
                print("=]")
                print("=] gtin_type, code, brand, manufacturer, name, ")
                print("=] qty_value (or qty), qty_default (or qtyd), qty_unit (or qtu)")
                print("=] info, note, madein, status, updated, additionalinfo")
                print("=]")
        #TC
        print()
        if len(results) > 0:
            print("Results:")
            for key, value in results.items():
                print(f"{key}: {value}")
            print()
        print("Logger:")
        logger("Stop")
        for i in log:
            print(i)
        conn.close()
    except:
        conn.close()
        sys.exit()