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
import mysql.connector
import uuid
import pymysql as Pymysqldb
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
import csv
import threading
from datetime import datetime, timedelta
import pandas as pd
import pdfkit
from flask_paginate import Pagination, get_page_parameter
from blueprint import blueprint
from logg import logger
import pandas as pd

app = Flask(
    __name__,
    template_folder="/home/simprosys-aman/Aman/Flask/Flask Practical/Flask_APP/templates",
)
app.secret_key = b"ghjkjlkgfdfghjkl98797980989jhgfghjkl"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "amandubey@simprosys.com"
app.config["MAIL_PASSWORD"] = "zsuoyovnmxuqceam"
app.config["MAIL_USE_TLS"] = True

mail = Mail(app)

exception_code = 40
date = datetime.now()


def MysqlDB():
    conn = Pymysqldb.connect(
        host="localhost",
        user="root",
        password="Dubey@123",
        database="FlaskDB",
    )

    return conn


conn = MysqlDB()
mycursor = conn.cursor()

@blueprint.route("/index", methods=["GET"])
def index():
    return render_template("base.html")


@blueprint.route("/sucsess", methods=["GET"])
def sucsess():
    return render_template("welcome.html")


@blueprint.route("/profile", methods=["POST", "GET"])
def profile():
    return render_template("profile.html")


@blueprint.route("/signup", methods=["POST", "GET"])
def signup():
    try:
        if request.method == "POST":
            conn = MysqlDB()
            mycursor = conn.cursor()
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            # password = generate_password_hash(password1)
            if not username or not email or not password:
                flash("All fields are required")

                return redirect("/api/signup")
            else:
                insert_query = (
                    "INSERT INTO Users(username,email, password) Values (%s,%s,%s)"
                )
                insert_value = (username, email, password)
                mycursor.execute(insert_query, insert_value)
                conn.commit()
                msg = Message(
                    "Thank you for joining",
                    sender="amandubey@simprosys.com",
                    recipients=[email],
                )
                msg.body = "Welcome to our community! We're thrilled to have you join us and can't wait to see what you bring to the table. Don't hesitate to reach out if you have any questions or if there's anything we can do to help make your experience here even better "
                mail.send(msg)
                flash("Registration successful")

                return render_template("signup.html")
        else:
            return render_template("signup.html")

    except Exception as e:
        print("Something Went Wrong")
        logger.error(e)

    return redirect("/api/login")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST" and "password" in request.form and "email" in request.form:
            conn = MysqlDB()
            mycursor = conn.cursor()
            email = request.form["email"]
            print(email)
            password = request.form["password"]
            # password1 = generate_password_hash(password)
            select_query = "SELECT * FROM Users WHERE email = %s and password = %s"
            select_value = (email, password)
            mycursor.execute(select_query, select_value)
            user = mycursor.fetchone()
            print(user)
            if user:
                session["authenticated"] = True
                session["email"] = email
                insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
                insert_value = (date,"0.0.0.0","user in the login")
                mycursor.execute(insert_query,insert_value)
                conn.commit()
                conn.close()
                print("herrrrrrrrrrrrrrr----------------------------------")

                return redirect("/api/product_list")
            else:
                flash("Invalid email or password. Please try again.")
                return redirect("/api/login")

        return render_template("login.html")

    except Exception as e:
        print("Something Went Wrong")
        logger.error(e)
        insert_query = "Insert into Exceptions(exception_code,exception_date,exception_type,messages,IP,description) Values(%s,%s,%s,%s,%s,%s)"
        insert_value = (exception_code,date,type(e),e,"0.0.0.0","Got error in the login time")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        conn.close()
    
        
    return render_template("login.html")


@blueprint.route("/logout", methods=["POST", "GET"])
def logout():
        session.pop("authenticated")
        session.pop("email")

        return redirect("/api/login")


@blueprint.route("/change_password", methods=["POST", "GET"])
def change_password():
    try:
        if request.method == "POST":
            password = request.form["password1"]
            password2 = request.form["password2"]
            email = session["email"]
            if password == password2:
                conn = MysqlDB()
                mycursour = conn.cursor()
                update_query = "UPDATE Users SET password = %s WHERE email = %s"
                update_value = (password, email)
                mycursour.execute(update_query, update_value)
                insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
                insert_value = (date,"0.0.0.0","user changeing the password")
                mycursor.execute(insert_query,insert_value)
                conn.commit()
                conn.close()
                flash("Password changed Successfully")

                return render_template("change_password.html")
            else:
                flash("Password1 and Password2 not match")

                return render_template("change_password.html")
        else:
            return render_template("change_password.html")
    except Exception as e:
        print("Someting went wrong")
        logger.error(e)
        insert_query = "Insert into Exceptions(exception_code,exception_date,exception_type,messages,IP,description) Values(%s,%s,%s,%s,%s,%s)"
        insert_value = (exception_code,date,type(e),e,"0.0.0.0","Got error in the Change Password time")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        conn.close()

    return redirect("/api/change_password")


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


@blueprint.route("/import_csv_useingthread", methods=["POST", "GET"])
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
            return redirect("/api/login")
        return render_template("import_csv.html")

    except Exception as e:
        print("Someting went wrong")
        logger.error(e)
        insert_query = "Insert into Exceptions(exception_code,exception_date,exception_type,messages,IP,description) Values(%s,%s,%s,%s,%s,%s)"
        insert_value = (exception_code,date,type(e),e,"0.0.0.0","Got error in the upload csv time")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        conn.close()
    return redirect("/api/login")


@blueprint.route("/export_csv", methods=["POST", "GET"])
def export_csv():
    try:
        conn = MysqlDB()
        mycursour = conn.cursor()
        mycursour.execute("SELECT * FROM insert_dynamic_data_csv")
        data = mycursour.fetchall()
        df = pd.DataFrame(data, columns=[desc[0] for desc in mycursour.description])
        csv_data = df.to_csv()
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d %H:%M:%S") + ":products.csv"
        insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
        insert_value = (date,"0.0.0.0","user in the login")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        mycursour.close()
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

    return redirect("/api/export_csv")


@blueprint.route("/export_pdf", methods=["POST", "GET"])
def export_pdf():
    try:
        conn = MysqlDB()
        mycursor = conn.cursor()
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

    return redirect("/api/export_pdf")


def products(offset=None, per_page=None):
    conn = MysqlDB()
    mycursure = conn.cursor()
    mycursure.execute(f"SELECT * FROM Products LIMIT {per_page} OFFSET {offset}")
    datacursure = mycursure.fetchall()
    mycursure.close()
    conn.close()

    return datacursure


@blueprint.route("/product_list", methods=["GET", "POST"])
def product_list():
    conn = MysqlDB()
    mycurser = conn.cursor()
    mycurser.execute("SELECT * FROM Products")
    alldata = mycurser.fetchall()
    print(alldata)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    first_page = 1
    per_page = 3
    offset = (page - 1) * int(per_page)
    print("offset", offset)
    items = products(offset, per_page)
    print(items)
    conn = MysqlDB()
    mycursure = conn.cursor()
    mycursure.execute("SELECT * FROM Products")
    all_data = mycursure.fetchall()
    mycursure.close()
    total_page = (len(all_data) // per_page) + len(all_data) % per_page
    print("total page", total_page)
    if request.method == "POST":
        conn = MysqlDB()
        mycurser = conn.cursor()
        insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
        insert_value = (date,"0.0.0.0","user in productlisting")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        Product_id = request.form.getlist("product_id")
        print("product_id", Product_id)
        if Product_id == []:
            flash("Please select the product first")

            return redirect("/api/product_list")
        else:
            conn = MysqlDB()
            mycurser = conn.cursor()
            Product_id = request.form.getlist("product_id")
            delete_query = "DELETE FROM Products WHERE product_id in %s;"
            delete_value = (Product_id,)
            mycurser.execute(delete_query, delete_value)
            insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
            insert_value = (date,"0.0.0.0","user deleting product")
            mycursor.execute(insert_query,insert_value)
            conn.commit()
            conn.close()
            flash(f"Products {Product_id} has been deleted sucsessfully")

            return redirect("product_list")

    return render_template(
        "product_list.html",
        items=items,
        page=page,
        per_page=per_page,
        total_page=total_page,
        first_page=first_page,
    )


@blueprint.route("forgot_password_and_reset", methods=["POST", "GET"])
def forgot_password_and_reset():
    try:
        if request.method == "POST" and "email" in request.form:
            email = request.form["email"]
            print("workingggggggggggggggggggggggg", email)
            select_query = "select * from Users where email = %s;"
            mycursor.execute(select_query, (email,))
            user = mycursor.fetchone()
            insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
            insert_value = (date,"0.0.0.0","user trying to forgot password")
            mycursor.execute(insert_query,insert_value)
            conn.commit()
            print("userrrrrrrrrrrrrrrr", user)
            if user:
                print("currrrrrrrrrr", user)
                expiretime = datetime.now() + timedelta(minutes=5)
                exptime = int(datetime.timestamp(expiretime))
                token = str(uuid.uuid4())
                print("____________++++++++++++++", token)
                update_query = "UPDATE usertable SET expire_time = %s, token = %s where email = %s;"
                update_value = (exptime, token, email)
                mycursor.execute(update_query, update_value)
                mycursor.close()
                conn.commit()
                print("WE here___________________________")
                msg = Message(
                    "Forgot Password",
                    sender="amandubey@simprosys.com",
                    recipients=[email],
                )
                msg.body = f"Tap On the Link and Reset Your Password--   http://127.0.0.1:8000/api/reset_password/{token}"
                mail.send(msg)
                flash("Forgot Password Link Has been Sent On Your Mail")

                return render_template("forgot_password.html")

            else:
                flash("Something went wrong")

                return render_template("forgot_password.html")

        else:
            return render_template("forgot_password.html")

    except Exception as e:
        print("Something Went Wrong")
        logger.error(e)
        insert_query = "Insert into Exceptions(exception_code,exception_date,exception_type,messages,IP,description) Values(%s,%s,%s,%s,%s,%s)"
        insert_value = (exception_code,date,type(e),e,"0.0.0.0","Got error in the export_pdf time")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        conn.close()

    return render_template("forgot_password.html")


@blueprint.route("/reset_password/<token>", methods=["POST", "GET"])
def reset_password(token):
    try:
        conn = MysqlDB()
        mycurser = conn.cursor()
        select_query = "SELECT * FROM usertable where token = %s;"
        mycurser.execute(select_query, token)
        data = mycurser.fetchone()
        insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
        insert_value = (date,"0.0.0.0","user reseting password")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        date1 = datetime.now()
        exptime = int(datetime.timestamp(date1))
        print("workinggggggggggggggg hereeeeeeeeeeeee")
        if exptime < int(data[3]):
            if request.method == "POST" and "password" in request.form:
                password = request.form["password"]
                update_query = "UPDATE usertable set password = %s where token = %s;"
                update_value = (password, token)
                mycurser.execute(update_query, update_value)
                conn.commit()
                mycurser.close()
                flash("Your Password has been Changed Sucsessfullyyyy")

                return redirect("/api/login")
        else:
            flash("Link has been expired Please forgot password again")

            return redirect("/api/forgot_password_and_reset")

    except Exception as e:
        print("Something Went Wrong")
        logger.error(e)
        insert_query = "Insert into Exceptions(exception_code,exception_date,exception_type,messages,IP,description) Values(%s,%s,%s,%s,%s,%s)"
        insert_value = (exception_code,date,type(e),e,"0.0.0.0","Got error in the reset password time")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        conn.close()

    return render_template("reset_password.html")


app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True,port=8000)
