from flask import *

import os

from db import *
from util import *

import mail

app = Flask(__name__)
app.secret_key = os.urandom(24)

base_args = {'appName': "Broomball Referee Scheduler"}

# Returns a redirect page if neccessary, or None
def pagesCheck():
    if not session.get('username'):
        return redirect(url_for('login'))
    if not canViewPages():
        if unconfirmedUser():
            return redirect(url_for('unconfirmed'))
        else:
            return redirect(url_for('unactivated'))
    return None

# Non-authenticated pages

@app.route('/register')
def register():
    if session.get('username'):
        return redirect(url_for('registered'))
    return render_template('register.html', appName=base_args['appName'])

@app.route('/login')
def login():
    if session.get('username'):
        return redirect(url_for('.index'))
    return render_template('login.html', appName=base_args['appName'])

# Authenticated pages

@app.route('/')
def index():
    check = pagesCheck()
    if check:
        return check
    return render_template("index.html", username= session['username'], supervisor = supervisor(),
        head = headUser(), admin=adminUser(), page='index', **base_args)

@app.route('/admin')
def admin():
    check = pagesCheck()
    if check:
        return check
    # permissions check to see if the user is an admin
    if not adminUser():
        return redirect(url_for('.index'))
    return render_template("admin.html", username= session['username'], supervisor = supervisor(),
        head = headUser(), admin=adminUser(), page='admin', **base_args)

@app.route('/rankings')
def demranks():
    check = pagesCheck()
    if check:
        return check
    # permissions check to see if they can view overall rankings
    if (not adminUser()) and (not supervisor()) and (not headUser()):
        return redirect(url_for('.index'))
    return render_template("rankings.html", username= session['username'], supervisor = supervisor(),
        head = headUser(), admin=adminUser(), page='rankings', **base_args)

# Removed because we merged "committee" and "admin"

# @app.route('/committee')
# def committee():
#     check = pagesCheck()
#     if check:
#         return check
#     return render_template("committee.html", username= session['username'], supervisor = supervisor(),
#         head = headUser(), admin=adminUser(), page='committee', **base_args)

@app.route('/available')
def available():
    check = pagesCheck()
    if check:
        return check
    return render_template("avaiable.html", username= session['username'], supervisor = supervisor(),
        head = headUser(), admin=adminUser(), page='available', **base_args)

@app.route('/profile')
def profile():
    check = pagesCheck()
    if check:
        return check
    return render_template("profile.html", username=session['username'], supervisor = supervisor(),
        head = headUser(), admin=adminUser(), page='profile ' **base_args)

# Access restriction pages (i.e. pages a user is redirected to if they cannot normally log in)

@app.route('/unactivated')
def unactivated():
    if unactivatedUser():
        return render_template("unactivated.html", username=session['username'], **base_args)
    else:
        return redirect(url_for('.index'))

@app.route('/unconfirmed')
def unconfirmed():
    if unconfirmedUser():
        return render_template("unconfirmed.html", username=session['username'], **base_args)
    else:
        return redirect(url_for('.index'))

@app.route('/registered')
def registered():
    if unconfirmedUser():
        return render_template("registered.html", username=session['username'], **base_args)
    else:
        return redirect(url_for('.index'))

# Endpoint for confirming user emails

@app.route('/confirm/<code>')
def confirm(code=None):
    if code:
        result = verifyEmailCode(code)
        if result:
            session['username'] = result  
    return redirect(url_for('.index'))

# AJAX endpoints

@app.route('/ajax/dateinfo', methods=['GET'])
def dateinfo():
    if not request.args.get('date'):
        return "Error", 400
    else:
        if len(request.args['date']) != 8:
            return "Bad date", 400
        month = monthFromNumber(int(request.args['date'][2:4]))
        day = request.args['date'][:2]
        year = request.args['date'][4:8]
        date = "{} {}, {}".format(month, day, year)
        return render_template("info.html", date = date)

@app.route('/ajax/login', methods=['POST'])
def ajaxlogin():
    userName=request.form['username']
    password=request.form['password']
    if userExists(userName):
        if checkUserPassword(userName, password):
            session['username'] = getUsername(userName)
            return "Request OK", 200
    return "Error", 400

@app.route('/ajax/logout', methods=['POST'])
def logout():
    session.clear()
    return "Request OK", 200

@app.route('/ajax/registersubmit', methods=['POST'])
def registerSubmit():

    userName=request.form['mtuid']
    firstName=request.form['first-name']
    lastName=request.form['last-name']
    password=request.form['password']
    email = request.form['email']
    try:
        addCompleteUser(userName, firstName + ' ' + lastName, email, password)
    except DuplicateUser:
        return "User exists", 400
    except DuplicateEmail:
        return "Email exists", 400
    emailCode = generateEmailCode()
    setEmailCode(userName, emailCode)

    #dispatchConfirmEmail(email, emailCode)
    session['username'] = userName
    return "Request OK", 200 

# Error pages
@app.errorhandler(NotLoggedIn)
def errorNotLoggedIn(error):
    return redirect(url_for('.index'))


# main launcher method

if __name__== "__main__":
    app.run(debug=True)
