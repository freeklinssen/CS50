import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    
    cash_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]['cash']
    cash_balance = round(cash_balance, 2)
    symboles = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", user_id)
    
    tickers = []
    
    for symbol in symboles:
        tickers.append(symbol["symbol"])
        print(tickers)
    
    quantities = []
    
    purchaches = db.execute("SELECT symbol, quantity, price FROM transactions WHERE user_id = ?", user_id)
    
    for purchase in purchaches:
        for i in range(len(tickers)):
            if purchase["symbol"] == tickers[i]:
                if len(quantities)-1 >= i:
                    quantities[i] = quantities[i] + purchase["quantity"]
                else:
                    quantities.append(purchase["quantity"])

    print(quantities)
        
    current_prices = []
    for i in range(len(tickers)):
        
        answer = lookup(tickers[i])
        temp = round(answer["price"], 2)
        current_prices.append(temp)
    print(current_prices)
    
    current_value = []
    for i in range(len(tickers)):
        current_value.append(quantities[i] * current_prices[i])
    print(current_value)
    
    total_balance = cash_balance
    for i in range(len(tickers)):
        total_balance = total_balance + current_value[i]
    
    # determine average buying price

    print(purchaches)
    
    avg_buy_price = []
    number_shares = []
    for purchase in purchaches:
        for i in range(len(tickers)):
            if purchase["symbol"] == tickers[i]:
                if purchase["quantity"] > 0:
                    if len(avg_buy_price)-1 >= i:
                        avg_buy_price[i] = (number_shares[i] * avg_buy_price[i] + purchase["quantity"] * 
                                            purchase["price"]) / (number_shares[i] + purchase["quantity"])
                        number_shares[i] = number_shares[i] + purchase["quantity"]
                    else:
                        avg_buy_price.append((purchase["quantity"] * purchase["price"]) / purchase["quantity"])
                        number_shares.append(purchase["quantity"])
                else:
                    number_shares[i] = number_shares[i] + purchase["quantity"]
                    
            else:
                continue
            
    buy_value = []
    for i in range(len(tickers)):
        buy_value.append(avg_buy_price[i] * number_shares[i])  
        
    gain_loss = []
    gain_loss_percentage = []
    for i in range(len(tickers)):
        gain_loss_percentage.append(((current_prices[i]-avg_buy_price[i])/avg_buy_price[i]))
        gain_loss.append(current_value[i] - buy_value[i])
    
    for i in range(len(tickers)):
        avg_buy_price[i] = round(avg_buy_price[i], 2)
        buy_value[i] = round(buy_value[i], 2)
        gain_loss[i] = round(gain_loss[i], 2)
        gain_loss_percentage[i] = round(gain_loss_percentage[i], 4)
        gain_loss_percentage[i] = "{:.2%}".format(gain_loss_percentage[i])
        if quantities[i] == 0:
            gain_loss_percentage[i] = 0
            
    print(buy_value)
    print(avg_buy_price)
    print(number_shares)
    
    # for purchache in all_purchaches
    
    lenght = len(tickers)
    # for purchaches in purchaches:
        
    # for ticker in tickers:
        
    return render_template("home.html", cash_balance=cash_balance, total_balance=total_balance, lenght=lenght, tickers=tickers, quantities=quantities,
                           current_prices=current_prices, current_value=current_value, avg_buy_price=avg_buy_price, buy_value=buy_value, 
                           number_shares=number_shares, gain_loss=gain_loss, gain_loss_percentage=gain_loss_percentage)
              

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Must provide symbol", 400)

        if not request.form.get("shares"):
            return apology("Must provide a number of stocks", 400)

        ticker = request.form.get("symbol").upper()
        
        quantity = (request.form.get("shares"))

        try:
            quantity = int(quantity)
        except:
            return apology("Must porvide a positive integer", 400)

        if quantity <= 0:
            return apology("Must provide a positive integer", 400)

        answer = lookup(ticker)

        if answer == None:
            return apology("Must provide a valid symbol", 400)

        name = answer["name"]
        price = answer["price"]
        total_price = price * quantity

        user_id = session["user_id"]

        print(user_id)

        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        if total_price > cash:
            return apology("Not enough cash :(", 400)
        else:
            new_cash = cash - total_price
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)
            db.execute("INSERT INTO transactions (user_id, name, price, quantity, type, symbol) VALUES(?, ?, ?, ?, ?, ?)", 
                       user_id, name, price, quantity, "Buy", ticker)

        return redirect('/')

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]
    history = db.execute("select * FROM transactions WHERE user_id = ?", user_id)

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

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
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must provide a valid symbol", 400)

        symbol = request.form.get("symbol")

        answer = lookup(symbol)

        if answer == None:
            return apology("must provide a valid symbol", 400)

        return render_template("quoted.html", answer=answer)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
            
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("must provide two identical passwords", 400)
            
        username = request.form.get("username")
        
        usernames = db.execute("SELECT username FROM users")
        
        for i in range(len(usernames)):
            if usernames[i]['username'] == username:
                return apology("username already in use", 400)

        hash1 = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash1)

        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Must provide symbol", 400)

        if not request.form.get("shares"):
            return apology("Must provide a number of stocks", 400)

        ticker = request.form.get("symbol").upper()
        quantity = request.form.get("shares")

        try:
            quantity = int(quantity)
        except:
            return apology("Must porvide a positive integer", 400)

        if quantity <= 0:
            return apology("Must provide a positive integer", 400)

        answer = lookup(ticker)

        if answer == None:
            return apology("Must provide a valid symbol", 400)

        name = answer["name"]
        price = answer["price"]
        total_price = price * quantity
        neg_quantity = 0 - quantity

        user_id = session["user_id"]

        try:     
            purchaches = db.execute("SELECT symbol, quantity, price FROM transactions WHERE user_id = ?", user_id)
    
        except:
            return apology("You don't own this stock ;)", 400)
            
        in_posses = 0
        
        for purchase in purchaches:
            if purchase["symbol"] == ticker:
                in_posses = in_posses + purchase["quantity"]
        
        if quantity > in_posses:
            return apology("You tried to sell more shares than you have ;)", 400)

        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        new_cash = cash + total_price
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)

        db.execute("INSERT INTO transactions (user_id, name, price, quantity, type, symbol) VALUES(?, ?, ?, ?, ?, ?)", 
                   user_id, name, price, neg_quantity, "Sell", ticker)

        return redirect('/')

    else:
        user_id = session["user_id"]
        symboles = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", user_id)

        return render_template("sell.html", symboles=symboles)
        
        
@app.route("/deregister", methods=["GET", "POST"])
@login_required
def deregester():
    if request.method == "POST":
        
        user_id = session["user_id"]
        
        db.execute("DELETE FROM transactions WHERE user_id = ?", user_id)
        db.execute("DELETE FROM users WHERE id = ?", user_id)
        
        return render_template("login.html")
        
    else:
        return render_template("deregister.html")
        
    
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
