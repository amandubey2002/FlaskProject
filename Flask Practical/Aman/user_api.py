from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    flash,
    url_for,
    Blueprint
)
from flask_security import roles_accepted
import uuid
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from logg import logger
from login_rquired import login_required,admin_login_required
from models import conn,mycursor
app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "amandubey@simprosys.com"
app.config["MAIL_PASSWORD"] = "zsuoyovnmxuqceam"
app.config["MAIL_USE_TLS"] = True

mail = Mail(app)

user_blueprint = Blueprint("user_blueprint",__name__,url_prefix="/user")

exception_code = 40
date = datetime.now()



@user_blueprint.route("/signup", methods=["POST", "GET"])
def signup():
    try:
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
            # password = generate_password_hash(password1)
            if not username or not email or not password:
                flash("All fields are required")

                return redirect(url_for("user_blueprint.signup"))
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
        print("Something Went Wrong",e)
        logger.error(e)

    return redirect(url_for("user_blueprint.login"))


@user_blueprint.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST" and "password" in request.form and "email" in request.form:
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
            # session["email"] = email
            insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
            insert_value = (date,"0.0.0.0","user in the login")
            mycursor.execute(insert_query,insert_value)
            conn.commit()
            print("herrrrrrrrrrrrrrr----------------------------------")

            return redirect(url_for("product_blueprint.product_list"))
        else:
            flash("Invalid email or password. Please try again.")
            return redirect(url_for("user_blueprint.login"))

    return render_template("login_user.html")



@user_blueprint.route("/logout", methods=["POST", "GET"])
def logout():
        session.pop("authenticated")
        # session.pop("email")
        return redirect(url_for("user_blueprint.login"))


@user_blueprint.route("/change_password", methods=["POST", "GET"])
@login_required
def change_password():
    try:
        if request.method == "POST":
            password = request.form["password1"]
            password2 = request.form["password2"]
            email = session["email"]
            if password == password2:
                update_query = "UPDATE Users SET password = %s WHERE email = %s"
                update_value = (password, email)
                mycursor.execute(update_query, update_value)
                insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
                insert_value = (date,"0.0.0.0","user changeing the password")
                mycursor.execute(insert_query,insert_value)
                conn.commit()
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

    return redirect("user_blueprint.change_password")



@user_blueprint.route("forgot_password_and_reset", methods=["POST", "GET"])
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
                msg.body = f"Tap On the Link and Reset Your Password--   http://127.0.0.1:8000/user/reset_password/{token}"
                mail.send(msg)
                flash("Forgot Password Link Has been Sent On Your Mail")

                return render_template("forgot_password.html")

            else:
                flash("No user with this email")

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


@user_blueprint.route("/reset_password/<token>", methods=["POST", "GET"])
def reset_password(token):
    try:
        select_query = "SELECT * FROM usertable where token = %s;"
        mycursor.execute(select_query, token)
        data = mycursor.fetchone()
        insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
        insert_value = (date,"0.0.0.0","user reseting password")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        date1 = datetime.now()
        exptime = int(datetime.timestamp(date1))
        if exptime < int(data[3]):
            if request.method == "POST" and "password" in request.form:
                password = request.form["password"]
                update_query = "UPDATE usertable set password = %s where token = %s;"
                update_value = (password, token)
                mycursor.execute(update_query, update_value)
                conn.commit()
                mycursor.close()
                flash("Your Password has been Changed Sucsessfullyyyy")

                return redirect("user_blueprint.login")
        else:
            flash("Link has been expired Please forgot password again")

            return redirect("user_blueprint.forgot_password_and_reset")

    except Exception as e:
        print("Something Went Wrong")
        logger.error(e)
        insert_query = "Insert into Exceptions(exception_code,exception_date,exception_type,messages,IP,description) Values(%s,%s,%s,%s,%s,%s)"
        insert_value = (exception_code,date,type(e),e,"0.0.0.0","Got error in the reset password time")
        mycursor.execute(insert_query,insert_value)
        conn.commit()
        conn.close()

    return render_template("reset_password.html")



@user_blueprint.route("/admin_dashboard",methods=["GET","POST"])
@admin_login_required
def admin_dashboard():
    select_query = "Select * from Users"
    mycursor.execute(select_query)
    users = mycursor.fetchall()
    return render_template("admin_dashboard.html",users=users)
    
    
@user_blueprint.route("/admin_user_add",methods=["GET","POST"])
@admin_login_required
def admin_user_add():
    if request.method=="POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['usertype']
        if not username or not email or not password or not role:
            flash("All fields are required")

            return redirect(url_for("user_blueprint.admin_dashboard"))
        
        else:
            insert_query = "Insert into Users(username,email,password,role) values(%s,%s,%s,%s)"
            insert_value = (username,email,password,role)
            mycursor.execute(insert_query,insert_value)
            conn.commit()
            flash("User added Sucsessfully")
            
            return redirect(url_for("user_blueprint.admin_dashboard"))
        
    else:
        
            return render_template("add_user.html")
        
@user_blueprint.route("/admin_login/", methods=["POST", "GET"])
def admin_login():
    if request.method == "POST" and "password" in request.form and "email" in request.form:
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["usertype"]
        select_query = "SELECT * FROM Users WHERE email = %s and password = %s and (role = 'admin' or role = 'staff')"
        select_value = (email, password)
        mycursor.execute(select_query, select_value)
        user = mycursor.fetchone()
        if user:
            session["authenticated"] = True
            session['role'] = role
            insert_query = "Insert into Users_Activity(user_activity_date,IP,description) Values(%s,%s,%s)"
            insert_value = (date,"0.0.0.0","admin_user in the login")
            mycursor.execute(insert_query,insert_value)
            conn.commit()

            return redirect(url_for("user_blueprint.admin_dashboard"))
        else:
            flash("Invalid email or password. Please try again.")
            
            return redirect(url_for("user_blueprint.admin_login"))

    return render_template("login_admin.html")


@user_blueprint.route("/admin_logout", methods=["POST", "GET"])
def admin_logout():
        session.pop("authenticated")
        session.pop("role")

        return redirect(url_for("user_blueprint.admin_login"))

@user_blueprint.route("/update_user/<int:id>",methods=["GET","POST"])
@admin_login_required
def update_user(id):
    print("this is id",id)
    select_query = "select * from Users where id = %s"
    select_value = (id)
    mycursor.execute(select_query,select_value)
    data = mycursor.fetchall()
    main_data = data[0]
    username = main_data[1]
    email = main_data[2]
    password = main_data[3]
    role = main_data[4]
    
    if request.method=="POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form['role']
        update_query = "Update Users set username = %s ,email = %s ,password = %s, role = %s where id = %s"
        update_value = (username,email,password,role,id)
        mycursor.execute(update_query,update_value)
        conn.commit()
        return redirect(url_for("user_blueprint.admin_dashboard"))
        
    return render_template("update_user.html",username=username,email=email,password=password,role=role,id=id)


@user_blueprint.route("/delete_user/<int:id>",methods=["GET","POST"])
@admin_login_required
def delete_user(id):
    select_query = "DELETE from Users where id = %s"
    select_value = (id)
    mycursor.execute(select_query,select_value)
    conn.commit()
    flash("user has been deleted sucsessfully")
    return redirect(url_for("user_blueprint.admin_dashboard"))