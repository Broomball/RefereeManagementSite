from flask import session

from db import *

import os
import binascii

class NotLoggedIn(Exception):
    pass

def monthFromNumber(n):
    if n == 1:
        return "January"
    elif n == 2:
        return "Feburary"
    elif n == 3:
        return "March"
    elif n == 4:
        return "April"
    elif n == 5:
        return "May"
    elif n == 6:
        return "June"
    elif n == 7:
        return "July"
    elif n == 8:
        return "August"
    elif n == 9:
        return "September"
    elif n == 10:
        return "October"
    elif n == 11:
        return "November"
    elif n == 12:
        return "December"

def canViewPages():
    print (unactivatedUser())
    print (unconfirmedUser())
    return (not unactivatedUser()) and (not unconfirmedUser())

# Returns true if this user is an admin level user, i.e. they are a chair or webadmin.
def adminUser():
    return __checkUserLevel__('ADMIN')

# Returns true if this user is a supervisor
def supervisor():
    return __checkUserLevel__('SUPERVISOR')

# Returns true if this user is a Head ref
def headUser():
    return __checkUserLevel__('HEADREF')

# Returns wether or not this user is an unactivated user i.e. they have not been confirmed by the head ref or chair yet
def unactivatedUser():
    return __checkUserLevel__('UNACTIVATED')

# Returns wether or not this user is an uncofirmed user i.e. they have not cofirmed their email yet
def unconfirmedUser():
    if not session.get('username'):
        raise NotLoggedIn()
    return not isUserConfirmed(session['username'])

def __checkUserLevel__(level):
    if not session.get('username'):
        raise NotLoggedIn()
    else:
        username = session.get('username')
        permissionLevel = getUserPerm(username)
        if permissionLevel == level:
            return True
        else:
            return False

# Returns a new, suitably random token to use as the code for email.
#      30 hexadecimal digits long
def generateEmailCode():
    return binascii.b2a_hex(os.urandom(15))