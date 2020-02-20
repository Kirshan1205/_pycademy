from flask import Flask, render_template, flash, request,url_for, redirect, session
from content_manegement import Content
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from dbconnect import connection
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from functools import wraps
import gc
from flask_mail import Message
from flask_mail import Mail
import uuid

myEmail="kidocodeictschool@gmail.com"

TOPIC_DICT= Content()

app = Flask(__name__)
app.secret_key = 'YOLO'

app.config.update(
    DEBUG = True,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = myEmail,
    MAIL_PASSWORD = "weareprogrammerz"
)
mail = Mail(app)

def send_mail(sender, email, message):
    msg = Message(
        'DONOTREPLY',
        sender = sender,
        recipients=[email]
        )
    msg.body = message
    mail.send(msg)

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/dashboard/')
@app.route('/dashboard/', methods=["POST"])
def dashboard():
    return render_template("dashboard.html", TOPIC_DICT = TOPIC_DICT)
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
    
@app.errorhandler(405)
def method_not_found(e):
    return render_template("405.html")


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))
    return wrap

@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash("You have been logged out")
    gc.collect()
    return redirect(url_for('dashboard'))

@app.route('/login/', methods=['GET','POST'])
def login_page():
    error = ''
    try:
        # session["logged_in"] = True
        c, conn = connection()
        if request.method == "POST":
            
            data = c.execute("SELECT * FROM users WHERE username = (%s)",
                             thwart(request.form['username']))
            data = c.fetchone()
            
            if data[7]=="active":
    
                if sha256_crypt.verify(request.form['password'], data[2]):
                    session["logged_in"] = True
                    session["username"] = request.form['username']
                    
                    flash("You are now logged in")
                    return redirect(url_for("dashboard"))
                else:
                    error = "Invalid credentials, try again."
            else:
                error = "Please Check Your Email To Verify Your Account"
                
        gc.collect()
        return render_template("login.html", error = error)
    except Exception as e:
        error = "Invalid credentials, try again."
        return render_template("login.html", error = error)
        
    return render_template("login.html")
    
    
    # if request.method == 'POST':
    #     return 'i got post'
    # else:
    #     return 'i got get'
    
class RegistrationForm(Form):
    username = TextField("Username", [validators.Length(min=4, max=20)])
    email = TextField("Email Address", [validators.Length(min=6, max=50)])
    password = PasswordField("Password", [validators.Required(),validators.EqualTo('confirm', message="Passwords Must Match")])
    
    confirm = PasswordField("Repeat Password")
    
    accept_tos = BooleanField("I Accept The <a href='/tos'>Terms of Service</a> And The <a href='/privacy/'>Privacy Notice</a> (Last Updated Jan 15 2015)", [validators.Required()])
    
@app.route('/register/', methods=['GET','POST'])
def register_page():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            realUUID = str(uuid.uuid4())[:20]
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            activate = realUUID
            c,conn = connection()
            
            x = c.execute("SELECT * FROM users WHERE (username = (%s) OR email = (%s))",(thwart(username), thwart(email)))
            y = c.fetchall()
            print y
            print '-'*100
            if int(x) > 0:
                flash("That username or email is already taken, please choose another")
                return render_template('register.html', form=form)
            else:
                c.execute("DELETE FROM users WHERE username=(%s)",(thwart(username)))
                c.execute("DELETE FROM users WHERE email=(%s)",(thwart(email)))
                c.execute("INSERT INTO users (username, password, email, activate, tracking) VALUES (%s, %s, %s, %s, %s)",
                (thwart(username), thwart(password), thwart(email), thwart(activate), thwart("/introduction-to-python-programming/")))
                
                conn.commit()
                flash("Thanks for registering please check your email!!!")
                c.close()
                conn.close()
                gc.collect()
                
                # session["username"] = username
                # session["email"] = email
                # session["activate"] = activate
                
                send_mail(myEmail,email,"Please Go To This Link To Verify Your Account:"+"\n"+"flaskblueprint-arshamalishirkouhi.c9users.io/verified/"+ realUUID)
                return redirect('/') #"Please Check Your Email"
        return render_template("register.html", form=form)
    except Exception as e:
        return(str(e))

@app.route("/verified/<uuid>")
def verify(uuid):
    c,conn = connection()
    # request from DB to check uuid in verification column 
    # if found: 1)user=user 2)update user status as active 3)update session
    # if != found: return the activation code is not valid
    c.execute("UPDATE users SET activate='active' WHERE activate='"+uuid+"';")
    conn.commit()
    return redirect(url_for("dashboard"))

@app.route("/forget/", methods=["POST", "GET"])
def forget():
    if request.method == "GET":
        return render_template("forget_password.html")
    elif request.method == "POST":
        realUUID = str(uuid.uuid4())[:20]
        c,conn = connection()
        c.execute("UPDATE users set forget_password=(%s) WHERE email = '"+request.form["Email"]+"';",(thwart(realUUID)))
        conn.commit()
        c.close()
        conn.close()
        flash("Please Go Check Your Email You IDIOT!!!!")
        send_mail(myEmail, request.form['Email'], "Please Go To This Link To Change Your Password:"+"\n"+"flaskblueprint-arshamalishirkouhi.c9users.io/forget_password/"+ realUUID)
        return render_template("forget_password.html")
        
@app.route("/forget_password/", methods=["GET","POST"])
@app.route("/forget_password/<uuid>", methods=["GET","POST"])
def forget_password(uuid=None):
    if request.method=="GET":
        c,conn = connection()
        x = c.execute("SELECT * FROM users WHERE forget_password=%s;",(uuid))
        if x==0:
            return 'Link is not valid'
        else:
            #data=c.fetchone()
            # #c.execute("UPDATE users SET forget_password=%s WHERE forget_password=%s",("NAN",uuid))
            # conn.commit()
            # conn.close()
            return render_template("changePassword.html",uuid=uuid)
    elif request.method=="POST":
        info=request.form
        print str(info),'-'*100
        if info["password"]==info["confirm_password"]:
            c,conn = connection()
            c.execute("UPDATE users SET password=%s, forget_password=%s WHERE forget_password=%s",(sha256_crypt.encrypt(info["password"]),'NaN',info['uuid']))
            conn.commit()
            conn.close()
            flash("your password has been change proceed with login")
            return render_template("changePassword.html",uuid=uuid)
            
        else:
            flash("The password doesn't match")
            return render_template("changePassword.html",uuid=uuid)
            
            
    
    # if x:
    #     password = sha256_crypt.encrypt((str(form.password.data)))
    #     c.execute("UPDATE users SET password=%s WHERE forget_password=%s",(password,uuid))
    #     conn.commit()
    #     c.close()
    #     conn.close()
    #     return render_template("changePassword.html")
    # else:
    #     return "You Can't Fool Me!"
    
if __name__ == '__main__':
    app.run(debug=True , host= '0.0.0.0' , port=8080)