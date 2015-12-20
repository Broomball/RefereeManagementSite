from db import *

if userExists( 'test1' ):
    deleteUser( 'test1' )
if userExists( 'test2' ):
    deleteUser( 'test2' )
if userExists( 'test3' ):
    deleteUser( 'test3' )
    

addUser('test1')
setUserFullName('test1', 'full name1') 
setUserPerm('test1', 'perm1' ) 
setUserEmail('test1', 'test1@mtu.edu') 
setUserPassword('test1', 'hunter1' ) 
print("Added user test1 individually!")
print("test1 get Calls")
print("Full Name:       ", getUserFullName('test1') )
print("Permissions:     ", getUserPerm('test1') )
print("Email:           ", getUserEmail('test1') )
print("Rank:            ", getUserRank('test1') )
print("Password Check:  ", checkUserPassword('test1', 'hunter1'), " =     True" )

addCompleteUser( 'test2', 'full name2', 'test2@mtu.edu', 'hunter2' ) 
addCompleteUser( 'test3', 'full name3', 'test3@mtu.edu', 'hunter3' ) 

print("Added user test2 in a group!")
print("test2 get Calls")
print("Full Name:       ", getUserFullName('test2') )
print("Permissions:     ", getUserPerm('test2') )
print("Email:           ", getUserEmail('test2') )
print("Rank:            ", getUserRank('test2') )
print("Password Check:  ", checkUserPassword('test2', 'hunter1'), "=    False" )
print("Password Check:  ", checkUserPassword('test2', 'hunter2'), " =    True" )

print("")
print("")

print("test1 is refUser and test2 is superUser")
addRankInstance( 'test1', 'test2', 4) 
print("Rank of test1:   ", getUserRank('test1') )
addRankInstance( 'test1', 'test2', 6) 
print("Rank of test1:   ", getUserRank('test1') )
print("")
print("Ref of id 2:     ", getRankRef(2) )
print("Super of id 2:   ", getRankSuper(2) )
print("Rank of id 2:    ", getRankRank(2) )
print("Date of id 2:    ", getRankDate(2) )
print(" ")

setRankRef(  2, 'test3')
setRankSuper( 2, 'test3')
setRankRank( 2, 10 )
setRankDate( 2, '2015-01-01' )

print("Rank of test1:   ", getUserRank('test1') )
print("Ref of id 2:     ", getRankRef(2) )
print("Super of id 2:   ", getRankSuper(2) )
print("Rank of id 2:    ", getRankRank(2) )
print("Date of id 2:    ", getRankDate(2) )

