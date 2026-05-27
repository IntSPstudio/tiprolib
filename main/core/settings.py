#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#RULES
ALLOWED_TABLES = [
    "products",
    "identifiers",
    "stock",
    "stock_log",
    "stock_slot",
    "price_history",
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
    },
    "add_complete_product": {
        "b": {
            "table":"products",
            "name": "brand_id",
            "help": "Name or ID"
        },
        "n": {
            "table":"products",
            "name": "name",
            "help": ""
        },
        "qty": {
            "table":"products",
            "name": "qty_default",
            "help": "Default quantity value with or without unit"
        },
        "qd": {
            "table":"products",
            "name": "qty_default",
            "help": "Default quantity value with or without unit"
        },
        "qu": {
            "table":"products",
            "name": "qty_unit",
            "help": "Default quantity unit"
        },
        "c": {
            "table":"products",
            "name": "category_id",
            "help": "Name or ID"
        },
        "i": {
            "table":"products",
            "name": "info",
            "help": "Additional info"
        },
        "cn": {
            "table":"identifiers",
            "name": "value",
            "help": "Identifier code value"
        },
        "ct": {
            "table":"identifiers",
            "name": "type_id",
            "help": "Identifier code type"
        },
        "ci": {
            "table":"identifiers",
            "name": "info",
            "help": "Additional info"
        }
    },
    "add_products": {
        "b": "brand_id",
        "n": "name",
        "qd": "qty_default",
        "qu": "qty_unit",
        "c": "category_id",
        "i": "info"
    },
    "add_organizations": {
        "n": "name",
        "i": "info"
    },
    "add_locations": {
        "n": "name",
        "o": "organization_id",
        "s": "street_address",
        "p": "postal_code",
        "c": "city",
        "i": "info"
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
        "weight_default",
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
    "identifier_types": {
        "id",
        "code",
        "name",
        "info"
    },
    "stock": {
        "id",
        "product_id",
        "identifier_id",
        "qty_value",
        "qty_unit",
        "weight",
        "manufactured_id",
        "extra",
        "status_id"
    },
    "stock_logs": {
        "id",
        "product_id",
        "identifier_id",
        "value",
        "status_id"
    },
    "stock_slots": {
        "id",
        "code",
        "info",
        "location_id"
    },
    "categories": {
        "id",
        "name",
        "info"
    },
    "locations": {
        "id",
        "name",
        "organization_id",
        "street_address",
        "postal_code",
        "city",
        "info"
    },
    "organizations": {
        "id",
        "name",
        "info"
    }
}

ALLOWED_FIELDS_PRD = ALLOWED_FIELDS["products"]
ALLOWED_FIELDS_LOC = ALLOWED_FIELDS["locations"]