import dbm

db = dbm.open("db/DB", "c")
db["Login"] = "admin,admin"
db.close()

