# This file called helpers.py contains auxilary functions for
# the LittleBitHelper project
# to use functions from the file import them into your code via import

import requests
import json
from datetime import date
from flask import redirect, render_template, session
from functools import wraps
from termcolor import cprint


# Render message as an apology to user.
def apology(message, code=400):
    return render_template("apology.html", top=code,
                           bottom=message)


# Checks if the user is logged in
def login_required(f):
    # Decorate routes to require login.
    # https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("tg_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Checks JSON file and updates it if necessuary
def base_check():
    # Opening JSON file
    f = open('data.json', "r")
    try:
        data = json.load(f)
        check = data['timestamp']
        cprint(f"@base_check: check: {check}", "magenta")
    except ValueError:
        # In case of an error sets the timestamp to the obviously wrong date
        check = 1111111111
        cprint(f"@base_check: no data {check}", "magenta")
    f.close()
    time_stamp = check
    cprint(f"@base_check: Timestamp: {time_stamp}", "magenta")
    date_time = date.fromtimestamp(time_stamp).isoformat()
    cprint(f"@base_check: The date is: {date_time}", "magenta")
    ts = date.today().isoformat()
    cprint(f"@base_check: Today is: {ts}", "magenta")
    flag = 0
    cprint("@base_check: flags:", "magenta")
    # A series of checks compares the timestamp with current date
    if date_time == ts:
        flag = 1
        cprint(f"@base_check: {flag}", "magenta")
        fd = "JSON is up to date"
        cprint(f"@base_check: {fd}", "green")
        return fd
    else:
        flag = 0
        cprint(f"@base_check: {flag}", "magenta")
    if flag == 0:
        # If the timestamp does not match then send a request via API
        # Contact API
        dat = date.today().isoformat()
        url = (f"https://openexchangerates.org/api/historical/{dat}.json?ap"
               "p_id=b3ce64356fea4b50abde8cbb5ac61474&show_alternative=fa"
               "lse&prettyprint=false")
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        cprint(f"@base_check: Response {response}", "yellow")
        newdict = json.loads(response.text)
        err = "JSON update error"
        # Tries to get the data from the recieved response
        try:
            cprint(f"@base_check: {newdict['rates']}", "magenta")
        except KeyError:
            # Returns an error message if failed
            cprint("@base_check: JSON error", "red")
            cprint(f"@base_check: {dat}", "magenta")
            return err
        # If no errors writes down the data to the JSON file
        data = newdict
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        cd = "JSON updated successfully!"
        cprint(f"@base_check: {cd}", "green")
        return cd


# Calculates exchange rate relative to USD. uses local JSON with.
# Rates data updates once a day
def rates(currency):
    # Checks the rate
    # Opens the JSON file in read mode
    f = open('data.json', "r")
    data = json.load(f)
    check = data['rates']
    f.close()
    rate = (check[currency])
    cprint(f"@rates: {rate}", "magenta")
    return rate


# Return currency symbol
def currency(value, cur):
    def symb(currencySymbol):
        # A dictionary of available currencies and their symbols
        symbols = {"ALL": "Lek", "AFN": "؋", "ARS": "$", "AWG": "ƒ",
                   "AUD": "$", "AZN": "₼", "BSD": "$", "BBD": "$",
                   "BYN": "Br", "BZD": "BZ$", "BMD": "$", "BOB": "$b",
                   "BAM": "KM", "BWP": "P", "BGN": "лв", "BRL": "R$",
                   "BND": "$", "KHR": "៛", "CAD": "$", "KYD": "$",
                   "CLP": "$", "CNY": "¥", "COP": "$", "CRC": "₡",
                   "HRK": "kn", "CUP": "₱", "CZK": "Kč", "DKK": "kr",
                   "DOP": "RD$", "XCD": "$", "EGP": "£", "SVC": "$",
                   "EUR": "€", "FKP": "£", "FJD": "$", "GHS": "¢",
                   "GIP": "£", "GTQ": "Q", "GGP": "£", "GYD": "$",
                   "HNL": "L", "HKD": "$", "HUF": "Ft", "ISK": "kr",
                   "INR": "₹", "IDR": "Rp", "IRR": "﷼", "IMP": "£",
                   "ILS": "₪", "JMD": "J$", "JPY": "¥", "JEP": "£",
                   "KZT": "лв", "KPW": "₩", "KRW": "₩", "KGS": "лв",
                   "LAK": "₭", "LBP": "£", "LRD": "$", "MKD": "ден",
                   "MYR": "RM", "MUR": "₨", "MXN": "$", "MNT": "₮",
                   "MZN": "MT", "NAD": "$", "NPR": "₨", "ANG": "ƒ",
                   "NZD": "$", "NIO": "C$", "NGN": "₦", "NOK": "kr",
                   "OMR": "﷼", "PKR": "₨", "PAB": "B/.", "PYG": "Gs",
                   "PEN": "S/.", "PHP": "₱", "PLN": "zł", "QAR": "﷼",
                   "RON": "lei", "RUB": "₽", "SHP": "£", "SAR": "﷼",
                   "RSD": "Дин.", "SCR": "₨", "SGD": "$", "SBD": "$",
                   "SOS": "S", "KRW": "₩", "ZAR": "R", "LKR": "₨",
                   "SEK": "kr", "CHF": "CHF", "SRD": "$", "SYP": "£",
                   "TWD": "NT$", "THB": "฿", "TTD": "TT$", "TRY": "₺",
                   "TVD": "$", "UAH": "₴", "AED": "د.إ", "GBP": "£",
                   "USD": "$", "UYU": "$U", "UZS": "лв", "VEF": "Bs",
                   "VND": "₫", "YER": "﷼", "ZWD": "Z$", "GEL": "₾"
                   }
        # Tries to get a corresponding symbol
        try:
            symbol = str(symbols[currencySymbol])
        except NameError:
            # If fails returns an abbreviation
            symbol = str(currencySymbol)
        return symbol
    # Formates the value-symbol pair accordingly
    formatted = f"{symb(cur)} {value:,.2f}"
    return formatted


# provides a list of the currency indexes
def keys():
    # Opens a JSON file in read mode
    f = open('data.json', "r")
    data = json.load(f)
    mylist = []
    rates = data['rates']
    f.close()
    # Populates the array with currency indexes from JSON
    # This makes the index check more robust becaue it
    # checks dynamically through the rates provider current data set
    for key in rates.keys():
        mylist.append(key)
    cprint(f"@keys {mylist}", "magenta")
    return mylist
