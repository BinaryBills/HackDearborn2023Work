import oracledb
import getpass
import os


user = "ADMIN"
dsn = "f1egppo9qb4yi0kx_medium"
pw = "DlGkS!2#4%6&8(0"
wallet_pw = "DlGkS!2#4%6&8(0"

con = oracledb.connect(user=user, password=pw, dsn=dsn, config_dir=r"./Wallet_F1EGPPO9QB4YI0KX/", wallet_password=wallet_pw)

print("Database version:", con.version)





def verifyEmail(email: str) -> bool:
    # Attempt connection to Oracle database.
    try:
        connection = oracledb.connect(dsn = dsn)
        print("Connected to database")
    except:
        print("Was not able to connect to the database.")
        return False
    
    cur = connection.cursor()
    
    try:
        cur.execute("select * from users where email = :email", [email])
        count = cur.fetchall()
        if (len(count) == 0):
            print("Unique email.")
            return True
        return False
    except:
        print("Could not execute query to find a user with given email.")
        return False
    

def addUser(email: str, password: str, pr1: str, pr2: int, pr3: str, r1: str, r2: str, r3: str) -> str:

    # Attempt connection to Oracle database.
    try:
        connection = oracledb.connect(dsn = dsn)
        print("Connected to database")

    except:
        print("Was not able to connect to the database.")
    cur = connection.cursor()
    try:
        cur.execute("insert into users values (:email, :password, :pr1, :pr2, :pr3, :r1, :r2, :r3)", [email, password, pr1, pr2, pr3, r1, r2, r3])
        connection.commit()
        output = "Added user into database"
    except:
        output = "Unsuccessful"    
    connection.close()
    return output
'''
Adds business to db
'''


    
def deleteUser(email: str) -> None:

    try:
        connection = oracledb.connect(dsn = dsn)
        print("Connected to database")
    except:
        print("Was not able to connect to database")
    cur = connection.cursor()
    try:
        cur.execute("delete from users where email = :email", [email])
        connection.commit()
        output = "Deleted ownsbusiness from database."
    except:
        output = "Unable to deleted ownsbusiness from database"
    try:
        cur.execute("delete from users where email = :email", [email])
        connection.commit()
        output = "Deleted user from database."
    except:
        output = "Unable to deleted user from database"
    connection.close()
    return output

    try:
        connection = oracledb.connect(dsn = dsn)
        print("Connected to database")
    except:
        print("Was not able to connect to database")
    cur = connection.cursor()
    try:
        cur.execute("delete from items where bid = :bid", [id])
        connection.commit()
        output = "Deleted item from database."
    except:
        output = "Unable to deleted ownsbusiness from database"
    try:
        cur.execute("delete from ownsbusiness where bid = :bid", [id])
        connection.commit()
        output = "Deleted ownsbusiness from database."
    except:
        output = "Unable to delete ownsbusiness from database"
    try:
        cur.execute("delete from business where id = :id", [id])
        connection.commit()
        output = "Deleted user from database."
    except:
        output = "Unable to delete business from database"
    connection.close()
    return output

def verifyLogin(email: str, password: str):

    # Attempt connection to Oracle db.
    try: 
        connection = oracledb.connect(dsn=dsn)
        print("Connected to database")
    except:
        print("Was not able to connect to database")
        print(oracledb.connect(dsn=dsn))
    cur = connection.cursor()
    # Check if the user even exists
    cur.execute("select * from users where email = :email", [email])
    number = cur.fetchall() 
    if (len(number) != 1):
        print("User with email does not exist")
        return None
    
    cur.execute("select * from users where email = :email and password = :password", [email, password])
    user = cur.fetchall()
    if (len(user) != 1):
        print("Password does not match, try again")
        return None
    print("Successfully verified user")
    return user

def updateUserPassword(email: str, password: str) -> str:
    # Attempt connection to Oracle database.
    try:
        connection = oracledb.connect(dsn = dsn)
        print("Connected to database")
    except:
        print("Was not able to connect to database")
    cur = connection.cursor()
    try:
        cur.execute("update user set password = :password where email = :email", [password, email])
        connection.commit()
    except:
        print("Could not update participants.")
    connection.close()

    try:
        connection = oracledb.connect(dsn = dsn)
        print("Connected to database")
    except:
        print("Was not able to connect to database")

    cur = connection.cursor()

    cur.execute("select * from items where name = :name and bid = :bid", [name, bid])
    items = cur.fetchall() 

    if (len(items) == 0):
        return "Item not found"

    try:
        cur.execute("delete from items where name = :name and bid = :bid", [name, bid])
        connection.commit()
        output = "Deleted item from database."
    except:
        output = "Unable to delete items from database"

    connection.close()
    return output

