import mysql.connector as mc

sql = mc.connect(host='localhost', user = 'root', password='1234')
cur = sql.cursor()
name = input("Enter Name: ")

cur.execute(f"CREATE DATABASE IF NOT EXISTS {name.lower()}_project;")
cur.execute(f"USE {name.lower()}_project;")
cur.execute("CREATE TABLE IF NOT EXISTS UserData(NAME VARCHAR(255), UNAME VARCHAR(255) PRIMARY KEY, DECRIP VARCHAR(255), EMAIL VARCHAR(255) NOT NULL, PWD VARCHAR(255) NOT NULL, POSTCOUNT INT DEFAULT 0, TYPE ENUM('user', 'shop', 'root'));")
cur.execute("CREATE TABLE IF NOT EXISTS ProductData(PID VARCHAR(4) PRIMARY KEY, UNAME VARCHAR(255) NOT NULL, CAPTION VARCHAR(255), IMG LONGBLOB NOT NULL, PRICE INT NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS FollowData(FrUname VARCHAR(255) NOT NULL, FdUname VARCHAR(255) NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS CommentData(CID VARCHAR(4) PRIMARY KEY, PID VARCHAR(4) NOT NULL, UNAME VARCHAR(255) NOT NULL, TEXT VARCHAR(255) NOT NULL)")

sql.close()
