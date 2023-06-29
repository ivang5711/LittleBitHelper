# This file called bot.py contains a code for the Telegram bot client for
# the LittleBitHelper project
# To run the file type ./../python bot.py in your terminal

import sqlite3
import logging
from aiogram import Bot, Dispatcher, executor, types
from datetime import date
from datetime import datetime
from termcolor import cprint


# Defines API token
API_TOKEN = 'PLACE_YOUR_TELEGRAM_BOT_TOKEN_HERE'


# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Tries to create a new database. Skips if the DB is already exists
con = sqlite3.connect('expenses.db')
cprint("@initialization: Opened database successfully", "blue")
con.execute('''CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    amount INT NOT NULL,
    comment TEXT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    users_id INTEGER NOT NULL,
    currency TEXT NOT NULL DEFAULT 'USD',
    FOREIGN KEY(users_id) REFERENCES users(id)
    ); ''')
cprint("@initialization: Table EXPENSES ready", "blue")
con.close()
con = sqlite3.connect('expenses.db')
con.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    tg_id TEXT NOT NULL,
    hash TEXT NOT NULL,
    default_currency TEXT NOT NULL DEFAULT 'USD'
    ); ''')
cprint("@initialization: Table USERS ready", "blue")
con.close()


# Creates an array with the currency indexes
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


# Checks if the user is allowed
def check(func):
    async def userCheck(message):
        # Gets user ID from the message sent to the Telegram Bot
        userId = message['from']['id']
        # Connects to the database and gets all the users from the table
        con = sqlite3.connect('expenses.db')
        cursor = con.execute('''SELECT tg_id
                             FROM users
                             ORDER BY id DESC;''')
        databaseResponse = cursor.fetchall()
        con.close()
        databaseResponseLength = len(databaseResponse)
        cprint(f"@check: Current user ID: {userId}", "blue")
        cprint(f"@check: Users in database: {databaseResponseLength}", "blue")
        # Checks if the particular user is in the users table
        for i in range(databaseResponseLength):
            cprint(f"@check: database id: {databaseResponse[i][0]}", "blue")
            cprint(f"@check: current user id: {userId}", "blue")
            if str(userId) == str(databaseResponse[i][0]):
                cprint("@check: User allowed", "blue")
                return await func(message)
        # If the user is not in the table returns the following message
        cprint("@check: User not allowed", "blue")
        return await message.reply("Register first. use /start to get "
                                   "your id and go to the web app "
                                   "to register", reply=False)
    return userCheck


# Gets user's default currency from
def defaultCurrency(message):
    # Gets user ID from the message sent to the Telegram Bot
    userId = message['from']['id']
    cprint(f"@defaultCurrency: {str(userId)}", "blue")
    # Connects to the database and gets user's default_currency value
    con = sqlite3.connect('expenses.db')
    cursor = con.execute('''SELECT default_currency
                            FROM users
                            WHERE tg_id = ?
                            ORDER BY id DESC;''', (userId,))
    databaseResponse = cursor.fetchone()
    cprint(f"@defaultCurrency: {str(databaseResponse)}", "blue")
    con.close()
    answer = databaseResponse[0]
    cprint(f"@defaultCurrency: {answer}", "blue")
    return answer


# Start command handler
# This handler will be called when user sends `/start` command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Gets user ID from the message sent to the Telegram Bot
    userId = message['from']['id']
    # Gets user name from the message sent to the Telegram Bot
    userName = message['from']['username']
    # Connects to the database and gets all the users from users table
    con = sqlite3.connect('expenses.db')
    cursor = con.execute('''SELECT tg_id
                         FROM users
                         ORDER BY id DESC;''')
    databaseResponse = cursor.fetchall()
    con.close()
    databaseResponseLength = len(databaseResponse)
    cprint(f"@send_welcome: Current user ID: {userId}", "blue")
    cprint(f"@send_welcome: Users in "
           f"database: {databaseResponseLength}", "blue")
    # Checks if the user is already in database
    flag = 0
    for i in range(databaseResponseLength):
        cprint(f"@send_welcome: database id: {databaseResponse[i][0]}", "blue")
        cprint(f"@send_welcome: current user id: {userId}", "blue")
        if str(userId) == str(databaseResponse[i][0]):
            cprint("@send_welcome: User allowed", "blue")
            flag = 1
            break
    # If the user is in database send a message with the list
    # of available commands
    if flag == 1:
        await message.reply("User already registered", reply=False)
        cprint(f"@send_welcome: User allowed {userId}", "blue")
        await message.answer("Dear " + str(userName)
                             + ", \n" + "Hello and welcome to the "
                             "LittleBitHelperBot")
        await message.answer("A list of available commands:"
                             "\n/start - shows this message"
                             "\n/help - shows a list of available commands\n")
    # If the user is not in the databse send a message with user's Tekegram ID
    else:
        cprint(f"@send_welcome: User not allowed {userId}", "blue")
        await message.answer('''Hello and welcome to the LittleBitHelperBot
                             \nYour ID is:\n''' + str(userId))


# Help command handler
# This handler will be called when user sends `/help` command
@dp.message_handler(commands=['help'])
@check
async def help(message: types.Message):
    # Sends a list of available commands
    await message.answer("A list of available commands:"
                         "\n/start - shows welcome message"
                         "\n/help - shows a list of available commands"
                         "\n/new - add a new expense record."
                         "\nUseage: type amount comment."
                         "\nExample: taxi 350 to airport"
                         "\n/all - provides a summ of all "
                         "expenses for all time"
                         "\n/typed - provides a list of types with "
                         "total amount spent for each type"
                         "\n/history - prints out all the records"
                         "\n/delete - allows to deleta a record."
                         "\nUsage: specify a record "
                         "id (history command can "
                         "help to find an id)."
                         "\nExample: 17\n"
                         "/currency - allows to change the default currency."
                         "\nUsage: specify new currency."
                         "\nExample: USD"
                         "\nYou can get the current currency value by "
                         "sending the following command:"
                         "\n/currency current")


# Add new record to the expenses table
# This handler will be called when user sends `/new` command
@dp.message_handler(commands=['new'])
@check
async def add_new(message: types.Message):
    # Gets user's ID
    user = types.User.get_current()
    userId = int(user['id'])
    # Gets user's message from bot
    messageString = ""
    messageString = message.text
    typeArray = []
    amountArray = []
    commentArray = []
    # Parses the user's message from string to the separate arrays
    flag = 0
    for i in range(5, len(messageString)):
        if messageString[i] != " " and flag == 0:
            typeArray.append(messageString[i])
        elif messageString[i] == " " and flag == 0:
            flag = 1
        elif messageString[i] != " " and flag == 1:
            amountArray.append(messageString[i])
        elif messageString[i] == " " and flag == 1:
            flag = 2
        elif flag == 2:
            commentArray.append(messageString[i])
    # converts the arrays to strings
    type = ""
    for i in range(len(typeArray)):
        type += typeArray[i]
    amount = ""
    for i in range(len(amountArray)):
        amount += amountArray[i]
    comment = ""
    for i in range(len(commentArray)):
        comment += commentArray[i]
    # Checks if the amount provided is digit
    if amount.isdigit():
        cprint("@add_new: yes, is digit", "blue")
        # Checks if the amount provided is greater than zero
        if int(amount) > 0:
            cprint("@add_new: amount > 0 and is valid", "blue")
            cprint(f"@add_new: {type, amount, comment}", "blue")
            # Gets date and time in ISO format
            dateISO = date.today().isoformat()
            dtn = datetime.now()
            timeISO = dtn.strftime("%H:%M:%S")
            cprint("@add_new: Opened database successfully", "blue")
            # Gets a user's default currency value
            currency = defaultCurrency(message)
            cprint(f"@add_new: {str(currency)}", "blue")
            # Adds new record to the expenses table
            con = sqlite3.connect('expenses.db')
            con.execute('''INSERT INTO expenses (
                type, amount, comment, date, time, users_id, currency)
                VALUES (?, ?, ?, ?, ?, ?, ?
                );''', (type, amount, comment, dateISO,
                        timeISO, userId, currency))
            con.commit()
            con.close()
            cprint("@add_new: Records created successfully", "blue")
            # prints the message if the insert was successfull
            await message.answer("New record added successfully")
        else:
            # Prints the error message if the value provided is less
            # or equal to zero
            cprint("@add_new: the valuse is = or less than 0", "blue")
            await message.answer("Please provide expense "
                                 "value greater than 0")
    else:
        # Prints an error message if the amount value provided is
        # not a digit
        cprint("@add_new: no, not a digit", "blue")
        await message.answer("Please provide input in the "
                             "following format: "
                             "\ntype amount comment"
                             "\nExample:\n/new taxi 125 trip from Airport")


# Prints out all the records
# This handler will be called when user sends `/all` command
@dp.message_handler(commands=['all'])
@check
async def all(message: types.Message):
    # Gets user's ID
    userId = int(message['from']['id'])
    # Gets a sum of all the records of the current user
    con = sqlite3.connect('expenses.db')
    cursor = con.execute('''SELECT SUM(amount)
                         FROM expenses
                         WHERE users_id = (?);''', (userId,))
    databaseResponse = cursor.fetchone()
    con.close()
    # Returns the sum to the user via messages
    answer = "All expenses: " + str(databaseResponse[0])
    cprint(f"@all: {databaseResponse[0]}", "blue")
    await message.answer(answer)


# Prints out all the records by type
# This handler will be called when user sends `/typed` command
@dp.message_handler(commands=['typed'])
@check
async def typed(message: types.Message):
    # Gets user's ID
    userId = int(message['from']['id'])
    # Gets the users records grouped by type
    con = sqlite3.connect('expenses.db')
    cursor = con.execute('''SELECT type, amount, users_id
                         FROM expenses
                         WHERE users_id = (?)
                         GROUP BY type
                         ORDER BY type;''', (userId,))
    databaseResponse = cursor.fetchall()
    databaseResponseLength = len(databaseResponse)
    con.close()
    # Checks if the output is not empty
    if databaseResponseLength == 0:
        # If the output is empty prints "nothing to show" message
        cprint("@typed: nothing to show yet...", "blue")
        await message.answer("nothing to show yet...")
    # If there are grouped record to show prints out them line by line
    for i in range(databaseResponseLength):
        cprint(f"@typed: {databaseResponse[i]}", "blue")
        await message.answer(str(databaseResponse[i][0]) + " | "
                             + str(databaseResponse[i][1]))


# Prints out all the records history
# This handler will be called when user sends `/history` command
@dp.message_handler(commands=['history'])
@check
async def history(message: types.Message):
    # Gets user's ID
    userId = int(message['from']['id'])
    # Gets all the users records
    con = sqlite3.connect('expenses.db')
    cursor = con.execute('''SELECT *
                          FROM expenses
                          WHERE users_id = (?);''', (userId,))
    databaseResponse = cursor.fetchall()
    databaseResponseLength = len(databaseResponse)
    con.close()
    cprint(f"{databaseResponse}", "blue")
    # If the output is empty prints "nothing to show" message
    if databaseResponseLength == 0:
        cprint("@history: nothing to show yet...", "blue")
        await message.answer("nothing to show yet...")
    # If there are records to show prints out them line by line
    for i in range(databaseResponseLength):
        cprint(f"@history: {databaseResponse[i]}", "blue")
        await message.answer(str(databaseResponse[i][0]) + " | "
                             + str(databaseResponse[i][1]) + " | "
                             + str(databaseResponse[i][2]) + " | "
                             + str(databaseResponse[i][3]) + " | "
                             + str(databaseResponse[i][4]) + " | "
                             + str(databaseResponse[i][5]) + " | "
                             + str(databaseResponse[i][7]))


# Deletes a record
# This handler will be called when user sends `/delete` command
@dp.message_handler(commands=['delete'])
@check
async def delete(message: types.Message):
    # Parses the user's input
    messageString = ""
    messageString = message.text
    messageStringLength = len(messageString)
    # Appends each symbol from the user's input to array
    deleteIdArray = []
    for i in range(7, messageStringLength):
        if messageString[i] != " ":
            deleteIdArray.append(messageString[i])
    # Converts the array to a string
    deleteId = ""
    deleteIdArrayLength = len(deleteIdArray)
    for i in range(deleteIdArrayLength):
        deleteId += deleteIdArray[i]
    # Checks if the string contains digits only
    if deleteId.isdigit():
        cprint("@delete: yes, is digit", "blue")
        # Checks if the value is greater than zero
        if int(deleteId) > 0:
            cprint("@delete: amount > 0 and is valid", "blue")
            cprint(f"@delete: {deleteId}", "blue")
            # Gets user's ID
            userId = int(message['from']['id'])
            flag = 0
            # Gets the all ids for the specified user from
            # the expenses table
            con = sqlite3.connect('expenses.db')
            cursor = con.execute('''SELECT id, users_id
                                  FROM expenses
                                  WHERE users_id = (?);''', (userId,))
            databaseResponse = cursor.fetchall()
            databaseResponseLength = len(databaseResponse)
            con.close()
            cprint(f"@delete: {databaseResponse}", "blue")
            # Checks if the user has resords history
            if databaseResponseLength == 0:
                # If no results returns "nothing to delete" message
                cprint("@delete: nothing to delete...", "blue")
                flag = 0
                await message.answer("nothing to delete yet...")
            # If the user has records history:
            else:
                cprint("@delete: user has records history. Wait...", "blue")
                # Checks if the specified ID is among the user's records
                for i in range(databaseResponseLength):
                    cprint(f"@delete: {databaseResponse[i][0]}", "blue")
                    cprint(f"@delete: {deleteId}", "blue")
                    if int(deleteId) == int(databaseResponse[i][0]):
                        cprint("@delete: The match is found. Ready "
                               "to delete", "blue")
                        flag = 1
                        break
            # If match is found then deletes the whole row from the table
            if flag == 1:
                con = sqlite3.connect('expenses.db')
                cur = con.cursor()
                result = cur.execute('''DELETE FROM expenses
                                     WHERE id = (?);''', (deleteId,))
                result.fetchone()
                cprint("@delete: Records deleted successfully", "blue")
                con.commit()
                cprint("@delete: Records really deleted successfully", "blue")
                await message.answer("Record with ID: " + deleteId
                                     + " deleted successfully!")
                await message.answer("/history")
            # If no matches found returns the following message:
            if flag == 0:
                await message.answer("No such ID. Use /history "
                                     "command to see all the IDs")
        # If id provided is less or equal to zero
        # returns the following message:
        else:
            await message.answer("No such ID. Use /history "
                                 "command to see all the IDs")
    # If id provided is not a digit returns the following message:
    else:
        await message.answer("No such ID. Use /history "
                             "command to see all the IDso")


# Changes user's default currency
# This handler will be called when user sends `/currency` command
@dp.message_handler(commands=['currency'])
@check
async def change_currency(message: types.Message):
    # Gets user's ID
    userId = int(message['from']['id'])
    # Gets user's message
    messageString = ""
    messageString = message.text
    messageStringLength = len(messageString)
    # Converts user's message into array
    currencyArray = []
    for i in range(9, messageStringLength):
        if messageString[i] != " ":
            currencyArray.append(messageString[i])
    # Converts the array into string
    currencyNew = ""
    currencyArrayLength = len(currencyArray)
    for i in range(currencyArrayLength):
        currencyNew += currencyArray[i]
    currencyNew = str(currencyNew)
    cprint(f"@currency: {currencyNew}", "blue")
    # Checks if the string is equal to "current"
    if currencyNew == "current":
        # Gets the default_currency value
        con = sqlite3.connect('expenses.db')
        cur = con.cursor()
        result = cur.execute('''SELECT default_currency
                             FROM users WHERE tg_id = (?);''', (userId,))
        currencyDefault = result.fetchone()[0]
        # Returns the default currency value
        cprint(f"@currency: Current default "
               f"currency: {currencyDefault}", "blue")
        await message.answer("Current default currency: " + currencyDefault)
    # If the string is not the "currency"
    # checks if it is a valid currecny abbreviation
    elif currencyNew in cur_index:
        # If the input is correct and is a valid currecny abbreviation
        # Updates the default_currency colums of the users table with
        # the new value
        cprint("@currency: valid", "blue")
        con = sqlite3.connect('expenses.db')
        cur = con.cursor()
        result = cur.execute('''UPDATE users
                             SET default_currency = (?)
                             WHERE tg_id = (?);''', (currencyNew, userId))
        result.fetchone()
        con.commit()
        cprint("@currency: Currency changed successfully", "blue")
        cprint("@currency: Currency changed successfully2", "blue")
        # Returns the message with the new default currency value
        await message.answer("Currency changed successfully!\nNew "
                             "currency: " + currencyNew)
    else:
        # In case of incorrect input returns the message with some guidance
        cprint("@currency: not valid", "blue")
        await message.answer("No such currency. Usage: /currency currency "
                             "symbol.\nExample:\n/currency USD\ntype "
                             "current to see current user's "
                             "currency\nExample:\n/currency current")


# Echo handler
# This handler will be called when user sends any unspecified input
# This one here does not do anything useful except that it can be
# useful to see if the bot is operational
@dp.message_handler()
@check
async def echo(message: types.Message):
    print("@echo: ", message.text)
    await message.answer(message.text)


# Main
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
