from flask import Flask, request, render_template, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "jeet1606"

# 🔑 Cloudflare D1 credentials
ACCOUNT_ID = "07f4ac146ed0740bd1b926a964bf95c2"
DB_ID = "482815c5-c41b-4292-a71f-19a45d2b5aa0"
API_TOKEN = "vJ0c4oFFKjbEpbIRZcfjpSgLIIm6i2BvzzFC_w4a"

# 🔁 helper function
def run_query(sql):
    url = f"https://api.cloudflare.com/client/v4/accounts/07f4ac146ed0740bd1b926a964bf95c2/d1/database/482815c5-c41b-4292-a71f-19a45d2b5aa0/query"

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json={
        "sql": sql
    })

    return response.json()

app=Flask(__name__)
app.secret_key="jeet1606"

@app.route('/')
def index():
    return redirect(url_for('signup'))

@app.route('/home', methods=['GET', 'POST'])
def home_page():
    userid = session.get("userid")
    username = session.get("username")

    # calculate balance dynamically
    sql_income = f"SELECT SUM(income_amount) as total FROM income WHERE userid={userid}"
    sql_expense = f"SELECT SUM(expense_amount) as total FROM expense WHERE userid={userid}"

    income = run_query(sql_income)
    expense = run_query(sql_expense)

    total_income = income['result'][0]['results'][0]['total'] or 0
    total_expense = expense['result'][0]['results'][0]['total'] or 0

    balance = total_income - total_expense

    return render_template('home.html', username=username, balance=balance)
        
    return render_template('home.html',username=username,userid=userid,balance=balance)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        username = request.form['user_name']
        password = request.form['pass_word']

        sql = f"""
        SELECT userid, password FROM users
        WHERE username='{username}'
        """
        result = run_query(sql)

        if result['result'][0]['results']:
            user = result['result'][0]['results'][0]

            if user['password'] == password:
                session['userid'] = user['userid']
                session['username'] = username
                return redirect(url_for('home_page'))
            else:
                return "Invalid password"

        return "User not found"

    return render_template('signin.html')


#mycur.execute("CREATE DATABASE expensetracker")
#mycur.execute("CREATE TABLE users(userid INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(30),password VARCHAR(25))")
#mycur.execute("CREATE TABLE income( userid INT,  income_amount INT, income_source VARCHAR(250), FOREIGN KEY(userid) REFERENCES users(userid),date VARCHAR(250) )")
#mycur.execute("CREATE TABLE expense(userid INT, expense_amount INT, expense_source VARCHAR(250), FOREIGN KEY(userid) REFERENCES users(userid), date VARCHAR(250))")
#mycur.execute("CREATE TABLE balance(userid INT,total_balance INT, FOREIGN KEY(userid) REFERENCES users(userid))")
#mycur.execute("DROP TABLE income")
#mycur.execute("DROP TABLE expense")
#mycur.execute("DROP TABLE balance")
#mycur.execute("DROP TABLE users")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form['user_name']
        password = request.form['pass_word']

        sql = f"""
        INSERT INTO users (username, password)
        VALUES ('{username}', '{password}')
        """
        run_query(sql)

        # fetch userid
        sql = f"SELECT userid FROM users WHERE username='{username}'"
        result = run_query(sql)

        userid = result['result'][0]['results'][0]['userid']

        session['userid'] = userid
        session['username'] = username

        return redirect(url_for('home_page'))

    return render_template('signup.html')

@app.route('/addincome', methods=['GET', 'POST'])
def adding_income():
    if request.method == "POST":
        userid = session.get("userid")
        amount = request.form['amountincome']
        source = request.form['incomesource']
        date = request.form['dateincome']

        sql = f"""
        INSERT INTO income (userid, income_amount, income_source, transaction_date)
        VALUES ({userid}, {amount}, '{source}', '{date}')
        """
        run_query(sql)

        return redirect(url_for('home_page'))

    return render_template('addincome.html')

from flask import Flask, request, render_template, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "jeet1606"

# 🔑 Cloudflare D1 credentials
ACCOUNT_ID = "07f4ac146ed0740bd1b926a964bf95c2"
DB_ID = "482815c5-c41b-4292-a71f-19a45d2b5aa0"
API_TOKEN = "vJ0c4oFFKjbEpbIRZcfjpSgLIIm6i2BvzzFC_w4a"

# 🔁 helper function
def run_query(sql):
    url = f"https://api.cloudflare.com/client/v4/accounts/07f4ac146ed0740bd1b926a964bf95c2/d1/database/482815c5-c41b-4292-a71f-19a45d2b5aa0/query"

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json={
        "sql": sql
    })

    return response.json()

app=Flask(__name__)
app.secret_key="jeet1606"

@app.route('/')
def index():
    return redirect(url_for('signup'))

@app.route('/home', methods=['GET', 'POST'])
def home_page():
    userid = session.get("userid")
    username = session.get("username")

    # calculate balance dynamically
    sql_income = f"SELECT SUM(income_amount) as total FROM income WHERE userid={userid}"
    sql_expense = f"SELECT SUM(expense_amount) as total FROM expense WHERE userid={userid}"

    income = run_query(sql_income)
    expense = run_query(sql_expense)

    total_income = income['result'][0]['results'][0]['total'] or 0
    total_expense = expense['result'][0]['results'][0]['total'] or 0

    balance = total_income - total_expense

    return render_template('home.html', username=username, balance=balance)
        
    return render_template('home.html',username=username,userid=userid,balance=balance)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        username = request.form['user_name']
        password = request.form['pass_word']

        sql = f"""
        SELECT userid, password FROM users
        WHERE username='{username}'
        """
        result = run_query(sql)

        if result['result'][0]['results']:
            user = result['result'][0]['results'][0]

            if user['password'] == password:
                session['userid'] = user['userid']
                session['username'] = username
                return redirect(url_for('home_page'))
            else:
                return "Invalid password"

        return "User not found"

    return render_template('signin.html')


#mycur.execute("CREATE DATABASE expensetracker")
#mycur.execute("CREATE TABLE users(userid INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(30),password VARCHAR(25))")
#mycur.execute("CREATE TABLE income( userid INT,  income_amount INT, income_source VARCHAR(250), FOREIGN KEY(userid) REFERENCES users(userid),date VARCHAR(250) )")
#mycur.execute("CREATE TABLE expense(userid INT, expense_amount INT, expense_source VARCHAR(250), FOREIGN KEY(userid) REFERENCES users(userid), date VARCHAR(250))")
#mycur.execute("CREATE TABLE balance(userid INT,total_balance INT, FOREIGN KEY(userid) REFERENCES users(userid))")
#mycur.execute("DROP TABLE income")
#mycur.execute("DROP TABLE expense")
#mycur.execute("DROP TABLE balance")
#mycur.execute("DROP TABLE users")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form['user_name']
        password = request.form['pass_word']

        sql = f"""
        INSERT INTO users (username, password)
        VALUES ('{username}', '{password}')
        """
        run_query(sql)

        # fetch userid
        sql = f"SELECT userid FROM users WHERE username='{username}'"
        result = run_query(sql)

        userid = result['result'][0]['results'][0]['userid']

        session['userid'] = userid
        session['username'] = username

        return redirect(url_for('home_page'))

    return render_template('signup.html')

@app.route('/addincome', methods=['GET', 'POST'])
def adding_income():
    if request.method == "POST":
        userid = session.get("userid")
        amount = request.form['amountincome']
        source = request.form['incomesource']
        date = request.form['dateincome']

        sql = f"""
        INSERT INTO income (userid, income_amount, income_source, transaction_date)
        VALUES ({userid}, {amount}, '{source}', '{date}')
        """
        run_query(sql)

        return redirect(url_for('home_page'))

    return render_template('addincome.html')

@app.route('/addexpense', methods=['GET', 'POST'])
def adding_expense():
    if request.method == "POST":
        userid = session.get("userid")
        amount = request.form['amountexpense']
        source = request.form['expensesource']
        date = request.form['dateexpense']

        sql = f"""
        INSERT INTO expense (userid, expense_amount, expense_source, transaction_date)
        VALUES ({userid}, {amount}, '{source}', '{date}')
        """
        run_query(sql)

        return redirect(url_for('home_page'))

    return render_template('addexpense.html')

@app.route('/viewtransactions')
def view_transactions():
    userid = session.get("userid")

    sql = f"""
    SELECT income_amount as amount, income_source as source, transaction_date as date, 'Income' as type
    FROM income WHERE userid={userid}

    UNION ALL

    SELECT expense_amount as amount, expense_source as source, transaction_date as date, 'Expense' as type
    FROM expense WHERE userid={userid}

    ORDER BY date DESC
    """

    result = run_query(sql)

    transactions = result['result'][0]['results']

    return render_template("viewtransactions.html", transactions=transactions)
        





        
