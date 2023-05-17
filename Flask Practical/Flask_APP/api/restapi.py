from flask import Flask,request,jsonify
from flask_restful import Resource,Api
import pymysql as Pymysqldb
from logg import logger
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,jwt_required,get_jwt_identity
from flask.views import MethodView
from models import MysqlDB

app = Flask(__name__)

app.secret_key = b'ghjkjlkgfdfghjkl98797980989jhgfghjkl'

jwt = JWTManager(app)

api = Api(app)




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
    
    
    def post(self):
        try:
            if request.method=='POST':
                conn = MysqlDB()
                mycusrsor = conn.cursor()
                id = request.json['id']
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
                sql = "INSERT INTO Products(product_id,Handle,Title,Body,Vendor,Type,Tags,Published,VariantSKU,VariantInventoryTracker,VariantPrice,ImageSrc) Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                value = (id,Handle,Title,Body,Vendor,Type,Tags,Published,Variant_SKU,Variant_Inventory_Tracker,Variant_Price,Image_Src)
                mycusrsor.execute(sql,value)
                conn.commit()
                conn.close()
                return {"msg": "Data has been successfully Added","Data":value}
            else:
                
                return {"Msg":"Method NoT allowed"}
            
        except Exception as e:
            print(e)
            logger.error(e)





class ProductAPi(Resource):
    @jwt_required()
    def get(self,id):
        try:
            conn = MysqlDB()
            mycusrsor = conn.cursor()
            mycusrsor.execute("SELECT * FROM Products WHERE id = %s",(id,))
            record = mycusrsor.fetchone()
            print(record)
            if record is None:
                
                return jsonify({"data":"No data Found"})
            else:
                
                return jsonify({"data":record})
                
        except Exception as e:
            print("Something went wrong")
            logger.error(e)

    @jwt_required()
    def put(self,id):
        try:
            conn = MysqlDB()
            mycusrsor = conn.cursor()
            mycusrsor.execute("SELECT * FROM Products WHERE id = %s",(id,))
            records = mycusrsor.fetchone()
            if records is not None:
                id = request.json['id']
                Handle = request.json['handle']
                Title = request.json['title']
                Body = request.json['body']
                Vendor = request.json['vendor']
                Type = request.json['type']
                Tags = request.json['tags']
                Published = request.json['published']
                Variant_SKU = request.json['variant.as_view(),_sku']
                Variant_Inventory_Tracker = request.json['variant_inventory_tracker']
                Variant_Price = request.json['variant_price']
                Image_Src = request.json['image__src']
                sql = "UPDATE Products SET handle=%s,title=%s,body=%s,vendor=%s,type=%s,tags=%s,published=%s,variant_sku=%s,variant_inventory_tracker=%s,variant_price=%s,image_src=%s where id = %s"
                value = (Handle,Title,Body,Vendor,Type,Tags,Published,Variant_SKU,Variant_Inventory_Tracker,Variant_Price,Image_Src,id)
                mycusrsor.execute(sql,value)
                conn.commit()
                mycusrsor.close()
                conn.close()
                
                return {'msg':'Data Has been Updated Sucsessfully','Data':value}
            
        except Exception as e:
            print(e)
            logger.error(e)

    @jwt_required()
    def delete(Self,id):
        try:
            conn = MysqlDB()
            mycusrsor = conn.cursor()
            mycusrsor.execute("DELETE FROM Products WHERE id = %s",(id,))
            conn.commit()
            mycusrsor.close()

            if mycusrsor.rowcount == 0:
                
                return "No Data Found"
            else:
                
                return "Data Has been Deleted Sucsessfully"
            
        except Exception as e:
            print(e)


api.add_resource(ProductApiView,'/Products')

api.add_resource(ProductAPi,'/Products/<int:id>')



if __name__=="__main__":
    app.run(debug=True,port=8000)