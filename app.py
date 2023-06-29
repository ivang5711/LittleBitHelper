# This file called app.py contains a code for the Web App for
# the LittleBitHelper project
# To run the file type ./../flask run in your terminal

from datetime import date
from datetime import datetime
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, currency, rates, base_check, keys
import sqlite3
import random
from datetime import timedelta
from termcolor import cprint
from werkzeug.exceptions import HTTPException


# Configure application
app = Flask(__name__)
# Custom filter
app.jinja_env.filters["currency"] = currency
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1440)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///expenses.db")


# Get the default currrency value for the current user
cur = ""
global cur_index
cur_index = ['default', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS',
             'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF',
             'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BWP', 'BYN',
             'BZD', 'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNH', 'CNY', 'COP',
             'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD',
             'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP',
             'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK',
             'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK',
             'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW',
             'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL',
             'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU',
             'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO',
             'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR',
             'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD',
             'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'SSP',
             'STD', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND',
             'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU',
             'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XCD',
             'XDR', 'XOF', 'XPD', 'XPF', 'XPT', 'YER', 'ZAR', 'ZMW', 'ZWL']
cprint(f"@app.py: {base_check()}", "cyan")


# Prevents the browsers from cashing the content of the Web pages
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    return response


# Provides a user's summary
@app.route("/")
@login_required
def index():
    # Gets the current session's user ID
    uid = int(session['tg_id'])
    # Reads the info from the database
    usersbase = db.execute('''SELECT default_currency
                           FROM users
                           WHERE tg_id = ?;''', uid,)
    total = 0
    global cur
    cur = (usersbase[0])["default_currency"]
    cprint(f"Default currency is: {cur}", "cyan")
    cprint(f"@index(): {base_check()}", "cyan")
    # Gets all the user's records from the expenses table
    usersbase = db.execute('''SELECT *
                           FROM expenses
                           WHERE users_id = ?;''', uid)
    cprint("@index(): look here", "cyan")
    cprint(f"@index() session user ID: {uid}", "cyan")
    cprint(f"@index() users in database: {len(usersbase)}", "cyan")
    # Gets the amount of the user's records in the database
    iterations = len(usersbase)
    # Checks if the amount of records is not zero
    if not (len(usersbase) == 0):
        cprint(f"@index(): {(usersbase[0])['users_id']}", "cyan")
        cprint("@index() here we go", "cyan")
        # Gets the user's records grouped by type and currency with
        # the amouts summed up correspondingly
        usersbase = db.execute('''SELECT id, type, SUM(amount), comment,
                               date, time, users_id, currency
                               FROM expenses
                               WHERE users_id = ?
                               GROUP BY type, currency
                               ORDER BY SUM(amount) DESC;''', uid)
        # Gets the amount of the grouped records
        iterations = len(usersbase)
        cprint("@index() end of look here", "cyan")
        # Declare the lists for the variable storage
        nid = []
        tgid = []
        type = []
        amount = []
        comment = []
        date = []
        time = []
        curren = []
        # Populates the lists with values from the selection from the database
        for i in range(iterations):
            nid.append((usersbase[i])["id"])
            tgid.append((usersbase[i])["users_id"])
            type.append((usersbase[i])["type"])
            comment.append((usersbase[i])["comment"])
            date.append((usersbase[i])["date"])
            time.append((usersbase[i])["time"])
            # Checks if the currency is the same as the current
            # default currency for the user
            if (usersbase[i])["currency"] == cur:
                total += (usersbase[i])["SUM(amount)"]
                amount.append((usersbase[i])["SUM(amount)"])
            # If the currency is differ from the user's
            # current default currency
            else:
                temporary = ((usersbase[i])["SUM(amount)"] /
                             rates((usersbase[i])["currency"]) * rates(cur))
                total = total + int(temporary)
                amount.append(temporary)
        strUid = str(uid)
        # Create new temporary table to store the new records
        db.execute('''CREATE TABLE IF NOT EXISTS ?
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   type TEXT NOT NULL,
                   amount INT NOT NULL,
                   users_id INTEGER NOT NULL);''', strUid)
        cprint("@index(): Table is ready", "cyan")
        # Populates the table with the updated values
        for i in range(iterations):
            db.execute('''INSERT INTO ? (type, amount, users_id)
                       VALUES (?, ?, ?);''', strUid, type[i],
                       amount[i], int(strUid))
        # Selects the records from the table grouped by type with
        # the smmount summed up correspondingly
        curso = db.execute('''SELECT type, SUM(amount)
                           FROM ?
                           GROUP BY type
                           ORDER BY SUM(amount) DESC;''', strUid)
        cprint(f"curso: {len(curso)}", "cyan")
        # populate the lists with the values from the selection
        type = []
        amount = []
        for i in range(len(curso)):
            cprint(f"@index(): {curso[i]}", "cyan")
            type.append((curso[i])["type"])
            amount.append((curso[i])["SUM(amount)"])
        cprint(f"lengths: {iterations}", "cyan")
        cprint(f"@index(): {len(curso)}", "cyan")
        iterations = len(curso)
        # Deletes the temporary table
        db.execute("DROP TABLE ?;", strUid)
        cprint("@index(): Table deleted", "cyan")
        # Runs the random color generator to provide unique
        # colors for the chart and table
        hexColorList = []
        for j in curso:
            color_index = ""
            for i in range(0, 6):
                # Generates a random integer in the given
                # range and converts it to hex, then slices the output
                tmp = (hex(random.randint(8, 13)))[2:]
                color_index += tmp
            hexColor = "#" + color_index
            hexColorList.append(hexColor)
        # Renders the index page
        return render_template("index.html", nid=nid, tgid=tgid, type=type,
                               amount=amount, comment=comment, date=date,
                               time=time, iterations=iterations,
                               hexColorList=hexColorList,
                               total=total, cur=cur, curren=curren)
    else:
        # Renders the index page
        return render_template("index.html",
                               iterations=iterations,
                               cur=cur, total=total)


# Provides a page for user to add new record to the database
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # Checks if the user gets to the page via POST method
    cprint(f"@add(): {base_check()}", "cyan")
    if request.method == "POST":
        # Checks if the symbol is provided
        if not request.form["symbol"]:
            return apology("must provide symbol", 400)
        # Checks if the input shares are digits
        userInput = request.form["shares"]
        if not userInput.isdigit():
            return apology("not a digit", 400)
        # Checks if the shares amount is provided and correct
        if ((not request.form["shares"]) or
            (float(request.form["shares"]) < 1) or
                ((float(request.form["shares"]) % 1) != 0)):
            return apology('''must provide a correct
                           number of shares to buy''', 400)
        # Stores the input into a variable
        type_ = request.form["symbol"]
        amount_ = request.form["shares"]
        comment_ = request.form["comment"]
        curr_ = request.form["currency"]
        dat = date.today().isoformat()
        dtn = datetime.now()
        tim = dtn.strftime("%H:%M:%S")
        # Gets current session's user ID
        uid = int(session['tg_id'])
        # Connects to the database
        conn = sqlite3.connect('expenses.db')
        cprint("@add: Opened database successfully", "cyan")
        # Checks if the provided currency value equals to "default"
        if curr_ == 'default':
            usersbase = db.execute('''SELECT default_currency
                                   FROM users
                                   WHERE tg_id = (?);''', uid)
            # Assignes the default currency value of the
            # current user to the variable
            current = (usersbase[0])['default_currency']
        else:
            # Otherwise assignes the new currency value to the variable
            current = curr_
        cprint(f"@add: {current}", "cyan")
        # Adds the new record with the new values to the expenses table
        conn.execute('''INSERT INTO expenses (type, amount,
                     comment, date, time, users_id, currency)
                     VALUES (?, ?, ?,
                     ?, ?, ?, ?);''', (type_, amount_,
                                       comment_, dat, tim,
                                       uid, current))
        conn.commit()
        conn.close()
        cprint("@add: Records created successfully", "cyan")
        # Redirects the user to the History page
        return redirect("/history")
    # Renders the Add page
    global cur_index
    currency_index = cur_index
    leng = len(cur_index)
    return render_template("add.html",
                           currency_index=currency_index,
                           leng=leng)


# Provides a page with all the user's history
@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    # Show history grouped by type
    cprint(f"@hystory(): {base_check()}", "cyan")
    # Gets the current session's user ID
    uid = int(session['tg_id'])
    listOfKeys = keys()
    # Sets the edit mode variable to 0
    edit_mode = 0
    # Checks if the user gets to the page via POST method
    if request.method == "POST":
        print("@history(): hey POST")
        # Tries to define which input was submitted to get to this page
        try:
            request.form["delete"]
            mode = "delete"
        except HTTPException:
            print("@history(): mode: NOT delete")
        try:
            request.form["edit"]
            mode = "edit"
        except HTTPException:
            print("@history(): mode: NOT edit")
        try:
            request.form["new_type"]
            mode = "update"
        except HTTPException:
            print("@history(): mode: NOT update")
        print("@history: try result = ", mode)
        # Checks if the input is valid and defines the form submitted
        if mode == "delete":
            toDelete = request.form["delete"]
            print("@history(): FROM delete", toDelete)
            # Checks if the input shares are digits
            if not toDelete.isdigit():
                return apology("not a digit", 400)
            # Checks if the shares amount is provided and correct
            if ((not request.form["delete"]) or
                (float(request.form["delete"]) < 1) or
                    ((float(request.form["delete"]) % 1) != 0)):
                return apology("must provide a correct number "
                               "of shares to buy", 400)
            # Stores the input into a variable
            cprint(f"@history: {toDelete}", "cyan")
            # Prints out the record with the given ID to the terminal
            usersbase = db.execute('''SELECT id, type, amount,
                                comment, date, time, users_id
                                FROM expenses WHERE id = (?);''', (toDelete,))
            cprint(f"@history: {usersbase[0]}", "cyan")
            # Deletes a record from the expenses table
            usersbase = db.execute('''DELETE FROM expenses
                                WHERE id = (?);''', (toDelete,))
        if mode == "edit":
            edit_mode = 0
            toEdit = request.form["edit"]
            print(f"@history(): FROM edit {toEdit}")
            cprint(f"@history: {toEdit}", "cyan")
            # Prints the selected record to the terminal
            usersbase = db.execute('''SELECT id, type, amount,
                                comment, date, time, users_id, currency
                                FROM expenses WHERE id = (?);''', (toEdit,))
            cprint(f"@history: {usersbase[0]}", "cyan")
            # Declare the lists for the variable storage
            nid = []
            tgid = []
            type = []
            amount = []
            comment = []
            date = []
            time = []
            curren = []
            iterations = len(usersbase)
            # Populates the lists with values from the joined tables
            for i in range(iterations):
                nid.append((usersbase[i])["id"])
                tgid.append((usersbase[i])["users_id"])
                type.append((usersbase[i])["type"])
                amount.append((usersbase[i])["amount"])
                comment.append((usersbase[i])["comment"])
                date.append((usersbase[i])["date"])
                time.append((usersbase[i])["time"])
                curren.append((usersbase[i])["currency"])
            # To have the current record's currency at the first place in the
            # dropdown menu creates a new list with the first element equal to
            # the current record currency
            temporaryCurrencyList = []
            temporaryCurrencyList.append(curren[0])
            # Appends the rest of the available currency
            # abbreviations to the list
            for i in range(len(listOfKeys)):
                temporaryCurrencyList.append(listOfKeys[i])
            print("@history(): ", temporaryCurrencyList[0])
            listOfKeys = temporaryCurrencyList
            # Renders the history page
            return render_template("history.html", nid=nid, tgid=tgid,
                                   type=type, amount=amount, comment=comment,
                                   date=date, time=time, iterations=iterations,
                                   cur=cur, curren=curren,
                                   edit_mode=edit_mode, listOfKeys=listOfKeys)
        # If the mode is Update:
        if mode == "update":
            print("@history(): I'm in")
            print("@history(): FROM INPUT:")
            # Populates variables with the new values
            # converting them to the proper types correspondingly
            new_type = str(request.form["new_type"])
            new_amount = str(request.form["new_amount"])
            new_comment = str(request.form["new_comment"])
            new_currency = str(request.form["new_currency"])
            new_id = int(request.form["new_id"])
            print("@history(): ", new_type)
            print("@history(): ", new_amount)
            print("@history(): ", new_comment)
            print("@history(): ", new_currency)
            print("@history(): ", new_id)
            print("@history(): that's all")
            # Gets the record with the selected ID from the expenses database
            usersbase = db.execute('''SELECT *
                                FROM expenses
                                WHERE id = (?);''', (new_id,))
            # Populates the variables with the values from the selection
            originalCurrency = usersbase[0]['currency']
            originalType = usersbase[0]['type']
            originalAmount = usersbase[0]['amount']
            originalComment = usersbase[0]['comment']
            cprint(f"@history: {originalCurrency}", "cyan")
            # Checks if there was no changes made to the input forms
            if ((str(new_currency) == str(originalCurrency))
                and ((str(originalType) == str(new_type))
                     or (str(new_type) == ""))
                and ((str(originalAmount) == str(new_amount))
                     or (str(new_amount) == ""))
                and ((str(originalComment) == str(new_comment))
                     or (str(new_comment) == ""))):
                cprint("@history(): all the fields remain the same. "
                       "No change required", "red")
            # If the changes were made to any of the field and the
            # new values do not match the previous ones
            else:
                cprint("@history(): Changes have to be applied!!!", "yellow")
                if new_type == "":
                    new_type = originalType
                if new_amount == "":
                    new_amount = originalAmount
                if new_comment == "":
                    new_comment = originalComment
                # Updates the record with the given ID in the expenses table
                db.execute('''UPDATE expenses
                           SET type = ?, amount = ?, comment = ?,
                           currency = ? WHERE id = ?;''', new_type,
                           new_amount, new_comment, new_currency, new_id,)
    # If the user gets to the page via "GET" request
    else:
        print("hey GET")
    # Reads all the records from the database for the current user ID
    usersbase = db.execute('''SELECT id, type, amount, comment,
                           date, time, users_id, currency
                           FROM expenses
                           WHERE users_id = (?) ORDER BY id DESC;''', (uid,))
    # Declare the lists for the variable storage
    nid = []
    tgid = []
    type = []
    amount = []
    comment = []
    date = []
    time = []
    curren = []
    iterations = len(usersbase)
    # Populates the lists with values from the joined tables
    for i in range(iterations):
        nid.append((usersbase[i])["id"])
        tgid.append((usersbase[i])["users_id"])
        type.append((usersbase[i])["type"])
        amount.append((usersbase[i])["amount"])
        comment.append((usersbase[i])["comment"])
        date.append((usersbase[i])["date"])
        time.append((usersbase[i])["time"])
        curren.append((usersbase[i])["currency"])
    # Sets the edit mode to 1
    edit_mode = 1
    # Renders the history page
    return render_template("history.html", nid=nid, tgid=tgid, type=type,
                           amount=amount, comment=comment, date=date,
                           time=time, iterations=iterations,
                           cur=cur, curren=curren, edit_mode=edit_mode)


# Provides a login page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Log user in
    cprint(f"@login: {base_check()}", "cyan")
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("tg_id"):
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        # Query database for username
        rows = db.execute('''SELECT *
                          FROM users
                          WHERE tg_id = ?''', request.form.get("tg_id"))
        # Ensure username exists and password is correct
        if (len(rows) != 1 or
            not check_password_hash(rows[0]["hash"],
                                    request.form.get("password"))):
            return apology("invalid username or password", 403)
        # Remember which user has logged in
        session["tg_id"] = rows[0]["tg_id"]
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Log user out
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


# Provides a page to set personal preferences
@app.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    cprint(f"@preferences: {base_check()}", "cyan")
    # Gets current session's user ID
    uid = int(session['tg_id'])
    global cur
    # Gets default currency value for the current user
    usersbase = db.execute('''SELECT default_currency
                           FROM users
                           WHERE tg_id = ?;''', uid)
    cur = (usersbase[0])["default_currency"]
    cprint(f"@preferences: {cur}", "cyan")
    # If the user gets to the page via "POST"
    if request.method == "POST":
        # Checks if the currency value provided
        tmp = request.form.get("currency")
        cprint(f"@preferences: {tmp}", "cyan")
        if not (tmp):
            return apology("must provide correct currency", 403)
        else:
            # Updates the default currency value for the current user
            # in the users table
            cur = str(tmp)
            db.execute('''UPDATE users
                       SET default_currency = ?
                       WHERE tg_id = ?;''', cur, uid,)
    # Assignes the list of possible keys to the variable
    listOfKeys = keys()
    # Assignes current rate to the variable
    rate = rates(cur)
    # Renders the preferences page
    return render_template("preferences.html", cur=cur, rate=rate,
                           listOfKeys=listOfKeys)


# Provides about page
@app.route("/about", methods=["GET", "POST"])
def about():
    # Renders the about page
    return render_template("about.html")


# Provides a page for new user registration
# This function was adopted from the CS50 course with minor changes
@app.route("/register", methods=["GET", "POST"])
def register():
    # Forgets any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensures username was submitted
        if not request.form["tg_id"]:
            return apology("must provide username", 400)
        # Checks if the user's ID is in the users table
        rows = db.execute('''SELECT *
                          FROM users
                          WHERE tg_id = ?''', request.form["tg_id"])
        # Ensure username exists and password is correct
        if len(rows) == 1:
            return apology("User already exists. Please log in instead", 400)
        # Ensure password was submitted
        elif not request.form["password"]:
            return apology("must provide password", 400)
        # Ensure password confirmation was submitted
        elif not request.form["confirmation"]:
            return apology("Enter confirmation", 400)
        # Checks if the confirmation is the same as password
        elif request.form["confirmation"] != request.form["password"]:
            return apology("passwords do not match", 400)
        # Adds a user and password hash to the database
        a = request.form["tg_id"]
        b = generate_password_hash(request.form["password"],
                                   method='pbkdf2:sha256', salt_length=8)
        db.execute('''INSERT INTO users (tg_id, hash)
                   VALUES (?, ?)''', a, b)
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Return apology("TODO")
        return render_template("register.html")
