#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#SETTINGS
from config import DATABASE_TYPE

#DATABASE
def create_database(conn):
    cursor = conn.cursor()

    #SQLITE
    if DATABASE_TYPE == "sqlite":
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_id INTEGER,
            name TEXT,
            qty_default REAL,
            qty_unit TEXT,
            category_id INTEGER,
            info TEXT,
            note TEXT,
            status_id INTEGER DEFAULT 1,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            extra TEXT,
            FOREIGN KEY(brand_id) REFERENCES organizations(id),
            FOREIGN KEY(category_id) REFERENCES categories(id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_identifiers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            identifier TEXT,
            identifier_type TEXT,
            info TEXT,
            status_id INTEGER DEFAULT 1,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products_data(id)
        )
        """)
        cursor.execute("""                
        CREATE TABLE IF NOT EXISTS product_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            identifier_id INTEGER,
            qty_value REAL,
            qty_unit TEXT,
            manufacturer_id INTEGER,
            extra TEXT,
            status_id INTEGER DEFAULT 1,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products_data(id),
            FOREIGN KEY(identifier_id) REFERENCES product_identifiers(id),
            FOREIGN KEY(manufacturer_id) REFERENCES organizations(id)
        )
        """)
        cursor.execute("""  
        CREATE TABLE IF NOT EXISTS quantity_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            identifier_id INTEGER,
            value INTEGER,
            status_id INTEGER DEFAULT 1,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products_data(id),
            FOREIGN KEY(identifier_id) REFERENCES product_identifiers(id)
        )
        """)
        cursor.execute("""                
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            info TEXT,
            status_id INTEGER DEFAULT 1,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            info TEXT,
            status_id INTEGER DEFAULT 1,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """) 
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            price REAL,
            currency TEXT,
            location_id INTEGER,
            organization_id INTEGER,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            status_id INTEGER DEFAULT 1,
            FOREIGN KEY(product_id) REFERENCES products_data(id),
            FOREIGN KEY(location_id) REFERENCES locations(id),
            FOREIGN KEY(organization_id) REFERENCES organizations(id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            organization_id INTEGER,
            status_id INTEGER DEFAULT 1,
            created DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(organization_id) REFERENCES organizations(id)
        )
        """)
    #COMMON
    conn.commit()
