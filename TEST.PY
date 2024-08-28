import mysql.connector as mc
from getpass import getpass
from os import system
from tkinter.filedialog import askopenfile
from tkinter import Tk
from PIL import Image
from difflib import get_close_matches
from io import BytesIO
from prettytable import PrettyTable


Tk().withdraw()

sql = mc.connect(host='localhost', user = 'root', password='1234', database='syon_project')
cur = sql.cursor()
uname = 'reliefmedicals'#input('Username: ')


def cls():
	system('cls')

def increment(col, table):
	cur.execute(f'SELECT {col} from {table};')
	try:
		last = (cur.fetchall()[-1][0])
		return str(last)[0]+f"{int((str(last)[1:]))+1 :03d}"
	except:
		return col[0].upper()+'001'
	
def getCol(col, table):
	cur.execute(f'SELECT {col} from {table}')
	l = []
	for row in cur.fetchall():
		l.append(row[0])
	return l

def getRow(table, cond, val):
	cur.execute(f'SELECT * FROM {table} WHERE {cond}="{val}";')
	rows = cur.fetchall()
	if len(rows) == 1:
		return rows[0]
	else:
		return rows

def signup(type):
	match type:
		case '1':
			name = input("Enter Shop Name: ")
			desc = check255("Enter a description of your store(max 255 char): ")
			
		case '2':
			name = input("Enter Your Name: ")
			desc = None

	email = input("Enter email: ")
	pwd = getpass("Enter password")
	
	if getpass("Enter password once again: ") == pwd:
		pass
	else:
		system('py TEST.py')


	cur.execute('INSERT INTO UserData VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', (increment('UID', 'UserData'), name, uname, desc, email, pwd, 0, type))
	sql.commit()

def getOne(col, table, cond, val):
	cur.execute(f'SELECT {col} from {table} where {cond}="{val}";')
	return cur.fetchone()[0]

def shop():
	cls()
	match input('1. Create Post\
				   2. Browse Posts\
				   3. Edit Profile\n'):
		case '1':
			cls()
			try:
				cur.execute("INSERT INTO ProductData VALUES(%s, %s, %s, %s)", (increment('pid', 'productdata'), uname, input("Enter Caption(blank for none): "), askopenfile(mode = 'rb', filetypes=[('Image File', '*.png'), ('Image File','*.jpg')]).read()))
			except AttributeError:
				print("Image Not Selected")
				shop()
		case '2':
			browse()
		case '3':
			cls()
			cur.execute(f'UPDATE UserData SET {input("What do you want to update(Name, Description, Email, Password):")} = "{input("Enter new Value: ")}" WHERE uname = "{uname}" ')

			if input("Are you sure(y/n): ").lower()[0] != 'y':
				print("Changed")

	sql.commit()

def browse():
	cls()
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
	
def productPage(pid):

	data=getRow("productdata", 'pid', pid)
	print(f"{data[2]}\nPrice: {data[4]} INR\n")
	print(f"Comments:")
	for i in getCol('pid', 'commentdata'):
		comment = (getRow('CommentData', 'pid', pid))
		print(f'@{comment[2]}:\n{comment[3]}\n')

	#Image.open(BytesIO(data[3])).show()
	match input("1. Comment\n2. Go Back\n"):
		case "1":
			comment(pid)
		case "2":
			browse()

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

def table(title):
	t = PrettyTable()
	t.field_names = [i[0] for i in cur.description]
	t.add_rows(cur.fetchall())
	print(f"{title}\n{t}\n\n")

def root():
	cls()
	match input("1. Browse\n2. Search for shops\n3. View tables\n4. Ban user\n5. Delete Post\n6. SQL console\n7. Logout"):

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

def check255(prompt):
	while True:
		inp = input(prompt)
		if len(inp)<=255:
			return inp
		else:
			print("Max char 255\n\n")

def comment(pid):
	cur.execute('INSERT INTO CommentData VALUES(%s, %s, %s, %s)', (increment('CID', 'CommentData'), pid, uname, check255("Enter Caption: ")))
	sql.commit()

###START OF TEST###
productPage("P001")
###END OF TEST###

sql.close()