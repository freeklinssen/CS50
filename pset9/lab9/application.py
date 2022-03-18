import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        if not request.form.get("name") or not request.form.get("month") or not request.form.get("day"):
            return redirect("/")
            
        name = request.form.get("name")
        print( type(name))
        month = request.form.get("month", type = int)
        print( type(month))
        day = request.form.get("day", type = int)
        
        #if not name or not month or not day
        if  ( name[0] > 'z' or name[0] < 'a') and (name[0] < 'A' or name[0] > 'Z') or month > 12 or month < 1 or day > 30 or day < 1:
            return redirect("/")
            
            
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        peoples = db.execute("SELECT * FROM birthdays")
        
        return render_template("index.html", peoples = peoples)


