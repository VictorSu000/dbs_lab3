import MySQLdb

db = None

def getDB():
    global db
    if db is None:
        db = MySQLdb.connect(host='localhost', port=3306, user='root', password='123456', db='bank', charset='utf8')
        print('mysql open success')
        db.autocommit(False)
        db.set_character_set('utf8')
    return db

def cleanUp():
    global db
    if db is not None:
        db.close()
