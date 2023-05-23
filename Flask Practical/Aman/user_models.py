from flask import Flask
import pymysql as Pymysqldb



def MysqlDB():
    conn = Pymysqldb.connect(
    host = 'localhost',
    user = 'root',
    password = 'Dubey@123',
    database = 'FlaskDB',
    )
    return conn



conn = MysqlDB()
mycursor = conn.cursor()

mycursor.execute(
    """
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255)
        );
    """
)


mycursor.execute(
    """
        CREATE TABLE IF NOT EXISTS Users_Activity (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        user_activity_date VARCHAR(255),
        IP VARCHAR(255),
        description VARCHAR(255)
        );
    """
)


mycursor.execute(
    """
        CREATE TABLE IF NOT EXISTS Exceptions (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        exception_code VARCHAR(255),
        exception_date VARCHAR(255),
        exception_type varchar(255),
        messages text,
        IP VARCHAR(255),
        description VARCHAR(255)
        );
    """
)

conn.commit()
