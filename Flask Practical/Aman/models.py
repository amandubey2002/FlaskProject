import pymysql as Pymysqldb
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
