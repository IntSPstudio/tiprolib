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
    "basic": {
        "qty": "qty_value",
        "qtyu": "qty_unit",
        "qtyd": "qty_default",
        "brand": "brand_id",
        "org": "organization_id",
        "cat": "category_id",
        "mfg": "manufacturer_id",
        "add": "street_addres",
        "gtin": "identifier",
        "code": "identifier"
    }
}

FIELD_ALIAS_BASIC = FIELD_ALIAS["basic"]

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
    "locations": {
        "id",
        "name",
        "organization_id",
        "street_addres",
        "postal_code",
        "city",
        "info"
    },
    "quantity": {
        "id",
        "product_id",
        "identifier_id",
        "value",
        "status_id"
    },
    "create_product": {
        "identifier",
        "type",
        "brand",
        "name",
        "qty_default",
        "qty_unit",
        "info"
    }
}

ALLOWED_FIELDS_PRD = ALLOWED_FIELDS["products"]
ALLOWED_FIELDS_LOC = ALLOWED_FIELDS["locations"]