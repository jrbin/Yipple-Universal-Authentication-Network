import os
import json
import bcrypt
import uuid

from .db import getDB, queryDB, insertDB, updateDB

def registerUser(username, password):
    isSuccess = False

    # Check input lengths
    if len(username) == 0 or len(password) == 0:
        return (isSuccess, 'Invalid username or password length')

    # Check username uniqueness
    res = queryDB('SELECT * FROM users WHERE username = ?', [username], one=True)
    if res is not None:
        # User already exists inside the database
        return (isSuccess, 'The supplied username is already in use')
    else:
        # Registration successful
        # table creds bug fixed
        max_uid = queryDB('SELECT max(uid) as max_uid From users')[0][0]
        insertDB('INSERT INTO users (uid, username, passhash) values (?, ?, ?)', (int(max_uid) + 1, username, password))
        insertDB('INSERT INTO creds (uid, name, address, email, phonenum, funds) values (?, ?, ?, ?, ?, ?)', (int(max_uid) + 1, username, "NULL", "NULL", "NULL", 0))
        isSuccess = True
    return (isSuccess, 'Registration successful')

# Returns tuple of (success, session)
# Session is the username in this case.
def validateUser(username, password):
    isSuccess = False

    if len(username) == 0 or len(password) == 0:
        return (isSuccess, None)

    res = queryDB('SELECT * FROM users WHERE username = ?', [username], one=True)

    if res is not None:
        if res[2] == password:
            # Login succeeded
            isSuccess = True
            return (isSuccess, username)
        return (isSuccess, username)

    return (isSuccess, None)

def queryCreds(username):
    res_users = queryDB('SELECT * From users WHERE username=?', [username], one = True)
    if res_users is None:
        return (res_users)
    res_creds = queryDB('SELECT * From creds WHERE uid=?', [res_users[0]] ,one = True)
    return (res_creds)

def updateCreds(username, EditedName, EditedAddress, EditedEmail, EditedPhoneNum, EditedFunds):
    isSuccess = False
    #queryDB() is a tuple not an integer
    user_uid = queryDB('SELECT uid From users WHERE username=?', [username], one = True)[0]
    try:
        updateDB('''UPDATE creds SET name = ?, address= ?, email = ?, phonenum = ?, funds = ? WHERE uid = ?''', (EditedName, EditedAddress,EditedEmail, EditedPhoneNum, EditedFunds, user_uid))
        isSuccess = True
        return (isSuccess, 'Update successful!!')
    except:
        return(isSuccess, 'Update Failure')
    
    
