#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# ID: 980001023
#|==============================================================|#

#|SYSTEM|=======================================================|#
APP_NAME = "TIPROLIB"

#|DATABASE|=====================================================|#
DATABASE_TYPE = "sqlite"
SQLITE_PATH = "products.db"

DATABASES = {
    "sqlite": {
        "user": "user",
        "path": SQLITE_PATH
    },

    "mariadb": {
        "host": "localhost",
        "user": "",
        "password": "",
        "database": "tiprolib"
    }
}

#|FEATURES|=====================================================|#
CLI_SC = False
DEBUG = True