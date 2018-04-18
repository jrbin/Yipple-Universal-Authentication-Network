from flask import Flask, render_template_string, request, render_template, \
    redirect, url_for, session



from . import app
from .. import models
import os

@app.route('/')
def home():
    username = None
    if 'username' in session:
        username = session['username']
    return render_template("home.html", username=username)

@app.route('/login', methods=["GET", "POST"])
def login():
    username = None
    password = None

    if request.method == "POST":
        # Implement me
#        print("***********")
#        print(username, password)

        if 'username' in request.form:
            username = request.form.get('username')

        if 'password' in request.form:
            password = request.form.get('password')

        if username is not None and password is not None:

            succ, sess = models.validateUser(username, password)

            if succ is True:
                session['username'] = request.form.get('username')
                # Craft the session
#                print(session)
                return redirect('/')
            else:
                return "Login request failed", 400
        else:

            return "login request received", 400

    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()

    return redirect(url_for("basic.home"))

@app.route('/register', methods=["GET", "POST"])
def register():
    username = None
    password = None
    result = False

    if request.method == "POST":
        if 'username' in request.form:
            username = request.form.get('username')

        if 'password' in request.form:
            password = request.form.get('password')

        if username is not None and password is not None:
            succ, status = models.registerUser(username, password)

            if succ is not False:
                return status, 200
            else:
                return status, 400
        return "User registration failed, either username or password is empty.", 400

    return render_template("register.html")

@app.route('/users/<account>',methods=['GET', 'POST'])
def users(account):
    username = account
    if username == 'me':
        username = session.get('username')
    #check if the username matches the session's username, if invalid username, return 403
    print(username, session.get('username'))
    if session.get('username') != 'admin':
        if username != session.get('username'):
            response = render_template("users.html"), 403
            return response
    # TODO: Implement the ability to edit and view credentials for
    # the creds database.
    if request.method == 'GET':
        # TODO: Display credentials if user belongs to current session, or if user is admin.
        # Deny access otherwise and display '404 not found' on the page
        if session.get('username') == "admin":
            userinfo = models.queryCreds(username)
        elif 'username' not in session:
            return '403 permission denied', 403
        else:
            userinfo = models.queryCreds(session['username'])
            print(userinfo)
        if userinfo is None:
            response = "404 not found" , 404
        else:
            response = render_template("users.html", uinfo = session, Name=userinfo[1], Address=userinfo[2], Email=userinfo[3], PhoneNum=userinfo[4], Funds=userinfo[5], username=username)

    else:
        # TODO: Update The Credentials
        # Two types of users can edit credentials for <account>
        # 1. Regular Users that have sessions == <account>
        if session.get('username') != 'admin':
            if request.form['username'] != username:
                return '403 permission denied', 403
            EditedName = request.form['name']
            EditedAddress = request.form['address']
            EditedEmail = request.form['email']
            EditedPhoneNum = request.form['phonenum']
            EditedFunds = int(request.form['funds'])
            updated_state, message = models.updateCreds(session['username'], EditedName, EditedAddress, EditedEmail, EditedPhoneNum, EditedFunds)
            print(updated_state,message)
            if updated_state == True:
            #update success, reload changed creds
                userinfo = models.queryCreds(session['username'])
                if userinfo is None:
                    response = render_template("users.html", uinfo = session, username= username)
                else:
                    response = render_template("users.html", uinfo = session, Name=userinfo[1], Address=userinfo[2], Email=userinfo[3], PhoneNum=userinfo[4], Funds=userinfo[5], username=username, update_msg = message)
            else:
                response = render_template("users.html", username = username, update_msg = message)
        # 2. Administrators.
        else:
            if request.form['username'] != username:
                return '403 permission denied', 403
            EditedName = request.form['name']
            EditedAddress = request.form['address']
            EditedEmail = request.form['email']
            EditedPhoneNum = request.form['phonenum']
            EditedFunds = int(request.form['funds'])
            updated_state, message = models.updateCreds(username, EditedName, EditedAddress, EditedEmail, EditedPhoneNum, EditedFunds)
#            print(updated_state,message)
            if updated_state == True:
            #update success, reload changed creds
                userinfo = models.queryCreds(username)
                if userinfo is None:
                    response = render_template("users.html", uinfo = session, username= username)
                else:
                    response = render_template("users.html", uinfo = session, Name=userinfo[1], Address=userinfo[2], Email=userinfo[3], PhoneNum=userinfo[4], Funds=userinfo[5], username=username, update_msg = message)
            else:
                response = render_template("users.html", username = username, update_msg = message)
    return response

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    response = None
    if request.method == 'GET':
        # TODO: Implement and secure the user administration control panel
        # The administration panel must distinguish between users that are administrators
        # as well as regular users.
        # It should also be able to search for a user via a get parameter called user.

        # search user by input account, first get the para from url
        searchedUser = request.args.get('user')
        # second query username from database and fetch the creds data
        userinfo = models.queryCreds(searchedUser)
        if session.get('username') == "admin":
            response = render_template("admin.html", user=searchedUser, userinfo = userinfo, admin = "admin")
        else:
            #response = render_template("admin.html", user=searchedUser, userinfo = userinfo)
            return '403 permission denied', 403

    elif request.method == 'POST':
        # TODO: You must also implement a post method in order update a searched users credentials.
        # It must return a page that denies a regular user
        # access and display '403 permission denied'.
        if session.get('username') == "admin":
            username = request.form['username']
            EditedName = request.form['name']
            EditedAddress = request.form['address']
            EditedEmail = request.form['email']
            EditedPhoneNum = request.form['phonenum']
            EditedFunds = int(request.form['funds'])
            updated_state, message = models.updateCreds(username, EditedName, EditedAddress, EditedEmail, EditedPhoneNum, EditedFunds)
            #reload data
            if updated_state == True:
                userinfo = models.queryCreds(username)
                response = render_template("admin.html", user=username, userinfo=userinfo, admin = "admin", message = message)
#        response = render_template("admin.html", user=searchedUser)


    return response




