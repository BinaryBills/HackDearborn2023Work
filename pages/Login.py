import oracledb
import getpass

user = "hlee3"
dsn = "ocidbdemo_high"
pw = getpass.getpass(f"Enter password for {user}: ")
wallet_pw = getpass.getpass("Enter wallet password for the database: ")

con = oracledb.connect(user=user, password=pw, dsn=dsn, config_dir=r"./Wallet_RT3XMTA51QNCGH1G/", wallet_password=wallet_pw)

print("Database version:", con.version)
