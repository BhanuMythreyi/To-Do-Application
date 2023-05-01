from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask_session import Session
import mysql.connector

obj = Flask(__name__)

try:
    connec = mysql.connector.connect(host="localhost",user="root",password="password",database="todonotes")
    connec.autocommit=True
    cur = connec.cursor(dictionary=True)
    print("Successfully connected")
except:
    print("Unable to connect, please check the connection variables!")

obj.secret_key = "mythreyi"
obj.config["SESSION_PERMANENT"] = False
obj.config["SESSION_TYPE"] = "filesystem"
Session(obj)
@obj.route("/")
def home1():
    return render_template("homepage.html")

@obj.route("/home")
def home():
    return render_template("homepage.html")

@obj.route("/login")
def login():
    return render_template("login.html")

@obj.route("/signup")
def signup():
    return render_template("signup.html")


@obj.route("/sign",methods=["POST","GET"])
def sign():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"]
        emailid = request.form["emailid"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

    else:
        return render_template("signup.html")
    content = request.form
    commandExe = f"INSERT INTO user(firstname,lastname,username,emailid,password1,password2) values('{content['firstname']}','{content['lastname']}','{content['username']}','{content['emailid']}','{content['password1']}','{content['password2']}')"
    cur.execute(commandExe)
    return redirect("/")


@obj.route("/updater1/<notes>")
# changes title based on notes, this route is used when user whishes to change title for a notes
def updater1(notes):
    return render_template("updating1.html",notes=notes)

@obj.route("/updater2/<title>")
# changes notes based on title, this route is used when user whishes to change notes for a title
def updater2(title):
    return render_template("updating2.html",title=title)

@obj.route("/log",methods=["POST","GET"])
def log():
    if request.method=="POST":
        session.pop('username',None)


        username = request.form['username']
        password1 = request.form['password']
        cur.execute('SELECT * FROM user WHERE username=%s AND password1=%s',(username,password1))
        tup = cur.fetchone()
        print(tup)
        if tup:
            session['loggedin'] = True
            session['username'] = tup['username']
            cur.execute("SELECT * FROM notes")
            res = cur.fetchall()
            return render_template("notes.html",res=res,username=session['username'])
        else:
            out = "Wrong credentials"
            return out

        
    else:
        return render_template("homepage.html")

@obj.route("/notes",methods=["GET","POST"])
def notes():
    return render_template("notes.html")


@obj.route("/note",methods=["GET","POST"])
def note():
    if request.method=="POST":
        content1 = request.form
        commandExe1 = f"INSERT INTO notes(title,notes,username) values('{content1['title']}','{content1['notes']}','{session['username']}')"
        try:
            cur.execute(commandExe1)
            
        except:
             return render_template("error_handler.html")
        cur.execute("SELECT * FROM notes")
        res = cur.fetchall()
        return render_template("notes.html",res=res,username=session['username'])
            

@obj.route("/update1/<notes>",methods=["POST","GET"])
# Changing title of a notes
def update1(notes):
    content2 = request.form
    commandExe2 = f"UPDATE notes SET title='{content2['title']}' WHERE notes='{notes}'"
    cur.execute(commandExe2)
    cur.execute("SELECT * FROM notes")
    res = cur.fetchall()
    return render_template("notes.html",res=res,username=session['username'])

@obj.route("/update2/<title>",methods=["POST","GET"])
# changing task/note for a title
def update2(title):
    content2 = request.form
    commandExe2 = f"UPDATE notes SET notes='{content2['notes']}' WHERE title='{title}'"
    cur.execute(commandExe2)
    cur.execute("SELECT * FROM notes")
    res = cur.fetchall()
    return render_template("notes.html",res=res,username=session['username'])

@obj.route("/delete/<tit>",methods=["DELETE","GET"])
def delete(tit):
    if('username' in session):
        commandExe3 = f"DELETE FROM notes WHERE title = '{tit}'"
        try:
            cur.execute(commandExe3)
        except:
            return render_template("error_handler.html")
        cur.execute("SELECT * FROM notes")
        res = cur.fetchall()
        return render_template("notes.html",res=res,username=session['username'])
    else:
        return render_template("login.html")

@obj.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect('/log')
