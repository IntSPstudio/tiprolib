#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#RULES
ALLOWED_TABLES = [
    "product_data",
    "product_identifiers",
    "product_inventory",
    "price_history",
    "quantity_history",
    "organizations",
    "categories",
    "locations"
]

FIELD_ALIAS = {
    "qty": "qty_value",
    "qtyu": "qty_unit",
    "qtyd": "qty_default",
    "cat": "category_id",
    "mfg": "manufacturer_id"
}

ALLOWED_FIELDS = {
    "products": {
        "id",
        "brand_id",
        "category_id",
        "name",
        "qty_default",
        "qty_unit",
        "info",
        "note",
        "extra",
        "status_id",
    },
    "identifiers": {
        "id",
        "product_id",
        "identifier",
        "type",
        "info",
        "status_id",
    },
    "inventory": {
        "id",
        "product_id",
        "identifier_id",
        "qty_value",
        "qty_unit",
        "manufactured_id",
        "extra",
        "status_id"
    },
    "quantity": {
        "id",
        "product_id",
        "identifier_id",
        "value",
        "status_id"
    }
}

ALLOWED_FIELDS_PRODUCTS = ALLOWED_FIELDS["products"]