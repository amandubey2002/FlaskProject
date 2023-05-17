from flask import Flask
import pymysql as Pymysqldb
app = Flask(__name__)
import mysql.connector


mysqldb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dubey@123",
    database="FlaskDB",
)

def MysqlDB():
    conn = Pymysqldb.connect(
    host = 'localhost',
    user = 'root',
    password = 'Dubey@123',
    database = 'FlaskDB',
    )
    return conn



conn = mysqldb.cursor()


conn.execute(
    """
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255)
        );
    """
)


conn.execute(
    """create table if not exists Products (product_id int not null , Handle varchar(400), Title varchar(400), Body varchar(400),Vendor varchar(400), Type varchar(400), Tags varchar(400), Published varchar(400),
            VariantSKU varchar(400), VariantInventoryTracker varchar(400), VariantPrice varchar(400), ImageSrc varchar(400) , primary key (product_id));"""
)

mysqldb.commit()
mysqldb.close()





import mysql.connector

app = Flask(__name__)



table_name = "insert_dynamic_data_csv"
mysqlcsv =mysql.connector.connect(username="root",database="FlaskDB",password="Dubey@123",host="localhost")
cursor =mysqlcsv.cursor()
sql_query =""" CREATE TABLE IF NOT EXISTS insert_dynamic_data_csv (
   handle TEXT, 
   title TEXT, 
   body_html TEXT, 
   vendor TEXT, 
   type TEXT, 
   tags TEXT, 
   published TEXT, 
   option1_name TEXT, 
   option1_value TEXT, 
   option2_name TEXT, 
   option2_value TEXT, 
   option3_name TEXT, 
   option3_value TEXT, 
   variant_sku TEXT, 
   variant_grams TEXT, 
   variant_inventory_tracker TEXT, 
   variant_inventory_policy TEXT, 
   variant_fulfillment_service TEXT, 
   variant_price TEXT, 
   variant_compare_at_price TEXT, 
   variant_requires_shipping TEXT, 
   variant_taxable TEXT, 
   variant_barcode TEXT, 
   image_src TEXT, 
   image_position TEXT, 
   image_alt_text TEXT, 
   gift_card TEXT, 
   seo_title TEXT, 
   seo_description TEXT, 
   google_shopping_google_product_category TEXT, 
   google_shopping_gender TEXT, 
   google_shopping_age_group TEXT, 
   google_shopping_mpn TEXT, 
   google_shopping_adwords_grouping TEXT, 
   google_shopping_adwords_labels TEXT, 
   google_shopping_condition TEXT, 
   google_shopping_custom_product TEXT, 
   google_shopping_custom_label_0 TEXT, 
   google_shopping_custom_label_1 TEXT, 
   google_shopping_custom_label_2 TEXT, 
   google_shopping_custom_label_3 TEXT, 
   google_shopping_custom_label_4 TEXT, 
   variant_image TEXT, 
   variant_weight_unit TEXT, 
   variant_tax_code TEXT, 
   cost_per_item TEXT, 
   status TEXT
);"""

cursor.execute(sql_query)
cursor.close()
mysqlcsv.commit()


if __name__ == "__main__":
    app.run(debug=True, port=8000)
