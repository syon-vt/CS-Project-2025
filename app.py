# ---------------------------------------------------------------------------- #
#                                Findr: The app                                #
# ---------------------------------------------------------------------------- #
from flask import Flask, render_template, abort, request, redirect, url_for, session, flash # web app functionality
from base64 import b64encode # load images from db
from logging import error # error msgs in console
import functions as sql # custom functions from function.py
from pickle import dumps # serializes cart for storage
from hashlib import sha256  # standard sha256 hashing for password


# ------------------------ initialize flask and mysal ------------------------ #
sql.init()
app = Flask(__name__, template_folder='blocktemplates', static_folder='static')
app.secret_key = "key"


# --------------------------- logout and init page --------------------------- #
@app.route("/", methods=['POST', 'GET'])
def init():
    session.clear()
    session['loggedin'] = False
    session['uname'] = 'Guest'
    return redirect(url_for('home'))


# -------------------------------- signin pgae ------------------------------- #
@app.route("/signin", methods=['GET', 'POST'])
def signin():

    if session.get('loggedin'):
        return redirect(url_for('home'))
    
    else:
        if request.method == 'POST':
            data = request.form
            session['email'] = data.get('email') # stores email in app wide session dict

            # check if account exists
            if not session.get('email') in sql.getCol('email', 'userdata'):
                flash('There is no account linked with that email', 'error')
                return redirect(url_for('signup'))
            
            else:
                # checks hashed pwd with stored hashed pwd
                if sha256(data.get('password').encode()).hexdigest() == sql.getOne('pwd', 'userdata', 'email', data['email']):   
                    session['loggedin'] = True
                    session['uname'] = sql.getOne('uname', 'userdata', 'email', session.get('email'))
                    return redirect(url_for('home'))
                else:
                    flash("Incorrect Password! Try Again", 'error')

    return render_template('signin.html',
                            loggedin=session.get("loggedin"))


# -------------------------------- signup page ------------------------------- #
@app.route("/signup", methods=['GET', 'POST'])
def signup():

    if session.get('loggedin'):
        return redirect(url_for('home'))
    
    else:
        if request.method == 'POST':
            
            data = request.form
            session['uname'] = data.get('uname')
            session['email'] = data.get('email')

            # check for dupe email
            if session.get('email') in sql.getCol('email', 'userdata'):
                flash("There is already an account linked to that email", 'error')
                return redirect(url_for('signin'))

            # check for dupe username
            elif session.get('uname') in sql.getCol('uname', 'userdata'):
                    flash("Username already taken", 'error')
            
            else:
                # hash and save pwd and account
                try:
                    password = sha256(data.get('password').encode()).hexdigest()
                    sql.signup(data.get('name'), session.get('uname'), data.get('desc'), data.get('email'), password)
                    session['loggedin'] = True
                    return redirect(url_for('home'))
                
                except Exception as e:
                    error(e)

        return render_template('signup.html',
                                loggedin=session.get("loggedin"), 
                                email = session.get('email'))
    

# --------------------------------- home page -------------------------------- #
@app.route("/home", methods=['GET'])
def home():

        return render_template('home.html',
                                loggedin=session.get("loggedin"), 
                                name=sql.getOne('name','userdata', 'uname', session.get('uname')), 
                                products=sql.all(), 
                                b64encode=b64encode,
                                seller=lambda uname: sql.getOne('name', 'userdata', 'uname', uname), 
                                postno=sql.postcount(session.get('uname')),
                                uname=session.get('uname'))


# ------------------------------- product page ------------------------------- #
@app.route("/<pid>", methods=['GET', 'POST'])
def productpage(pid):

        
    isliked = sql.checklike(session.get('uname'), pid)

    if pid in sql.getcart(session.get('uname')):
        incart = True
    else:
        incart = False

    if pid not in sql.getCol('pid' ,'productdata'):
        abort(404)
    data = sql.getRow('productdata', 'pid', pid)[0]

    if request.method == 'POST':
        if not session.get('loggedin'):
            flash("You need to be Logged in to perform this action", 'error')
            return redirect(url_for("signin"))

        if request.form.get('comment'):
            sql.addComment(pid, session.get('uname'), request.form.get('comment'))

        elif request.form.get('isliked'):
            if request.form.get('isliked') == "True":
                sql.addlike(session.get('uname'), pid)
                isliked = True

            elif request.form.get('isliked') == "False":
                isliked = False
                sql.remlike(session.get('uname'), pid)
        
        elif request.form.get('incart'):
            if request.form.get('incart') == 'True':
                sql.addtocart(session.get('uname'), pid)
                return redirect(url_for("cart"))
            
            elif request.form.get('incart') == 'False':
                sql.remfromcart(session.get('uname'), pid)
                return redirect(url_for('productpage',pid=pid))
            
        else:
            error("not getting in loop")
        
    try:
        return render_template('productpage.html',
                                loggedin=session.get("loggedin"), 
                                img=b64encode(data[3]).decode('utf-8'), 
                                title=data[2], 
                                seller=sql.getOne('name', 'userdata', 'uname', data[1]).title(), 
                                price=data[4], 
                                comments=sql.getRow('commentdata', 'pid', pid), 
                                pid=pid, 
                                liked=isliked,
                                likecount = sql.likecount(pid),
                                incart=incart)
    except TypeError:
        abort(404)


@app.route("/upload", methods=['GET', 'POST'])
def upload():

    if session.get('loggedin'):
        if request.method == 'POST':
            data = request.form
            img = request.files['img'].read()
            
            try:
                sql.upload(session.get('uname'), data.get('caption'), data.get('price')  ,img)
                flash('Uploaded Succesfully', 'success')

            except Exception as e:
                flash('Upload Failed', 'error')
        return render_template('upload.html',
                                loggedin=session.get("loggedin"))
    
    else:
        flash("You need to be Logged in to perform this action", 'error')
        return redirect(url_for('signin'))

#everything is fucked? i hope...?
@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if session.get('loggedin'):

        data = sql.getRow('userdata', 'uname', session.get('uname'))[0][0:5]
        headers = sql.clmnheads('userdata')[0:5]
        if request.method == 'POST':
            try:
                data = [
                    request.form.get('NAME'),
                    session.get('uname'),
                    request.form.get('DECRIP'),
                    request.form.get('EMAIL'),
                    sha256(request.form.get('PWD').encode()).hexdigest(),
                    0,
                    dumps([])]
            

                if data[4]=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855":
                    data[4] = sql.getOne('pwd', 'userdata', 'uname', session.get('uname '))

                sql.edit(session.get('uname'), data)

                flash("Profile edited successfully", 'success')
            except Exception as e:
                error(e)
                flash(f"Process Failed {e}", 'error')
        return render_template('edit.html',
                                loggedin=session.get("loggedin"),
                                dictionary=dict(zip(headers, data)),
                                name=sql.getOne('name','userdata', 'uname', session.get('uname')))
        
    else:
        flash("You need to be Logged in to perform this action", 'error')
        return redirect(url_for('signin'))

@app.route("/cart", methods=['GET', 'POST'])
def cart():
    if session.get('loggedin'):
        
        cart = []
        total = 0

        for product in sql.getcart(session.get('uname')):
            cart.append(sql.getRow('productdata', 'pid', product)[0])
   
        for item in cart:
            total+=item[4]

        if request.method == 'POST':
            if request.form.get('buy'):
                sql.sendrequests(sql.getcart(session.get('uname')), session.get('uname'))
                sql.clearcart(session.get('uname'))
                cart = []

            elif request.form.get('delete'):
                sql.remfromcart(session.get('uname'), request.form.get('delete'))
                
                for item in cart:
                    if item[0] == request.form.get('delete'):
                        cart.remove(item)


        return render_template('cart.html',
                                loggedin=session.get("loggedin"),
                                details=cart, 
                                b64encode=b64encode,
                                name=sql.getOne('name','userdata', 'uname', session.get('uname')),
                                total=total)
    else:
        flash("You need to be Logged in to perform this action", 'error')
        return redirect(url_for('signin'))
    

@app.route("/requests", methods=['GET', 'POST'])
def requests():
    if session.get('loggedin'):

        all = sql.getrequests(session.get('uname'))
        requests = []
        for req in all:
            requests.append([req[::2]]+sql.getRow('productdata', 'pid', req[3]))

        if request.method == 'POST':
            if request.form.get('status'):
                status = request.form.get('status').split(',')
                sql.setstatus(status[1], status[0])
            error(request.form)
            error(request.form)
            

        return render_template('requests.html', 
                                loggedin=session.get("loggedin"),
                                requests=requests,
                                b64encode=b64encode)
                               
    else:
        flash("You need to be Logged in to perform this action", 'error')
        return redirect(url_for('signin'))
    

@app.errorhandler(404)
def not_found(e):
    return f"Page Not Found\n{e}", 404


if __name__ == '__main__':
    app.run(debug=True)
