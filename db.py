import pymysql
import time
from passlib.hash import bcrypt

#connects to Local  MySQL DB
#Set up DB using DBsetup Directions
#userSchema, rankSchema, shiftSchema

#TO-DO: Get All of the ranks by Group from "rank" Table
#TO-DO: Shift Schema think out

class DuplicateEmail( Exception ):
    pass
class DuplicateUser( Exception ):
    pass
class UserDoesntExist( Exception ):
    pass
class SuperUserDoesntExist( Exception ):
    pass
class InvalidEmail( Exception ):
    pass
class InvalidRank( Exception ):
    pass
class IdDoesntExist( Exception ):
    pass
class InvalidDate( Exception ):
    pass
class InvalidShiftNum( Exception ):
    pass
class InvalidRink( Exception ):
    pass
class notBoolean( Exception ):
    pass
class sameUser( Exception ):
    pass 

#Global connector and db 
db = pymysql.connect( host = '71.13.210.36', port = 3306, user = 'bb', passwd = 'FightQueen77', db = 'Broomball' ) 
#db = pymysql.connect( host = '127.0.0.1', port = 3306, user = 'bb', passwd = 'FightQueen77', db = 'Broomball' ) 
cursor = db.cursor()

#userSchema
#Checks if user exists and if email exists
def userExists( username ):
    sql = ("SELECT username FROM user WHERE username=%s;", (username,) )
    if not executeGetOne( sql ): 
        return False
    else:  
        return True

# this allows us to match usernames exactly
def getUsername( username ):
    sql = ("SELECT username FROM user WHERE username=%s", (username,))
    return executeGetOne( sql )
                       
def emailExists( email ):
    sql =  ("SELECT email  FROM user WHERE email=%s;", (email,) )
    if not executeGetOne( sql ):
        return False
    else:
        return True

#Adds a password, no checking is involved 
def setUserPassword ( username, password ):
    myHash = bcrypt.encrypt( password )
    sql = ("UPDATE user SET password=%s WHERE username=%s;", (myHash, username) )
    return executeSet( sql )

#Checks to see if the given password matches the existing one
#Returns true if the password is correct
def checkUserPassword ( username, password ):
    sql = ("SELECT password FROM user WHERE username=%s;",(username,))

    myHash = executeGetOne( sql )
    return bcrypt.verify( password, myHash )

#Adders for "user" Table
def addUser ( username ):
    if userExists( username ):
        raise DuplicateUser()
    else:
        sql = ("INSERT INTO user (username) VALUES (%s);",(username,))
        return executeSet( sql )

def addCompleteUser ( username, fullName, email, password, rank = 0, perm = 'UNACTIVATED' ):
    if emailExists(email):
        raise DuplicateEmail()
    if userExists(username):
        raise DuplicateUser()
    addUser( username )

    setUserFullName( username, fullName )
    setUserPerm( username, perm )
    setUserPassword( username, password )
    setUserEmail( username, email )
    return

#Setters for "user" Table
def setUserFullName ( username, fullName ):
    if not userExists( username ):
        raise UserDoesntExist()
    sql = ("UPDATE user SET fullName=%s WHERE username=%s;",(fullName, username))
    return executeSet( sql )
    
def setUserPerm ( username, perm ):
    if not userExists( username ):
        raise UserDoesntExist()
    sql = ("UPDATE user SET permissionLevel=%s WHERE username=%s;",(perm, username))
    return executeSet( sql )

def confirmEmail( username ):
    if not userExists( username ):
        raise UserDoesntExist()
    sql = ("UPDATE user SET confirmed=true WHERE username=%s", username)
    return executeSet( sql )

def isUserConfirmed( username ):
    if not userExists( username ):
        raise UserDoesntExist()
    sql = ("SELECT confirmed FROM user WHERE username=%s and confirmed=true", username)
    result = executeGetRow( sql )
    if result:
        return True
    else:
        return False

def setUserEmail ( username, email ):
    if not userExists( username ):
        raise UserDoesntExist()
    if validEmail( email ):
        sql = ("UPDATE user SET email=%s WHERE username=%s;",(email, username))
        return executeSet( sql )

def validEmail( email ): 
    if emailExists( email ):
        raise DuplicateEmail()
    print(email)
    parts = email.split( '@' )
    if len( parts ) == 2 and len( parts[0] ) != 0 and parts[1] == 'mtu.edu':
        return True
    else:
        raise InvalidEmail()

def setUserRank ( username ):
    if not userExists( username ):
        raise UserDoesntExist()
    sql = ("SELECT AVG(rank) FROM rank WHERE refUser=%s;",(username,))
    rank = executeGetOne( sql )
    sql = ("UPDATE user SET rank=%s WHERE username=%s;",(rank, username))
    return executeSet( sql )

#Getters for "user" Table
def getUserFullName ( username ):
    if not userExists( username ):
        raise UserDoesntExist()
    sql = ("SELECT fullName FROM user WHERE username=%s;",(username,))
    return executeGetOne( sql )

def getUserPerm ( username ):
    if not userExists( username ):
        raise UserDoesntExist()
    sql = ("SELECT permissionLevel FROM user WHERE username=%s;",username)
    return executeGetOne( sql )

def getUserEmail ( username ):
    if not userExists( username ):
        raise UserDoesntExist()
    sql = ("SELECT email FROM user WHERE username=%s;",username)
    return executeGetOne( sql )

def getUserRank ( username ):
    if not userExists( username ):
        raise UserDoesntExist()
    sql = ("SELECT rank FROM user WHERE username=%s;",username)
    return executeGetOne( sql )

#Delete user, use with caution and/or testing. There is no record to what was delted or by who
def deleteUser ( username ): 
    if not userExists( username ):
        raise UserDoesntExist()
    sql = ("DELETE FROM user WHERE username = %s;",username)
    return executeSet( sql )


#rankSchema
def rankIDExists( id ):
    sql = ("SELECT id FROM rank WHERE id = %s;", id )
    if not executeGetRow( sql ): 
        return False
    else:  
        return True

def validDate( date ):
    parts = date.split( '-' )
    if len( parts ) == 3 and len( parts[0] ) == 4 and len( parts[1] ) == 2 and len( parts[2] ) == 2:
        return True
    else:
        raise InvalidDate()

#Adder for "rank" Table
#Automatically Today's Date by default
def addRankInstance ( refUser, superUser, rank, date = time.strftime("%Y-%m-%d") ):
    if not userExists( refUser ):
        raise UserDoesntExist()        
    if not userExists( superUser ):
        raise SuperUserDoesntExist()
    if rank < 0 or rank > 10:
        raise InvalidRank()
    if validDate( date ):
        sql = ("INSERT INTO rank(refUser, superUser, rank, date) VALUES(%s, %s, %s, %s);", (refUser, superUser, rank, date))
        executeSet( sql )
        setUserRank( refUser )
        return 

#Getters for "rank" table
def getRankRef ( id ):
    if not rankIDExists( id ):
        raise IdDoesntExist()
    sql = ("SELECT refUser FROM rank WHERE id=%s;", id)
    return executeGetOne( sql )

def getRankSuper ( id ):
    if not rankIDExists( id ):
        raise IdDoesntExist()
    sql = ("SELECT superUser FROM rank WHERE id=%s;",id)
    return executeGetOne( sql )

def getRankRank ( id ):
    if not rankIDExists( id ):
        raise IdDoesntExist()
    sql = ("SELECT rank FROM rank WHERE id=%s;",id)
    return executeGetOne( sql )

def getRankDate ( id ):
    if not rankIDExists( id ):
        raise IdDoesntExist()
    sql = ("SELECT date FROM rank WHERE id=%s;",id)
    return executeGetOne( sql )


#Setters for "rank" table
def setRankRef ( id, refUser ):
    if not userExists( refUser ):
        raise UserDoesntExist()        
    if not rankIDExists( id ):
        raise IdDoesntExist()
    oldRef = getRankRef( id )
    sql = ("UPDATE rank SET refUser=%s WHERE id=%s;", (refUser, id ))
    executeSet( sql )
    setUserRank( oldRef )
    setUserRank( refUser )
    return 

def setRankSuper ( id, superUser ): 
    if not userExists( superUser ):
        raise SuperUserDoesntExist()
    if not rankIDExists( id ):
        raise IdDoesntExist()
    sql = ("UPDATE rank SET superUser=%s WHERE id=%s;", (superUser, id) )
    return executeSet( sql )

def setRankRank ( id, rank ): 
    if rank < 0 or rank > 10:
        raise InvalidRank()
    if not rankIDExists( id ):
        raise IdDoesntExist()
    sql = ("UPDATE rank SET rank=%s WHERE id=%s;", (rank, id) )
    executeSet( sql )
    setUserRank( getRankRef( id ) )
    return 

def setRankDate ( id, date ): 
    if not rankIDExists( id ):
        raise IdDoesntExist()
    if validDate( date ):
        sql = ("UPDATE rank SET date=%s WHERE id=%s;", (date, id ))
        return executeSet( sql )

def getAllRankUser( refUser ):
    return

def getAllRankSuper( superUser ):
    return

def getAllRankDate( date ):
    return 

#refShiftSchema
def refShiftIDExists( id ):
    sql = ("SELECT id FROM refShift WHERE id = %s;", id )
    if not executeGetRow( sql ): 
        raise IdDoesntExist()
    else:  
        return True

#Adder for "shift" Table
def addRefShiftInstance ( date, shiftNum, rink, refUser1, refUser2, canceled = 0, isOpen = 1 ):
    if not userExists( refUser1 ) and not userExists( refUser2 ):
        raise UserDoesntExist() 
    if shiftNum < 0 or shiftNum > 4:
            raise InvalidShiftNum()
    if rink != "SILVER" or rink != "GOLD" or rink != "BLACK":
        raise InvalidRink() 
    if validDate( date ):
        sql = ("INSERT INTO shift( date, shiftNum, rink, refUser1, refUser2, canceled, isOpen ) VALUES( %s, %s, %s, %s, %s, %s, %s );", ( date, shiftNum, rink, refUser1, refUser2, canceled, isOpen ) )
        return executeSet( sql )

#Getters for "shift" table
def getRefShiftDate ( id ):
    if refShiftIDExists( id ):
        sql = ("SELECT date FROM refShift WHERE id=%s;", id)
        return executeGetOne( sql )

def getRefShiftNum ( id ):
    if refShiftIDExists( id ):
        sql = ("SELECT shiftNum FROM refShift WHERE id=%s;", id)
        return executeGetOne( sql )

def getRefShiftRink ( id ):
    if refShiftIDExists( id ):
        sql = ("SELECT rink FROM refShift WHERE id=%s;", id)
        return executeGetOne( sql )

def getRefShiftUserOne ( id ):
    if refShiftIDExists( id ):
        sql = ("SELECT refUser1 FROM refShift WHERE id=%s;", id)
        return executeGetOne( sql )

def getRefShiftUserTwo ( id ):
    if refShiftIDExists( id ):
        sql = ("SELECT refUser2 FROM refShift WHERE id=%s;", id)
        return executeGetOne( sql )

def getRefShiftCanc ( id ):
    if refShiftIDExists( id ):
        sql = ("SELECT canceled FROM refShift WHERE id=%s;", id)
        return executeGetOne( sql )

def getRefShiftOpen ( id ):
    if refShiftIDExists( id ):
        sql = ("SELECT isOpen FROM refShift WHERE id=%s;", id)
        return executeGetOne( sql )

#Setters for "shift" table
def setRefShiftUser ( id, oldUser, newUser ):
    if not userExists( oldUser ):
        raise UserDoesntExist()  
    if not userExists( newUser ):
        raise UserDoesntExist()       
    if refShiftIDExists( id ):
        sql = ("SELECT refUser1 FROM refShift WHERE id=%s;", id)        
        if executeGetOne( sql ) == oldUser:
            sql = ("SELECT refUser2 FROM refShift WHERE id=%s;", id)
            if executeGetOne( sql ) == newUser:
                raise sameUser()
            else:             
                sql = ("UPDATE refShift SET refUser1=%s WHERE id=%s;", (newUser, id ))
                executeSet( sql )
        else:
            sql = ("SELECT refUser1 FROM refShift WHERE id=%s;", id)
            if executeGetOne( sql ) == newUser:
                raise sameUser()
            else:             
                sql = ("UPDATE refShift SET refUser2=%s WHERE id=%s;", (newUser, id ))
                executeSet( sql )
    return 

def setRefShiftCanc ( id, canc ):
    if canc.lower() != "true" or canc.lower() != "false":
        raise notBoolean()        
    if refShiftIDExists( id ):
        sql = ("UPDATE refShift SET canceled=%s WHERE id=%s;", (canc, id ))
        executeSet( sql )
        sql = ( "SELECT refUser1, refUser2 FROM refShift WHERE id=%s;", ( id )) 
        return executeGetRow( sql )

def setRefShiftOpen ( id, isOpen ):
    if isOpen.lower() != "true" or isOpen.lower() != "false":
        raise notBoolean()        
    if refShiftIDExists( id ):
        sql = ("UPDATE refShift SET isOpen=%s WHERE id=%s;", ( isOpen, id ))
        executeSet( sql )
        return


def setEmailCode( username, code ):
    sql = ("INSERT INTO emailCode VALUES (%s, %s) ON DUPLICATE KEY UPDATE code=%s", (username, code, code))
    return executeSet(sql)

def verifyEmailCode( code ):
    sql = ("SELECT * FROM emailCode WHERE code=%s", code)
    result = executeGetRow(sql)
    if result:
        sql = ("DELETE FROM emailCode WHERE username=%s", result[0])
        executeSet(sql)
        return result[0]
    else:
        return False

# Helper methods for Everything
def executeSet( sql ):
    global cursor
    stayingAlive()
    try:
        cursor.execute( *sql )
        db.commit()
    except pymysql.InternalError as e:
        raise e

def executeGetOne( sql ):
    global cursor
    stayingAlive()
    try: 
        cursor.execute( *sql )
        result = cursor.fetchone()[0]
    except TypeError:
        result = None
        pass 
    except pymysql.InternalError as e: 
        raise e
    return result;

def executeGetRow( sql ):
    global cursor
    stayingAlive()
    try: 
        cursor.execute( *sql )
        result = cursor.fetchall()
    except TypeError:
        result = None
        pass
    except pymysql.InternalError as e:
        raise e
    return result;

def stayingAlive():
    global db
    global cursor 
    try:
        db.commit()
        cursor.close()
        cursor = db.cursor()
    except pymysql.InternalError as e:
        raise e
