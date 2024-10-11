from tkinter.filedialog import askopenfile
from difflib import get_close_matches
from prettytable import PrettyTable
import mysql.connector as mc
from getpass import getpass
from os import system
from tkinter import Tk
from PIL import Image
from io import BytesIO
from pickle import dumps, loads
from logging import error

def init():
	global sql
	global cur
	global uname
	sql = mc.connect(host='localhost', user = 'root', password='1234', database='syon_project')
	cur = sql.cursor(buffered=True)
	sql.autocommit = True
init()

def getCol(col, table):
	cur.execute(f'SELECT {col} from {table}')
	l = []
	for row in cur.fetchall():
		l.append(row[0])
	return l

def getRow(table, cond, val):
	cur.execute(f'SELECT * FROM {table} WHERE {cond}="{val}";')
	rows = cur.fetchall()

	return rows
	
def getOne(col, table, cond, val):
	cur.execute(f'SELECT {col} from {table} where {cond}="{val}"')
	return cur.fetchone()[0]

def addComment(pid, uname, caption):
	cur.execute('INSERT INTO CommentData VALUES(%s, %s, %s, %s)', (increment('cid', 'commentdata'), pid, uname, caption))
	#sql.commit()
	
def upload(uname, cap, price, img):
	cur.execute("INSERT INTO ProductData VALUES(%s, %s, %s, %s, %s)", (increment('pid', 'productdata'), uname, cap, img, price))
	cur.execute("UPDATE UserData SET POSTCOUNT = POSTCOUNT+1 WHERE uname=%s", (uname,))
	#sql.commit()

def edit(uname, newdata):
	sql.autocommit = False
	try:
		cur.execute('delete from userdata where uname=%s', (uname,))
		cur.execute('insert into userdata values(%s, %s, %s, %s, %s, %s, %s)', newdata)
	except Exception as e:
		sql.rollback()
	sql.commit()
	sql.autocommit = True
	
def clmnheads(table):
	cur.execute(f"SELECT * FROM {table} where uname='1'")
	return [i[0] for i in cur.description]

def all():
	cur.execute("SELECT * from ProductData;")
	return cur.fetchall()

def increment(col, table):
	cur.execute(f'SELECT {col} from {table};')
	try:
		last = (cur.fetchall()[-1][0])
		return str(last)[0]+f"{int((str(last)[1:]))+1 :03d}"
	except:
		return col[0].upper()+'001'
	
def postcount(uname):
	c=0
	for product in all():
		if product[1].lower() == uname.lower():
			c+=1
	return c

def signup(name, uname, decrip, email, pwd):
	cur.execute("INSERT INTO UserData VALUES(%s, %s, %s, %s, %s, %s, %s)", (name, uname, decrip, email, pwd, 0, dumps([])))
	#sql.commit()
	
def checklike(uname, pid):
	if pid in getCol('pid', 'LikeData') and getRow('LikeData', 'pid', pid)[0][1] == uname:
		return True
	return False

def addlike(uname, pid):
	cur.execute("SELECT * FROM LikeData WHERE PID=%s AND UNAME=%s", (pid, uname))
	if not cur.fetchall():
		cur.execute("INSERT INTO LikeData VALUES(%s, %s)", (pid, uname))
		#sql.commit()

def remlike(uname, pid):
	cur.execute("DELETE FROM LikeData WHERE PID=%s AND UNAME=%s", (pid, uname))
	#sql.commit()

def likecount(pid):
	cur.execute('SELECT * FROM LikeData WHERE PID=%s', (pid,))
	return len(cur.fetchall())

def getcart(uname):
	return loads(getOne('CART', 'UserData', 'uname', uname))

def addtocart(uname, pid):
	cart = getcart(uname)
	cart.append(pid)
	cur.execute("UPDATE UserData SET CART=%s WHERE UNAME=%s", (dumps(cart), uname))
	#sql.commit()

def remfromcart(uname, pid):
	cart = getcart(uname)
	cart.remove(pid)
	cur.execute("UPDATE UserData SET CART=%s WHERE UNAME=%s", (dumps(cart), uname))
	#sql.commit()

