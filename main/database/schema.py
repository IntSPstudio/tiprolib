#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from config import DATABASE_TYPE
from database.adapter import PLACEHOLDER
from core.settings import ALLOWED_TABLES

#DATABASE SETTINGS
def create_database(conn):
    cursor = conn.cursor()
    #DATABASE TYPES
    if DATABASE_TYPE == "sqlite":
        create_sqlite(cursor)
    conn.commit()
    seed_defaults(conn)

#DEFAULT VALUES TO DATABASE
def seed_defaults(conn):
    cursor = conn.cursor()
    #ORGANIZATION INI
    insert_default(cursor, "organizations", 1, {"name": "default", "info": "Default organization"})
    insert_default(cursor, "organizations", 2, {"name": "undefined", "info": "Undefined organization"})
    insert_default(cursor, "organizations", 3, {"name": "cash_customer", "info": "Default cash customer"})
    #WEBSITE USERS 1
    insert_default(cursor, "web_users", 1, {
        "username": "korhonen",
        "display_name": "Korhonen",
        "password_hash": "",
        "role": "admin",
        "must_change_password": 1,
    })
    #WEBSITE USERS 2
    insert_default(cursor, "web_users", 2, {
        "username": "virtanen",
        "display_name": "Virtanen",
        "password_hash": "",
        "role": "admin",
        "must_change_password": 1,
    })
    #IDENTIFIERS
    for type_id, value, name in [
        (1, "internal", "Internal code"),
        (2, "upc", "UPC"),
        (3, "ean13", "EAN-13"),
        (4, "ean8", "EAN-8"),
        (5, "isbn", "ISBN"),
        (6, "pn", "Part number"),
        (7, "sn", "Serial number"),
    ]:
        insert_default(cursor, "identifier_types", type_id, {"value": value, "name": name})
    #DEPBOSIT (Aka. Pantti)
    insert_default(cursor, "deposit_types", 1, {"code": "none","name": "No deposit","amount": "0","currency": "eur"})
    #SEND IT
    conn.commit()

#INSERT HELPER
def insert_default(cursor, table, row_id, values):
    #TABLE RULES
    if table not in ALLOWED_TABLES:
        print("HEI")
        raise ValueError(f"Invalid table '{table}'")
    #GET DATA
    cursor.execute(f"SELECT id FROM {table} WHERE id = {PLACEHOLDER}", (row_id,))
    if cursor.fetchone():
        return
    #SEND IT
    columns = ["id"] + list(values.keys())
    placeholders = ", ".join([PLACEHOLDER] * len(columns))
    cursor.execute(
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
        (row_id, *values.values()),
    )

#SQLITE DATABASES
def create_sqlite(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS statuses (
        id INTEGER PRIMARY KEY,
        value TEXT UNIQUE NOT NULL,
        name TEXT,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        info TEXT,
        master_id INTEGER,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(master_id) REFERENCES organizations(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        info TEXT,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        organization_id INTEGER DEFAULT 1,
        street_address TEXT,
        postal_code TEXT,
        city TEXT,
        info TEXT,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(organization_id) REFERENCES organizations(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deposit_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT,
        amount REAL DEFAULT 0,
        currency TEXT DEFAULT 'eur',
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand_id INTEGER DEFAULT 1,
        name TEXT NOT NULL,
        qty_default REAL DEFAULT 1,
        qty_unit TEXT DEFAULT 'pcs',
        weight_default REAL,
        weight_unit TEXT DEFAULT 'g',
        category_id INTEGER,
        deposit_type_id INTEGER DEFAULT 1,
        info TEXT,
        note TEXT,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        extra TEXT,
        FOREIGN KEY(brand_id) REFERENCES organizations(id),
        FOREIGN KEY(category_id) REFERENCES categories(id),
        FOREIGN KEY(deposit_type_id) REFERENCES deposit_types(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS identifier_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value TEXT UNIQUE NOT NULL,
        name TEXT,
        info TEXT,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS identifiers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        value TEXT UNIQUE NOT NULL,
        type_id INTEGER DEFAULT 1,
        info TEXT,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id),
        FOREIGN KEY(type_id) REFERENCES identifier_types(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_slots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT NOT NULL,
        path TEXT UNIQUE,
        parent_id INTEGER,
        organization_id INTEGER,
        info TEXT,
        location_id INTEGER,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(parent_id) REFERENCES stock_slots(id),
        FOREIGN KEY(organization_id) REFERENCES organizations(id),
        FOREIGN KEY(location_id) REFERENCES locations(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        identifier_id INTEGER,
        qty_value REAL DEFAULT 0,
        qty_unit TEXT,
        weight REAL,
        weight_unit TEXT DEFAULT 'kg',
        manufacturer_id INTEGER DEFAULT 1,
        extra TEXT,
        slot_id INTEGER DEFAULT 1,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id),
        FOREIGN KEY(identifier_id) REFERENCES identifiers(id),
        FOREIGN KEY(manufacturer_id) REFERENCES organizations(id),
        FOREIGN KEY(slot_id) REFERENCES stock_slots(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_id INTEGER,
        product_id INTEGER,
        identifier_id INTEGER,
        action TEXT NOT NULL,
        qty_delta REAL DEFAULT 0,
        qty_unit TEXT,
        reason TEXT,
        ref_table TEXT,
        ref_id INTEGER,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(stock_id) REFERENCES stock(id),
        FOREIGN KEY(product_id) REFERENCES products(id),
        FOREIGN KEY(identifier_id) REFERENCES identifiers(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        price REAL NOT NULL,
        currency TEXT DEFAULT 'eur',
        location_id INTEGER,
        organization_id INTEGER,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        status_id INTEGER DEFAULT 1,
        FOREIGN KEY(product_id) REFERENCES products(id),
        FOREIGN KEY(location_id) REFERENCES locations(id),
        FOREIGN KEY(organization_id) REFERENCES organizations(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        organization_id INTEGER DEFAULT 1,
        vendor_id INTEGER DEFAULT 2,
        total_price REAL,
        currency TEXT DEFAULT 'eur',
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(organization_id) REFERENCES organizations(id),
        FOREIGN KEY(vendor_id) REFERENCES organizations(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS purchase_lines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        purchase_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        identifier_id INTEGER,
        qty_value REAL DEFAULT 1,
        qty_unit TEXT,
        unit_price REAL,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(purchase_id) REFERENCES purchases(id),
        FOREIGN KEY(product_id) REFERENCES products(id),
        FOREIGN KEY(identifier_id) REFERENCES identifiers(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        organization_id INTEGER DEFAULT 1,
        customer_id INTEGER DEFAULT 3,
        total_price REAL,
        currency TEXT DEFAULT 'eur',
        payment_status INTEGER DEFAULT 0,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(organization_id) REFERENCES organizations(id),
        FOREIGN KEY(customer_id) REFERENCES organizations(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sale_lines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        identifier_id INTEGER,
        qty_value REAL DEFAULT 1,
        qty_unit TEXT,
        unit_price REAL,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(sale_id) REFERENCES sales(id),
        FOREIGN KEY(product_id) REFERENCES products(id),
        FOREIGN KEY(identifier_id) REFERENCES identifiers(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS web_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        display_name TEXT,
        password_hash TEXT,
        role TEXT DEFAULT 'seller',
        must_change_password INTEGER DEFAULT 1,
        token_secret TEXT,
        status_id INTEGER DEFAULT 1,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

#PRAGMA RULES
def ensure_sqlite_column(cursor, table, column, definition):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    if column not in columns:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")