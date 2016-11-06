import PDatabase

def connect():
    db = PDatabase.PDatabase("databasename", "username", "host", "password")
    if db.connected:
        return True
    else:
        return False
