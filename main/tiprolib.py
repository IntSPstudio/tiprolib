#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# Version: 0.0.0.110104
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
        info TEXT,
        note TEXT,
        madein TEXT,
        status TEXT,
        created TEXT,
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

def generate_internal_gtin(conn):
    cursor = conn.cursor()
    while True:
        code = str(random.randint(1000000000, 9999999999))
        cursor.execute("SELECT gtin FROM products WHERE gtin=?", (code,))
        if not cursor.fetchone():
            return code

def create_product(conn):
    cursor = conn.cursor()
    now = currentdatetime()
    gtin = input("GTIN: ")
    gtin = gtin.replace(" ", "")

    if gtin == "":
        gtin = generate_internal_gtin(conn)
        gtin_type = "internal"
        output = "Generated GTIN:"+ str(gtin)
        logger(output)
    else:
        gtin_type = input("GTIN type: ")
        gtin_type = gtin_type.lower()

    brand = input("Brand: ")
    name = input("Name: ")
    additional = {}
    cursor.execute("""
    INSERT INTO products
    (gtin, gtin_type, brand, name, status, created, updated, additionalinfo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (gtin, gtin_type, brand, name, "active", now, now, json.dumps(additional)))
    conn.commit()
    logger("Product created")

def get_product(conn, gtin):
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
    additional = json.loads(row[13])
    master = {
        "ID": row[0],
        "Gtin": row[1],
        "Gtin type": row[2],
        "Code": row[3],
        "Brand": row[4],
        "Manufacturer": row[5],
        "Name": row[6],
        "Info": row[7],
        "Note": row[8],
        "Made in": row[9],
        "Status": row[10],
        "Created": row[11],
        "Updated": row[12],
    }
    results = master | additional
    return results

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
        except:
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
            print("=] Welcome! To use this you need to write one of the following command.")
            print("=] Commands:")
            print("=]  create")
            print("=]  get GTIN")
            print("=]  price GTIN VALUE")
            print("=]  history GTIN")
            print("=]  extra ID")
            sys.exit()
        cmd = sys.argv[1]
        if cmd == "create":
            create_product(conn)
        elif cmd == "get":
            results = get_product(conn, sys.argv[2])
        elif cmd == "price":
            add_price(conn, sys.argv[2], sys.argv[3])
        elif cmd == "history":
            price_history(conn, sys.argv[2])
        elif cmd == "extra":
            add_additional(conn, sys.argv[2])
        #TC
        print()
        if len(results) > 0:
            print("Results:")
            for key, value in results.items():
                print(f"{key}: {value}")
            print()
        print("Logger:")
        for i in log:
            print(i)
    except:
        sys.exit()