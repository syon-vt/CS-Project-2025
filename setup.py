import mysql.connector as mc
from pickle import dumps


sql = mc.connect(host='localhost', user = 'root', password='1234')
cur = sql.cursor()
name = input("Enter Name: ")
sql.autocommit = True
cur.execute(f"CREATE DATABASE IF NOT EXISTS {name.lower()}_project;")
cur.execute(f"USE {name.lower()}_project;")
cur.execute("CREATE TABLE IF NOT EXISTS UserData(NAME VARCHAR(255), UNAME VARCHAR(255) PRIMARY KEY, DESCRIPTION VARCHAR(255), EMAIL VARCHAR(255) NOT NULL, PWD VARCHAR(255) NOT NULL, POSTCOUNT INT DEFAULT 0, CART LONGBLOB);")
cur.execute("CREATE TABLE IF NOT EXISTS ProductData(PID VARCHAR(4) PRIMARY KEY, UNAME VARCHAR(255) NOT NULL, CAPTION VARCHAR(255), IMG LONGBLOB NOT NULL, PRICE INT NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS CommentData(CID VARCHAR(4) PRIMARY KEY, PID VARCHAR(4) NOT NULL, UNAME VARCHAR(255) NOT NULL, TEXT VARCHAR(255) NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS LikeData(PID VARCHAR(4), UNAME VARCHAR(255))")
cur.execute("CREATE TABLE IF NOT EXISTS RequestData(RID VARCHAR(255), SELLER VARCHAR(255), BUYER VARCHAR(255), PID VARCHAR(4), STATUS VARCHAR(255))")
cur.execute("INSERT INTO UserData VALUES(%s, %s, %s, %s, %s, %s, %s)", ('Guest', 'Guest', 'Description', 'example@email.com', 'password', 0, dumps([])))
cur.execute("UPDATE UserData SET CART=%s", (dumps([]),))
sql.close()
