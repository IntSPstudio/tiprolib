#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# Version: 0.0.0.110304
# ID: 980001022
#|==============================================================|#

#IMPORT
import sqlite3
import json
import sys
import random
from datetime import datetime
#SETTINGS
log =[]
results ={}
demo =1

def initialize():
    DB = "products.db"
    conn = sqlite3.connect(DB)
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
        date TEXT
    )
    """)
    conn.commit()
    return conn

def currentdatetime():
    now = str(datetime.now().isoformat("#", "auto"))
    now = now.replace("-",".")
    now = now.replace("#", "-")
    return now

def logger(input):
    now = currentdatetime()
    output = now + " ; " + input
    log.append(output)

def print_table(headers, rows):
    data = [headers] + rows
    widths = [max(len(str(row[i])) for row in data) for i in range(len(headers))]
    for row in data:
        line = " | ".join(str(row[i]).ljust(widths[i]) for i in range(len(row)))
        line = line.replace("None", "    ")
        print(line)

def generate_internal_gtin(conn):
    cursor = conn.cursor()
    while True:
        code = str(random.randint(1000000000, 9999999999))
        cursor.execute("SELECT gtin FROM products WHERE gtin=?", (code,))
        if not cursor.fetchone():
            return code
def get_table(conn, name, mode):
    cursor = conn.cursor()
    allowed_tables = ["products", "price_history"]

    if name not in allowed_tables:
        logger("Invalid table")
        return

    cursor.execute("SELECT * FROM " + name)
    headers = [col[0] for col in cursor.description]

    rows = cursor.fetchall()

    if not rows:
        logger("Error")
        return

    return headers, rows

def create_product(conn, mode, content):
    cursor = conn.cursor()
    now = currentdatetime()
    if mode == 0:
        gtin = input("GTIN: ")
    elif mode == 1:
        gtin = content[0]
    gtin = gtin.replace(" ", "")
    if gtin == "":
        gtin = generate_internal_gtin(conn)
        gtin_type = "internal"
        output = "Generated GTIN:"+ str(gtin)
        logger(output)
    else:
        if mode == 0:
            gtin_type = input("GTIN type: ")
        elif mode == 1:
            gtin_type = content[1]
        gtin_type = gtin_type.lower()
    if mode == 0:
        brand = input("Brand: ")
        name = input("Name: ")
        additional = {}
    elif mode == 1:
        brand = content[2]
        name = content[3]
        additional = content[4]

    with conn:
        cursor.execute("""
        INSERT INTO products
        (gtin, gtin_type, brand, name, status, created, updated, additionalinfo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (gtin, gtin_type, brand, name, "active", now, now, json.dumps(additional)))

    logger("Product created")
def update_product_field(conn, gtin, field, value):
    cursor = conn.cursor()
    now = currentdatetime()

    if field == "qty":
        field = "qty_value"
    elif field == "qtyu":
        field = "qty_unit"
    elif field == "qtyd":
        field = "qty_default"

    allowed_fields = [
        "gtin_type", "code", "brand", "manufacturer", "name",
        "qty_value", "qty_default", "qty_unit", "info", "note", "madein",
        "additionalinfo", "status"
    ]
    
    if field not in allowed_fields:
        logger("Error: field not allowed")
        return
    
    gtin = gtin.replace(" ", "")
    
    with conn:
        cursor.execute(f"UPDATE products SET {field}=? WHERE gtin=?", (value, gtin))
        cursor.execute("UPDATE products SET updated=? WHERE gtin=?", (now, gtin))
    
    logger(f"Updated {field} for GTIN {gtin} to {value}")

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
    row = ''.join(char for char in row if char.isalpha())
    output = "Old status:"+ row
    logger(output)
    if row == "active":
        row = "passive"
    else:
        row = "active"

    with conn:
        cursor.execute("UPDATE products SET status=? WHERE id=?",(row, pid))
        cursor.execute("UPDATE products SET updated=? WHERE id=?",(now, pid))
    output = "New status:"+ row
    logger(output)

def get_product(conn, gtin, field):
    cursor = conn.cursor()
    gtin = gtin.replace(" ", "")
    cursor.execute(
        "SELECT * FROM products WHERE gtin=?",
        (gtin,)
    )
    row = cursor.fetchone()
    if not row:
        logger("Product not found")
        return
    if field == "":
        additional = json.loads(row["additionalinfo"])
        master = {
            "ID": row["id"],
            "Gtin": row["gtin"],
            "Gtin type": row["gtin_type"],
            "Code": row["code"],
            "Brand": row["brand"],
            "Manufacturer": row["manufacturer"],
            "Name": row["name"],
            "Qty ": row["qty_value"],
            "Qty default value": row["qty_default"],
            "Qty unit": row["qty_unit"],
            "Info": row["info"],
            "Note": row["note"],
            "Made in": row["madein"],
            "Status": row["status"],
            "Created": row["created"],
            "Updated": row["updated"],
        }
        results = master | additional
        return results
    else:
        if field == "qty":
            field = "qty_value"
        elif field == "qtyu":
            field = "qty_unit"
        elif field == "qtyd":
            field = "qty_default"

        allowed_fields = [
            "gtin_type", "code", "brand", "manufacturer", "name",
            "qty_value", "qty_default", "qty_unit", "info", "note", "madein",
            "status", "updated", "additionalinfo"
        ]
        if field not in allowed_fields:
                logger("Error: field not allowed")
                return
        output ={field: row[field]}
        return output

def add_price(conn, gtin, price):
    cursor = conn.cursor()

    gtin = gtin.replace(" ","")
    if gtin !="":
        try:
            price = price.replace(",",".")
            price = float(price)
            cursor.execute(
                "SELECT id FROM products WHERE gtin=?",
                (gtin,)
            )
            row = cursor.fetchone()
            if not row:
                logger("Product not found")
                return
            product_id = row[0]
            cursor.execute("""
            INSERT INTO price_history
            (product_id, price, currency, date)
            VALUES (?, ?, ?, ?)
            """, (product_id, price, "EUR", currentdatetime()))
            conn.commit()
            logger("Price added")
        except ValueError:
            logger("Invalid price")
    else:
        logger("No gtin code")

def price_history(conn, gtin):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM products WHERE gtin=?",
        (gtin,)
    )
    row = cursor.fetchone()
    if not row:
        logger("Product not found")
        return
    product_id = row[0]
    cursor.execute("""
    SELECT price, currency, date
    FROM price_history
    WHERE product_id=?
    ORDER BY date DESC
    """, (product_id,))
    for r in cursor.fetchall():
        if demo == 1:
            print(r[2], "|", r[0], r[1])

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

def search_volume(conn, volume):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT gtin, name
    FROM products
    WHERE json_extract(additionalinfo, '$.volume_ml') = ?
    """, (volume,))
    for r in cursor.fetchall():
        if demo == 1:
            print(r[0], "|", r[1])

if __name__ == "__main__":
    #TA
    logger("start")
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
            print("=]  price GTIN VALUE        | Add price history")
            print("=]  history GTIN            | Show price history")
            print("=]  extra ID                | Add additional info")
            print("=]")
            conn.close()
            sys.exit()
        cmd = sys.argv[1]
        if cmd == "create":
            create_product(conn, 0, "")
        elif cmd == "products":
            headers, rows = get_table(conn, "products", 1)
            skip_cols = ["status", "created", "updated", "additionalinfo","info","note","madein"]
            indices = [i for i, h in enumerate(headers) if h not in skip_cols]
            filtered_headers = [headers[i] for i in indices]
            filtered_rows = []
            for row in rows:
                filtered_rows.append([row[i] for i in indices])
            print_table(filtered_headers, filtered_rows)
        elif cmd == "get":
            if len(sys.argv) == 3:
                results = get_product(conn, sys.argv[2], "")
            elif len(sys.argv) == 4:
                results = get_product(conn, sys.argv[2], sys.argv[3])
        elif cmd == "update":
            update_product_field(conn, sys.argv[2], sys.argv[3], sys.argv[4])
        elif cmd == "status":
            status_product(conn, sys.argv[2])
        elif cmd == "price":
            add_price(conn, sys.argv[2], sys.argv[3])
        elif cmd == "history":
            price_history(conn, sys.argv[2])
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
        logger("stop")
        print()
        if len(results) > 0:
            print("Results:")
            for key, value in results.items():
                print(f"{key}: {value}")
            print()
        print("Logger:")
        for i in log:
            print(i)
        conn.close()
    except:
        conn.close()
        sys.exit()