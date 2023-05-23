from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    make_response,
    Response,
    jsonify,
    flash,
)
from Flask_APP.api.logg import logger
from userapp.models import conn,mycursor
import mysql.connector
from flask_mail import Mail, Message
import csv
import threading
from datetime import datetime
import pandas as pd
import pdfkit
from flask_paginate import get_page_parameter
from product_app.blueprint import product_blueprint
import pandas as pd
from userapp.models import MysqlDB
conn = MysqlDB()

exception_code = 40
date = datetime.now()


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


@product_blueprint.route("/import_csv_useingthread", methods=["POST", "GET"])
def upload_csv():
    try:
        if request.method == "POST":
            file = request.files["file"]
            read_data_csv_file = pd.read_csv(file)
            read_data_csv_file = read_data_csv_file.fillna("")

            table_name = "insert_dynamic_data_csv"
            mysqlcsv = mysql.connector.connect(
                user="root", database="FlaskDB", password="Dubey@123", host="localhost"
            )
            cursor = mysqlcsv.cursor()

            insert_stmt = f"INSERT INTO {table_name} ({all_columns}) VALUES ({','.join(['%s'] * len(all_columns.split(',')))})"

            for i, row in read_data_csv_file.iterrows():
                values = (
                    row["Handle"],
                    row["Title"],
                    row["Body (HTML)"],
                    row["Vendor"],
                    row["Type"],
                    row["Tags"],
                    row["Published"],
                    row["Option1 Name"],
                    row["Option1 Value"],
                    row["Option2 Name"],
                    row["Option2 Value"],
                    row["Option3 Name"],
                    row["Option3 Value"],
                    row["Variant SKU"],
                    row["Variant Grams"],
                    row["Variant Inventory Tracker"],
                    row["Variant Inventory Policy"],
                    row["Variant Fulfillment Service"],
                    row["Variant Price"],
                    row["Variant Compare At Price"],
                    row["Variant Requires Shipping"],
                    row["Variant Taxable"],
                    row["Variant Barcode"],
                    row["Image Src"],
                    row["Image Position"],
                    row["Image Alt Text"],
                    row["Gift Card"],
                    row["SEO Title"],
                    row["SEO Description"],
                    row["Google Shopping / Google Product Category"],
                    row["Google Shopping / Gender"],
                    row["Google Shopping / Age Group"],
                    row["Google Shopping / MPN"],
                    row["Google Shopping / AdWords Grouping"],
                    row["Google Shopping / AdWords Labels"],
                    row["Google Shopping / Condition"],
                    row["Google Shopping / Custom Product"],
                    row["Google Shopping / Custom Label 0"],
                    row["Google Shopping / Custom Label 1"],
                    row["Google Shopping / Custom Label 2"],
                    row["Google Shopping / Custom Label 3"],
                    row["Google Shopping / Custom Label 4"],
                    row["Variant Image"],
                    row["Variant Weight Unit"],
                    row["Variant Tax Code"],
                    row["Cost per item"],
                    row["Status"],
                )
                cursor.execute(insert_stmt, values)
                insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
                insert_value = (date,"0.0.0.0","user import csv")
                mycursor.execute(insert_query,insert_value)
            cursor.close()
            mysqlcsv.commit()

            flash("Csv imported Sucsessfully")
            return redirect("/user_blueprint/login")
        return render_template("import_csv.html")

    except Exception as e:
        print("Someting went wrong")
        logger.error(e)
        insert_query = "Insert into Exceptions(exception_code,exception_date,exception_type,messages,IP,description) Values(%s,%s,%s,%s,%s,%s)"
        insert_value = (exception_code,date,type(e),e,"0.0.0.0","Got error in the upload csv time")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        conn.close()
    return redirect("/user_blueprint/login")


@product_blueprint.route("/export_csv", methods=["POST", "GET"])
def export_csv():
    try:
        # conn = MysqlDB()
        # mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM insert_dynamic_data_csv")
        data = mycursor.fetchall()
        df = pd.DataFrame(data, columns=[desc[0] for desc in mycursor.description])
        csv_data = df.to_csv()
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d %H:%M:%S") + ":products.csv"
        insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
        insert_value = (date,"0.0.0.0","user in the login")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        mycursor.close()
        conn.close()
        response = Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename={filename}"},
        )

        return response

    except Exception as e:
        print("Someting went wrong")
        logger.error(e)
        insert_query = "Insert into Exceptions(exception_code,exception_date,exception_type,messages,IP,description) Values(%s,%s,%s,%s,%s,%s)"
        insert_value = (exception_code,date,type(e),e,"0.0.0.0","Got error in the export_csv time")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        conn.close()

    return redirect("/product_blueprint/export_csv")


@product_blueprint.route("/export_pdf", methods=["POST", "GET"])
def export_pdf():
    try:
        # conn = MysqlDB()
        # mycursor = conn.cursor()
        mycursor.execute("SELECT * FROM insert_dynamic_data_csv")
        data = mycursor.fetchall()
        insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
        insert_value = (date,"0.0.0.0","user is trying to export pdf")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        mycursor.close()
        conn.close()
        template = render_template("pdf_data.html", data=data)
        pdf = pdfkit.from_string(template, False)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "attachment; filename=products.pdf"

        return response

    except Exception as e:
        print("Someting went wrong")
        logger.error(e)
        insert_query = "Insert into Exceptions(exception_code,exception_date,exception_type,messages,IP,description) Values(%s,%s,%s,%s,%s,%s)"
        insert_value = (exception_code,date,type(e),e,"0.0.0.0","Got error in the export_pdf time")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        conn.close()

    return redirect("/product_blueprint/export_pdf")


def products(offset=None, per_page=None):
    conn = MysqlDB()
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT * FROM Products LIMIT {per_page} OFFSET {offset}")
    datacursure = mycursor.fetchall()
    mycursor.close()
    conn.close()

    return datacursure


@product_blueprint.route("/product_list", methods=["GET", "POST"])
def product_list():
    mycurser = conn.cursor()
    mycurser.execute("SELECT * FROM Products")
    alldata = mycurser.fetchall()
    print(len(all_data))
    print(alldata)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    first_page = 1
    per_page = 3
    offset = (page - 1) * int(per_page)
    print("offset", offset)
    items = products(offset, per_page)
    print(items)
    # conn = MysqlDB()
    # mycursure = conn.cursor()
    mycurser.execute("SELECT * FROM Products")
    all_data = mycurser.fetchall()
    mycurser.close()
    total_page = (len(all_data) // per_page) + len(all_data) % per_page
    print("total page", total_page)
    if request.method == "POST":
        # conn = MysqlDB()
        # mycurser = conn.cursor()
        insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
        insert_value = (date,"0.0.0.0","user in productlisting")
        mycurser.execute(insert_query,insert_value)
        conn.commit()
        Product_id = request.form.getlist("product_id")
        print("product_id", Product_id)
        if Product_id == []:
            flash("Please select the product first")

            return redirect(url_for("product_blueprint.product_list"))
        else:
            # conn = MysqlDB()
            # mycurser = conn.cursor()
            Product_id = request.form.getlist("product_id")
            delete_query = "DELETE FROM Products WHERE product_id in %s;"
            delete_value = (Product_id,)
            mycursor.execute(delete_query, delete_value)
            insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
            insert_value = (date,"0.0.0.0","user deleting product")
            mycurser.execute(insert_query,insert_value)
            conn.commit()
            conn.close()
            flash(f"Products {Product_id} has been deleted sucsessfully")

            return redirect(url_for("product_blueprint.product_list"))


    return render_template(
        "product_list.html",
        items=items,
        page=page,
        per_page=per_page,
        total_page=total_page,
        first_page=first_page,
    )
