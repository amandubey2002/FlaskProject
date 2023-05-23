from flask import Flask,request,jsonify
from flask_jwt_extended import JWTManager,create_access_token,jwt_required
from Flask_APP.api.logg import logger
import pymysql as Pymysqldb
from flask_restful import Resource,Api
from datetime import timedelta
from .blueprint import rest_blueprint
from app_config import app
from userapp.models import conn,mycursor

app.config["JWT_SECRET_KEY"]= "jjdkjads834dmdk7"

# def MysqlDB():
#     conn = Pymysqldb.connect(
#     host = 'localhost',
#     user = 'root',
#     password = 'Dubey@123',
#     database = 'FlaskDB',
#     )
#     return conn



jwt = JWTManager(app)

@rest_blueprint.route("/token",methods=["POST"])
def token():
    # conn = MysqlDB()
    # mycurser = conn.cursor()
    email =request.json.get("email")
    password = request.json.get("password")
    sql = "select * from Users where email=%s and password=%s "
    value = (email,password)
    mycursor.execute(sql,value)
    user = mycursor.fetchone()
    if mycursor.rowcount==0:
        return jsonify({"message":" username or password"}),401
    elif mycursor.rowcount == 1:
        access_token = create_access_token(identity=user[0],expires_delta=timedelta(hours=1))
        return jsonify({ "token": access_token, "user_id": user[0] })   
    mycursor.close()  


class ProductApiView(Resource):
    
    @jwt_required()
    def get(self):
        try:
            # conn = MysqlDB()
            # mycusrsor = conn.cursor()
            mycursor.execute("SELECT * FROM Products")
            records = mycursor.fetchall()
            sorted_data = sorted(records)
            all_data = []
            for record in sorted_data:
                all_data.append({'id':record[0],'handle':record[1],'title':record[2],'body':record[3],'vendor':record[4],'type':record[5],'tags':record[6],'published':record[7],'variant_sku':record[8],'variant_inventory_tracker':record[9],'Variant_Price':record[10],'image__src':record[11]})
            return {"Data":all_data,"total_data":len(all_data)}
        except:
            print("Something went wrong")
    
    @jwt_required()
    def post(self):
        try:
            if request.method=='POST':
                # conn = MysqlDB()
                # mycusrsor = conn.cursor()
                id = request.form['id']
                print(id)
                Handle = request.form['handle']
                Title = request.form['title']
                Body = request.form['body']
                Vendor = request.form['vendor']
                Type = request.form['type']
                Tags = request.form['tags']
                Published = request.form['published']
                print('here')
                Variant_SKU = request.form['variant_sku']
                Variant_Inventory_Tracker = request.form['variant_inventory_tracker']
                print("here")
                Variant_Price = request.form['variant_price']
                print("here")
                print(Variant_Price)
                print("here")
                Image_Src = request.form['image__src']
                print(Image_Src)
                sql = "INSERT INTO Products(product_id,Handle,Title,Body,Vendor,Type,Tags,Published,VariantSKU,VariantInventoryTracker,VariantPrice,ImageSrc) Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                value = (id,Handle,Title,Body,Vendor,Type,Tags,Published,Variant_SKU,Variant_Inventory_Tracker,Variant_Price,Image_Src)
                mycursor.execute(sql,value)
                conn.commit()
                conn.close()
                return {"msg": "Data has been successfully Added","Data":value}
            else:
                return {"Msg":"Method NoT allowed"}
        except Exception as e:
            logger.error(e)
            print(e)
            
            
            
class ProductAPi(Resource):
    @jwt_required()
    def get(self,id):
        try:
            # conn = MysqlDB()
            # mycusrsor = conn.cursor()
            mycursor.execute("SELECT * FROM Products WHERE product_id = %s",(id,))
            record = mycursor.fetchone()
            print(record)
            if record is None:
                return jsonify({"data":"No data Found"})
            else:
                return jsonify({"data":record})
                
        except Exception as e:
            print(f"Something went wrong {e}")
            logger.error(e)

    @jwt_required()
    def put(self,id):
        try:
            # conn = MysqlDB()
            # mycusrsor = conn.cursor()
            mycursor.execute("SELECT * FROM Products WHERE product_id = %s",(id,))
            records = mycursor.fetchone()
            if records is not None:
                id = request.json['product_id']
                Handle = request.json['handle']
                Title = request.json['title']
                Body = request.json['body']
                Vendor = request.json['vendor']
                Type = request.json['type']
                Tags = request.json['tags']
                Published = request.json['published']
                Variant_SKU = request.json['variant_sku']
                Variant_Inventory_Tracker = request.json['variant_inventory_tracker']
                Variant_Price = request.json['variant_price']
                Image_Src = request.json['image__src']
                sql = "UPDATE Products SET handle=%s,title=%s,body=%s,vendor=%s,type=%s,tags=%s,published=%s,variant_sku=%s,variant_inventory_tracker=%s,variant_price=%s,image_src=%s where product_id = %s"
                value = (Handle,Title,Body,Vendor,Type,Tags,Published,Variant_SKU,Variant_Inventory_Tracker,Variant_Price,Image_Src,id)
                mycursor.execute(sql,value)
                conn.commit()
                conn.close()
                return {'msg':'Data Has been Updated Sucsessfully','Data':value}
        except Exception as e:
            print(e)

    @jwt_required()
    def delete(Self,id):
        try:
            # conn = MysqlDB()
            # mycusrsor = conn.cursor()
            mycursor.execute("DELETE FROM Products WHERE product_id = %s",(id,))
            conn.commit()
            mycursor.close()

            if mycursor.rowcount == 0:
                return "No Data Found"
            else:
                return "Data Has been Deleted Sucsessfully"
        except Exception as e:
            print(e)
            logger.error(e)


product_route = ProductApiView.as_view("product_route")  
product1_route = ProductAPi.as_view("product1_route")

rest_blueprint.add_url_rule("/Products",view_func=product_route)
rest_blueprint.add_url_rule("/Products/<int:id>",view_func=product1_route)





