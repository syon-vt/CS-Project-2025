#imports
from mysql.connector import connect
from pickle import dumps, loads




#initializes the mysql connector
def init():
	global sql
	global cur
	global uname
	sql = connect(host='localhost', user = 'root', password='1234', database='syon_project')
	cur = sql.cursor(buffered=True)
	sql.autocommit = True
init()


# ---------------------------------------------------------------------------- #
#                                 SQL FUNCTIONS                                #
# ---------------------------------------------------------------------------- #

#returns required column as list
def getCol(col, table):
	cur.execute(f'SELECT {col} from {table}')
	l = []
	for row in cur.fetchall():
		l.append(row[0])
	return l

# ---------------------------------------------------------------------------- #

#returns required row as list
def getRow(table, cond, val):
	cur.execute(f'SELECT * FROM {table} WHERE {cond}="{val}";')
	return list(cur.fetchall())

# ---------------------------------------------------------------------------- #

#returns single value
def getOne(col, table, cond, val):
	cur.execute(f'SELECT {col} from {table} where {cond}="{val}"')
	return cur.fetchone()[0]

# ---------------------------------------------------------------------------- #

#returns column heads as list
def clmnheads(table):
	cur.execute(f"SELECT * FROM {table} where uname='1'")
	return [i[0] for i in cur.description]

# ---------------------------------------------------------------------------- #

#returns all items
def all():
	cur.execute("SELECT * from ProductData;")
	return cur.fetchall()

# ---------------------------------------------------------------------------- #

#autoincrement for primary keys
def increment(col, table):
	cur.execute(f'SELECT {col} from {table};')
	try:
		last = (cur.fetchall()[-1][0])
		return str(last)[0]+f"{int((str(last)[1:]))+1 :03d}"
	except:
		return col[0].upper()+'001'
	
# ---------------------------------------------------------------------------- #
#                             End of SQL FUNCTIONS                             #
# ---------------------------------------------------------------------------- #



# ---------------------------------------------------------------------------- #
#                                Findr FUNCTIONS                               #
# ---------------------------------------------------------------------------- #

#adds comment
def addComment(pid, uname, caption):
	cur.execute('INSERT INTO CommentData VALUES(%s, %s, %s, %s)', (increment('cid', 'commentdata'), pid, uname, caption))

# ---------------------------------------------------------------------------- #

#uploads posts
def upload(uname, cap, price, img):
	cur.execute("INSERT INTO ProductData VALUES(%s, %s, %s, %s, %s)", (increment('pid', 'productdata'), uname, cap, img, price))
	cur.execute("UPDATE UserData SET POSTCOUNT = POSTCOUNT+1 WHERE uname=%s", (uname,))

# ---------------------------------------------------------------------------- #

#edits userdata
def edit(uname, newdata):
	sql.autocommit = False
	try:
		cur.execute('delete from userdata where uname=%s', (uname,))
		cur.execute('insert into userdata values(%s, %s, %s, %s, %s, %s, %s)', newdata)
	except Exception as e:
		sql.rollback()

	sql.commit()
	sql.autocommit = True	

# ---------------------------------------------------------------------------- #

#returns postcount
def postcount(uname):
	c=0
	for product in all():
		if product[1].lower() == uname.lower():
			c+=1
	return c

# ---------------------------------------------------------------------------- #

#creates user
def signup(name, uname, decrip, email, pwd):
	cur.execute("INSERT INTO UserData VALUES(%s, %s, %s, %s, %s, %s, %s)", (name, uname, decrip, email, pwd, 0, dumps([])))
	
# ------------------------------ LIKE FUNCTIONS ------------------------------ #

#checks if liked	
def checklike(uname, pid):
	if pid in getCol('pid', 'LikeData') and getRow('LikeData', 'pid', pid)[0][1] == uname:
		return True
	return False

# ---------------------------------------------------------------------------- #

#adds Like
def addlike(uname, pid):
	cur.execute("SELECT * FROM LikeData WHERE PID=%s AND UNAME=%s", (pid, uname))
	if not cur.fetchall():
		cur.execute("INSERT INTO LikeData VALUES(%s, %s)", (pid, uname))

# ---------------------------------------------------------------------------- #

#removes like
def remlike(uname, pid):
	cur.execute("DELETE FROM LikeData WHERE PID=%s AND UNAME=%s", (pid, uname))
	
# ---------------------------------------------------------------------------- #

#returns like count
def likecount(pid):
	cur.execute('SELECT * FROM LikeData WHERE PID=%s', (pid,))
	return len(cur.fetchall())
# ------------------------------------- . ------------------------------------ #


# ------------------------------ CART FUNCTIONS ------------------------------ #

#returns deserialized cart
def getcart(uname):
	return loads(getOne('CART', 'UserData', 'uname', uname))

# ---------------------------------------------------------------------------- #

#updates serialized cart after addition of product
def addtocart(uname, pid):
	cart = getcart(uname)
	cart.append(pid)
	cur.execute("UPDATE UserData SET CART=%s WHERE UNAME=%s", (dumps(cart), uname))
	
# ---------------------------------------------------------------------------- #

#updates serialized cart after removal of product
def remfromcart(uname, pid):
	cart = getcart(uname)
	cart.remove(pid)
	cur.execute("UPDATE UserData SET CART=%s WHERE UNAME=%s", (dumps(cart), uname))

# ---------------------------------------------------------------------------- #

#clears cart
def clearcart(uname):
	cur.execute("UPDATE UserData SET CART = %s WHERE UNAME = %s", (dumps([]), uname))
	
# ------------------------------------- . ------------------------------------ #


# ----------------------------- REQUEST FUNCTIONS ---------------------------- #

#sends requests
def sendrequests(pidlist, uname):
	for pid in pidlist:
		cur.execute("INSERT INTO RequestData VALUES(%s, %s, %s, %s, %s)", (increment('RID', "RequestData"), getOne('uname','productdata', 'pid', pid), uname, pid, 'Pending'))

# ---------------------------------------------------------------------------- #

#gets all current requests
def getrequests(shop):
	cur.execute("SELECT * FROM RequestData WHERE SELLER=%s", (shop,))
	return list(cur.fetchall())

# ---------------------------------------------------------------------------- #

#sets request status/deletes requests
def setstatus(rid, status):
	if status == "Delete":
		cur.execute("DELETE FROM RequestData WHERE RID=%s", (rid,))
	else:
		cur.execute("UPDATE RequestData SET STATUS=%s WHERE RID=%s", (status, rid))
# ------------------------------------- . ------------------------------------ #

# ---------------------------------------------------------------------------- #
#                                       .                                      #
# ---------------------------------------------------------------------------- #