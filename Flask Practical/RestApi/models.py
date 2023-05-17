from app import app
from flask import Flask
import mysql.connector


mysqldb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '1234',
    database = 'FlaskDB',
)

conn = mysqldb.cursor()

conn.execute("""
    CREATE TABLE IF NOT EXISTS Product (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Handle VARCHAR(400),
    Title VARCHAR(400),
    Body VARCHAR(400),
    Vendor VARCHAR(400),
    Type VARCHAR(400),
    Tags VARCHAR(400),
    Published VARCHAR(400),
    Variant_SKU VARCHAR(400),
    Variant_Inventory_Tracker VARCHAR(400),
    Variant_Price VARCHAR(400),
    Image_Src VARCHAR(400)
    );
""")

mysqldb.commit()
mysqldb.close()

if __name__ == '__main__':
    app.run(debug=True,port=8000)