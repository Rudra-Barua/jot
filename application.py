import os
# Used Finance50 and Week 8 PSET as the base
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from urllib.request import urlopen
from bs4 import BeautifulSoup

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///jot.db")


@app.route("/")
@login_required
def index():
    # Go through the db and find all the undeleted notes and their respective websites
    websitedata = db.execute(
        "SELECT website, note FROM history WHERE user_id=:user_id AND deleted = 0", user_id=session["user_id"])

    # Create an empty dictionary for the notebooks
    notebooks = {}

    # Go through the note/website data and append all the unique sites and their titles to the dict
    for i in range(len(websitedata)):
        if websitedata[i]["website"] not in notebooks:
            # Beautiful soup is taking the url of a site and finding its title
            url = websitedata[i]["website"]
            soup = BeautifulSoup(urlopen(url))
            title = soup.title.get_text()
            notebooks[websitedata[i]["website"]] = [websitedata[i]["website"], title, i]

    # Go through each site key and add its correspoinding notes as key value pair
    for notebook in notebooks:
        for log in websitedata:
            if notebook == log["website"]:
                notebooks[log["website"]].append(log["note"])

    # Lets send this over to the index html to display our notes
    return render_template("index.html", notebooks=notebooks)


@app.route("/write", methods=["GET", "POST"])
@login_required
def write():
    if request.method == "POST":
        # Check that the user is typing in notes
        if not request.form.get("note"):
            flash("Missing Note!")
            return redirect("/write")

        # Check that the user has a website
        if not request.form.get("url"):
            flash("Missing Website!")
            return redirect("/write")

        # Get the form data from the user
        note = request.form.get("note")
        website = request.form.get("url")

        # Go into the records for all the notes and add in the notes just entered
        db.execute("INSERT INTO history (user_id,note,website) VALUES(?,?,?)",
                   session["user_id"], note, website)

        flash("Noted!")

        return redirect("/write")
    else:
        # To make it convenient the previous searched website will open up on start
        recent = db.execute(
            "SELECT website FROM history WHERE user_id=:user_id ORDER BY datetime DESC LIMIT 1;", user_id=session["user_id"])

        # For first time users, it starts them off on a webpage
        try:
            iframe = recent[0]["website"]
        except:
            iframe = "https://en.wikipedia.org/wiki/Main_Page"


        return render_template("write.html", iframe=iframe)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/todos", methods=["GET", "POST"])
@login_required
def todos():
    if request.method == "POST":
        # Check that a task was input
        if not request.form.get("task"):
            flash("Missing Task!")
            return redirect("/todos")

        # Check that a website was input
        if not request.form.get("url"):
            flash("Missing Website!")
            return redirect("/todos")

        # Check that a date/time was input
        if not request.form.get("timedate"):
            flash("Missing Date/Time!")
            return redirect("/todos")

        # Grab all the user input
        task = request.form.get("task")
        url = request.form.get("url")
        timedate = request.form.get("timedate")

        # The time date given by HTML forms puts in an extra T that the SQL DB does not use
        timedate = timedate.replace('T', ' ')

        # Go into the records for all the todos and add in the information associate with the todo
        db.execute("INSERT INTO todos (user_id,task,website,timedate) VALUES(?,?,?,?)",
                    session["user_id"], task, url, timedate)

        flash("Added!")

        return redirect("/todos")
    else:
        # Get all the undeleted tasks and put all the information regarding each task into a dict
        tododata = db.execute("SELECT website, task, timedate, completed, todo_id FROM todos WHERE user_id=:user_id AND deleted = 0",
                                  user_id=session["user_id"])

        todos = {}

        # Go through each of the tasks and make a dict with the keys being the unique sites
        for i in range(len(tododata)):
            if tododata[i]["website"] not in todos:
                todos[tododata[i]["website"]] = [tododata[i]["website"], i]

        # Go through each of the tasks and start sorting them into the sites they are associated with
        for todo in todos:
            for sitetodo in tododata:
                if todo == sitetodo["website"]:
                    temp = [sitetodo["task"], sitetodo["timedate"], sitetodo["completed"], sitetodo["todo_id"]]
                    todos[sitetodo["website"]].append(temp)

        # To make it more convenient, the site of the previous task will be autofilled
        recent = db.execute("SELECT website FROM todos WHERE user_id=:user_id ORDER BY todo_id DESC LIMIT 1;",
                            user_id=session["user_id"])
        try:
            recent = recent[0]["website"]
        except:
            recent = ""

        return render_template("todos.html", todos=todos, recent=recent)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure passwords match
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords do not match", 400)

        # Insert the password's hash and username into the table
        try:
            user = db.execute("INSERT INTO users (username, hash) VALUES(?,?)", request.form.get(
                "username"), generate_password_hash(request.form.get("password")))
        except:
            return apology("username already taken", 400)

        # Remember which user has logged in
        session["user_id"] = user

        flash("Successful Registration!")

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/delete", methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        # Get the url of the notebook/site being deleted
        website = request.form['note']

        # Set the deleted condition for that site to true
        db.execute("UPDATE history SET deleted = 1 WHERE user_id=:user_id AND website=:website;",
                    user_id=session["user_id"], website=website)

        flash("Notebook Deleted!")

        return redirect("/")
    else:
        return redirect("/")


@app.route("/deletetodo", methods = ['GET', 'POST'])
def deletetodo():
    if request.method == 'POST':
        # Find the todo_id of the todo being deleted
        todo_id = request.form['task']

        # Use the todo_id and use_id to find the todo and set its deleted condition to true
        db.execute("UPDATE todos SET deleted = 1 WHERE user_id=:user_id AND todo_id=:todo_id;",
                    user_id=session["user_id"], todo_id=todo_id)

        flash("Task Completed!")

        return redirect("/todos")
    else:
        # For convenience, the most recent task's website is autofilled in the url bar
        recent = db.execute("SELECT website FROM todos WHERE user_id=:user_id ORDER BY todo_id DESC LIMIT 1;",
                            user_id=session["user_id"])
        try:
            recent = recent[0]["website"]
        except:
            recent = ""

        print(recent)

        return render_template("/todos", recent=recent)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
