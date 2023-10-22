import oracledb
import getpass

user = "hlee3"
dsn = "F1EGPPO9QB4YI0KX_high"
pw = "DlGkS!2#4%6&8(0"
wallet_pw = "DlGkS!2#4%6&8(0"

con = oracledb.connect(user=user, password=pw, dsn=dsn, config_dir=r"./Wallet_F1EGPPO9QB4YI0KX/", wallet_password=wallet_pw)

print("Database version:", con.version)
