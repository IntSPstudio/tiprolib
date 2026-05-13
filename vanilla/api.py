#|==============================================================|#
# Made by IntSPstudio
# Thank you for using this plugin!
# Version: 0.0.0.0
# ID: 980003037
#|==============================================================|#

#SETTINGS
from flask import Flask, request, jsonify
import tiprolib
app = Flask(__name__)

#CONNECTION
def get_conn():
    return tiprolib.initialize()

#START FUNCTIONS
def start_database():
    # CHECK / CREATE DATABASE
    conn = get_conn()
    tiprolib.create_database(conn)

#INDEX
@app.route("/", methods=["get"])
def homepage():
    return "<h1>Hello world!</h1>"

#GET ALL PRODUCTS
@app.route("/products", methods=["GET"])
def get_products():
    conn = get_conn()
    results = tiprolib.get_table(conn,"products",2)
    conn.close()
    return jsonify(results)

#GET SINGLE PRODUCT
@app.route("/products/<gtin>", methods=["GET"])
def get_product(gtin):
    conn = get_conn()
    product = tiprolib.get_product(conn, gtin)
    conn.close()
    if not product:
        return jsonify({"error": "Not found"}), 404
    return jsonify(product)

#CREATE PRODUCT
@app.route("/products", methods=["POST"])
def create_product():
    conn = get_conn()
    data = request.json
    results = tiprolib.create_product(conn, data)
    conn.close()
    return jsonify({"info": results}), 201

#START
if __name__ == "__main__":
    start_database()
    app.run(host="0.0.0.0", port=5000, debug=True)