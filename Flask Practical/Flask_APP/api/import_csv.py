from flask import Flask,request,redirect,render_template,url_for,flash
import csv
from logg import logger
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector
import pandas as pd
app = Flask(
    __name__,
    template_folder="/home/simprosys-aman/Aman/Aman/Flask Practical/Flask_APP/templates",
)



app.config["MYSQL_DB"]="FlaskDB"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_PASSWORD"]="Dubey@123"

mysqldb =MySQL(app)


# mysql_data = mysqldb.connection
# mysql_cursor =mysql_data.cursor(MySQLdb.cursors.DictCursor)

# all_column = """handle , 
#    title , 
#    body_html , 
#    vendor , 
#    type , 
#    tags, 
#    published , 
#    option1_name , 
#    option1_value , 
#    option2_name , 
#    option2_value , 
#    option3_name , 
#    option3_value , 
#    variant_sku , 
#    variant_grams , 
#    variant_inventory_tracker , 
#    variant_inventory_policy, 
#    variant_fulfillment_service , 
#    variant_price , 
#    variant_compare_at_price , 
#    variant_requires_shipping , 
#    variant_taxable , 
#    variant_barcode , 
#    image_src , 
#    image_position , 
#    image_alt_text , 
#    gift_card , 
#    seo_title , 
#    seo_description , 
#    google_shopping_google_product_category , 
#    google_shopping_gender , 
#    google_shopping_age_group , 
#    google_shopping_mpn , 
#    google_shopping_adwords_grouping , 
#    google_shopping_adwords_labels , 
#    google_shopping_condition , 
#    google_shopping_custom_product , 
#    google_shopping_custom_label_0 , 
#    google_shopping_custom_label_1 , 
#    google_shopping_custom_label_2 , 
#    google_shopping_custom_label_3, 
#    google_shopping_custom_label_4 , 
#    variant_image , 
#    variant_weight_unit , 
#    variant_tax_code , 
#    cost_per_item , 
#    status """


# import pandas as pd

# @app.route('/csv_import',methods=["POST","GET"])
# def savecsv():  
#     if request.method=="POST":
#         file =request.files['file']   
#         read_data_csv_file =pd.read_csv(file)
#         read_data_csv_file =read_data_csv_file.fillna("")
#         #read_data_csv_file.head()
#         table_name = "insert_dynamic_data_csv"
#         mysqlcsv =mysql.connector.connect(username="root",database="FlaskDB",password="Dubey@123",host="localhost")
#         cursor =mysqlcsv.cursor()

#         insert_stmt = f"INSERT INTO {table_name} ({','.join([col for col in all_column])}) VALUES ({','.join(['%s']*len(all_column))})"
#         print(len(insert_stmt))
#         print(len(all_column))
#         print(read_data_csv_file.columns)
#         print(len(read_data_csv_file.columns))
#         for i , row in read_data_csv_file.iterrows():
#             values = (row["Handle"],row["Title"],row["Body (HTML)"],row["Vendor"],row["Type"],row["Tags"],row["Published"],
#                 row["Option1 Name"],row["Option1 Value"],row["Option2 Name"],row["Option2 Value"],row["Option3 Name"],
#                 row["Option3 Value"],row["Variant SKU"],row["Variant Grams"],row["Variant Inventory Tracker"],row["Variant Inventory Policy"],
#                 row["Variant Fulfillment Service"],row["Variant Price"],row["Variant Compare At Price"],row["Variant Requires Shipping"],
#                 row["Variant Taxable"],row["Variant Barcode"],row["Image Src"],row["Image Position"],row["Image Alt Text"],row["Gift Card"],
#                 row["SEO Title"],row["SEO Description"],row["Google Shopping / Google Product Category"],
#                 row["Google Shopping / Gender"],row["Google Shopping / Age Group"],row["Google Shopping / MPN"],
#                 row["Google Shopping / AdWords Grouping"],row["Google Shopping / AdWords Labels"],row["Google Shopping / Condition"],
#                 row["Google Shopping / Custom Product"],row["Google Shopping / Custom Label 0"],
#                 row["Google Shopping / Custom Label 1"],row["Google Shopping / Custom Label 2"],
#                 row["Google Shopping / Custom Label 3"],row["Google Shopping / Custom Label 4"],
#                 row["Variant Image"],row["Variant Weight Unit"],row["Variant Tax Code"],row["Cost per item"],row["Status"])
#             print(len(values))
#             print(i,values)
#             cursor.execute(insert_stmt,values)
#         cursor.close()
#         mysqlcsv.commit()
#     return render_template('import_csv.html')







all_columns = """handle,
                 title,
                 body_html,
                 vendor,
                 type,
                 tags,
                 published,
                 option1_name,
                 option1_value,
                 option2_name,
                 option2_value,
                 option3_name,
                 option3_value,
                 variant_sku,
                 variant_grams,
                 variant_inventory_tracker,
                 variant_inventory_policy,
                 variant_fulfillment_service,
                 variant_price,
                 variant_compare_at_price,
                 variant_requires_shipping,
                 variant_taxable,
                 variant_barcode,
                 image_src,
                 image_position,
                 image_alt_text,
                 gift_card,
                 seo_title,
                 seo_description,
                 google_shopping_google_product_category,
                 google_shopping_gender,
                 google_shopping_age_group,
                 google_shopping_mpn,
                 google_shopping_adwords_grouping,
                 google_shopping_adwords_labels,
                 google_shopping_condition,
                 google_shopping_custom_product,
                 google_shopping_custom_label_0,
                 google_shopping_custom_label_1,
                 google_shopping_custom_label_2,
                 google_shopping_custom_label_3,
                 google_shopping_custom_label_4,
                 variant_image,
                 variant_weight_unit,
                 variant_tax_code,
                 cost_per_item,
                 status"""

@app.route('/csv_import', methods=["POST", "GET"])
def savecsv():
    if request.method == "POST":
        file = request.files['file']
        read_data_csv_file = pd.read_csv(file)
        read_data_csv_file = read_data_csv_file.fillna("")

        table_name = "insert_dynamic_data_csv"
        mysqlcsv = mysql.connector.connect(user="root", database="FlaskDB", password="Dubey@123", host="localhost")
        cursor = mysqlcsv.cursor()

        insert_stmt = f"INSERT INTO {table_name} ({all_columns}) VALUES ({','.join(['%s'] * len(all_columns.split(',')))})"

        for i, row in read_data_csv_file.iterrows():
            values = (row["Handle"],row["Title"],row["Body (HTML)"],row["Vendor"],row["Type"],row["Tags"],row["Published"],
                row["Option1 Name"],row["Option1 Value"],row["Option2 Name"],row["Option2 Value"],row["Option3 Name"],
                row["Option3 Value"],row["Variant SKU"],row["Variant Grams"],row["Variant Inventory Tracker"],row["Variant Inventory Policy"],
                row["Variant Fulfillment Service"],row["Variant Price"],row["Variant Compare At Price"],row["Variant Requires Shipping"],
                row["Variant Taxable"],row["Variant Barcode"],row["Image Src"],row["Image Position"],row["Image Alt Text"],row["Gift Card"],
                row["SEO Title"],row["SEO Description"],row["Google Shopping / Google Product Category"],
                row["Google Shopping / Gender"],row["Google Shopping / Age Group"],row["Google Shopping / MPN"],
                row["Google Shopping / AdWords Grouping"],row["Google Shopping / AdWords Labels"],row["Google Shopping / Condition"],
                row["Google Shopping / Custom Product"],row["Google Shopping / Custom Label 0"],
                row["Google Shopping / Custom Label 1"],row["Google Shopping / Custom Label 2"],
                row["Google Shopping / Custom Label 3"],row["Google Shopping / Custom Label 4"],
                row["Variant Image"],row["Variant Weight Unit"],row["Variant Tax Code"],row["Cost per item"],row["Status"])
            cursor.execute(insert_stmt, values)

        cursor.close()
        mysqlcsv.commit()

    return render_template('import_csv.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)