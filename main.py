from tkinter.filedialog import askopenfile
from difflib import get_close_matches
from prettytable import PrettyTable
import mysql.connector as mysql
from getpass import getpass
from tkinter import Tk
from io import BytesIO
from os import system
from PIL import Image

#Init
sql = mysql.connect(host='localhost', user = 'root', password='1234', database='syon_project')
cur = sql.cursor()
Tk().withdraw()

def cls():
	system('cls')

#For Auto IDS
def increment(col, table):
	cur.execute(f'SELECT {col} from {table};')
	try:
		last = (cur.fetchall()[-1][0])
		return str(last)[0]+f"{int((str(last)[1:]))+1 :03d}"
	except:
		return col[0].upper()+'001'

#Enforce 255 char limit for SQL
def check255(prompt):
	while True:
		inp = input(prompt)
		if len(inp)<=255:
			return inp
		else:
			print("Max char 255\n\n")

#For easy access of single coloums
def getCol(col, table):
	cur.execute(f'SELECT {col} from {table}')
	l = []
	for row in cur.fetchall():
		l.append(row[0])
	return l

#Signup function
def signup(type):
	cls()
	match type:
		case '1':
			name = input("Enter Shop Name: ")
			desc = check255("Enter a description of your store(max 255 char): ")
			type = 'shop'
		case '2':
			name = input("Enter Your Name: ")
			desc = None
			type = 'user'

	email = input("Enter email: ")
	pwd = getpass("Enter password: ")
	
	if getpass("Enter password once again: ") == pwd:
		pass
	else:
		system('py TEST.py')


	cur.execute('INSERT INTO UserData VALUES(%s, %s, %s, %s, %s, %s, %s)', (name, uname, desc, email, pwd, 0, type))
	sql.commit()

#For easy access of single values
def getOne(col, table, cond, val):
	cur.execute(f'SELECT {col} from {table} where {cond}="{val}";')
	return cur.fetchone()[0]

#For easy access of one row
def getRow(table, cond, val):
	cur.execute(f'SELECT * FROM {table} WHERE {cond}="{val}";')
	return cur.fetchall()[0]

#Seller main page
def shop():
	cls()
	match input('1. Create Post\
				   2. Browse Posts\
				   3. Edit Profile:\n'):
		case '1':
			cls()
			cur.execute("INSERT INTO ProductData VALUES(%s, %s, %s, %s, %s)", (increment('pid', 'productdata'), uname, input("Enter Caption(blank for none): "), askopenfile(mode = 'rb', filetypes=("Image Files", "*.png *.jpg")).read(), int(input("Price of item: "))))
		case '2':
			browse()
	sql.commit()
	print("Product Added Successfully!")
	shop()

#Main Browsing Page
def browse():
	cur.execute('select * from productdata;')
	products = cur.fetchall()

	for i in range(1, len(products)+1):
		print(f"{i}. {products[i-1][2]}\tPrice: {products[i-1][4]}")

	x = input("Item No(exit to leave): ")
	if x.isdigit():
		productPage(products[int(x)-1][0])
	else:
		print("Thank you for visiting\nExiting...")
		exit()

#Comment on Products
def comment(pid):
	cur.execute('INSERT INTO CommentData VALUES(%s, %s, %s, %s)', (increment('CID', 'CommentData'), pid, uname, check255("Enter Caption: ")))
	sql.commit()

#Product page template
def productPage(pid):

	data=getRow("productdata", 'pid', pid)
	print(f"{data[2]}\nPrice: {data[4]} INR\n")
	
	print(f"Comments:\n")
	for i in getRow('CommentData', 'pid', pid):
		print(f'@{i[2]}:\n{i[3]}\n')

	Image.open(BytesIO(data[3])).show()
	match input("1. Comment\n2. Go Back\n"):
		case "1":
			comment(pid)
		case "2":
			browse()

#Spellcheck
def ifExists(value:str):

	if value.title() in getCol("NAME", "UserData"):
		return value
	else:
		guess = get_close_matches(value, getCol("NAME", "UserData"))

	if guess!=[] and input(f"Object not found\nDid you mean: {guess[0]}?\n").lower()[0] == 'y':
		for i in range(len(guess)):
			print(f'{i+1}. {guess[i]}')
		return guess[int(input("Did you mean to input any of thses?\n"))-1]
	else:
		print("It seems that we do not have that in our registry")

#Quick Table
def table(title):
	t = PrettyTable()
	t.field_names = [i[0] for i in cur.description]
	t.add_rows(cur.fetchall())
	print(f"{title}\n{t}\n\n")         

#Admin Page
def root():
	cls()
	match input("1. Browse\n2. Search for shops\n3. View tables\n4. Ban user\n5. Delete Post\n6. SQL console\n7. Logout\n"):

		case "1":
			browse()
			root()

		case "2":
			productPage(ifExists(input("Enter shop name: ")))
			root()

		case "3":
			cur.execute("SELECT * FROM Userdata;")
			table("USERDATA")
			cur.execute("SELECT PID, uname, CAPTION, PRICE from ProductData;")
			table("PRODUCTDATA")
			input()
			root()

		case "4":
			name = input("Enter username of user: ")
			if input("Are you sure(y/n):")[0].lower() =='y':
				cur.execute(f'DELETE FROM USERDATA WHERE UNAME="{name}"')
				sql.commit()
			else:
				print("Cancelling...")
			input()
			root()

		case "5":
			pid = input("Enter pid: ")
			if input("Are you sure(y/n):")[0].lower() =='y':
				cur.execute(f'DELETE FROM Productdata WHERE PID="{pid}"')
				sql.commit()
			else:
				print("Cancelling...")
			input()
			root()

		case "6":
			query = ""
			while query != 'exit':
				query = input("mysql> ")
				cur.execute(query)
			try:
				sql.commit()
			except:
				pass
			root()
			
		case "7":
			print("Logging Out...")
			exit()

##Main.py##
uname = input('Username: ')
#root
if uname == 'root':
	if getpass('Password: ').encode('utf-8').hex() == '70617373776f7264':
		root()
	else:
		print("Incorrect password\nExiting...")

#signin
elif uname in getCol('uname', 'UserData'):
		
		pwd = getpass("Enter Password: ")
		if pwd == getOne('pwd', 'userdata', 'UNAME', uname):
			pass
		else:
			input(f"Incorrect password!\nTry again later")
			
			exit()

#signup
else:
	signup(input("Are you a:\n1. Seller\n2. Shopper\n"))

if getOne('type', 'userdata', 'uname', uname) == 'shop':
	shop()
else:
	browse()

sql.close()