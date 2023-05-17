from flask import Flask,request,jsonify
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,jwt_required,get_jwt_identity
from logg import logging
import pymysql as Pymysqldb
from flask_restful import Resource,Api
from datetime import timedelta



app =Flask(__name__)

app.config["JWT_SECRET_KEY"]= "jjdkjads834dmdk7"

api = Api(app)

def MysqlDB():
    conn = Pymysqldb.connect(
    host = 'localhost',
    user = 'root',
    password = 'Dubey@123',
    database = 'FlaskDB',
    )
    return conn



jwt = JWTManager(app)

@app.route("/token",methods=["POST"])
def token():
    conn = MysqlDB()
    mycurser = conn.cursor()
    email =request.json.get("email")
    password = request.json.get("password")
    sql = "select * from Users where email=%s and password=%s "
    value = (email,password)
    mycurser.execute(sql,value)
    user = mycurser.fetchone()
    if mycurser.rowcount==0:
        return jsonify({"message":" username or password"}),401
    elif mycurser.rowcount == 1:
        access_token = create_access_token(identity=user[0],expires_delta=timedelta(hours=1))
        return jsonify({ "token": access_token, "user_id": user[0] })   
    mycurser.close()  


class ProductApiView(Resource):
    
    @jwt_required()
    def get(self):
        try:
            conn = MysqlDB()
            mycusrsor = conn.cursor()
            mycusrsor.execute("SELECT * FROM Products")
            records = mycusrsor.fetchall()
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
                conn = MysqlDB()
                mycusrsor = conn.cursor()
                id = request.form['id']
                Handle = request.form['handle']
                Title = request.form['title']
                Body = request.form['body']
                Vendor = request.form['vendor']
                Type = request.form['type']
                Tags = request.form['tags']
                Published = request.form['published']
                Variant_SKU = request.form['variant_sku']
                Variant_Inventory_Tracker = request.form['variant_inventory_tracker']
                Variant_Price = request.form['variant_price']
                Image_Src = request.form['image__src']
                sql = "INSERT INTO Products(product_id,Handle,Title,Body,Vendor,Type,Tags,Published,VariantSKU,VariantInventoryTracker,VariantPrice,ImageSrc) Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                value = (id,Handle,Title,Body,Vendor,Type,Tags,Published,Variant_SKU,Variant_Inventory_Tracker,Variant_Price,Image_Src)
                mycusrsor.execute(sql,value)
                conn.commit()
                conn.close()
                return {"msg": "Data has been successfully Added","Data":value}
            else:
                return {"Msg":"Method NoT allowed"}
        except Exception as e:
            logging.error(e)
            print(e)
            
            
            
class ProductAPi(Resource):
    @jwt_required()
    def get(self,id):
        try:
            conn = MysqlDB()
            mycusrsor = conn.cursor()
            mycusrsor.execute("SELECT * FROM Products WHERE product_id = %s",(id,))
            record = mycusrsor.fetchone()
            print(record)
            if record is None:
                return jsonify({"data":"No data Found"})
            else:
                return jsonify({"data":record})
                
        except Exception as e:
            print(f"Something went wrong {e}")
            logging.error(e)

    @jwt_required()
    def put(self,id):
        try:
            conn = MysqlDB()
            mycusrsor = conn.cursor()
            mycusrsor.execute("SELECT * FROM Products WHERE product_id = %s",(id,))
            records = mycusrsor.fetchone()
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
                mycusrsor.execute(sql,value)
                conn.commit()
                conn.close()
                return {'msg':'Data Has been Updated Sucsessfully','Data':value}
        except Exception as e:
            print(e)

    @jwt_required()
    def delete(Self,id):
        try:
            conn = MysqlDB()
            mycusrsor = conn.cursor()
            mycusrsor.execute("DELETE FROM Products WHERE product_id = %s",(id,))
            conn.commit()
            mycusrsor.close()

            if mycusrsor.rowcount == 0:
                return "No Data Found"
            else:
                return "Data Has been Deleted Sucsessfully"
        except Exception as e:
            print(e)
            logging.error(e)


api.add_resource(ProductApiView,'/Products')
api.add_resource(ProductAPi,'/Products/<int:id>')  

          
if __name__=="__main__":
    app.run(debug=True,port=8000)
