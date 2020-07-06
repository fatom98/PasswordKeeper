import dbm, base64

db = dbm.open("db/DB", "c")
login = "admin,admin"
enc = base64.b64encode(login.encode("utf-8"))
print(enc)
db["Login"] = enc
db.close()

