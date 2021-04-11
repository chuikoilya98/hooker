import sqlite3
import os.path as pt

#filename = 'db/database.db'
#conn = sqlite3.connect(pt.abspath(filename))
#cursor = conn.cursor()

#cursor.execute("""CREATE TABLE guests (userId,name,phone)""")
#cursor.execute("""CREATE TABLE actions (userId,actionTime,reserveTime,guests,longTime)""")

#cursor.execute("""INSERT INTO guests VALUES ('331392389','Ilya','79995862639')""")
#conn.commit()

#sql = """UPDATE guests SET phone = '123' WHERE name = 'Ilya'"""

#sql = """SELECT * FROM guests WHERE userId = '331392389'"""



class DataBase :
    filename = 'db/database.db'
    conn = sqlite3.connect(pt.abspath(filename))
    cursor = conn.cursor()
    
    def createUser(self,userInfo:dict, userId:str) :
        filename = 'db/database.db'
        conn = sqlite3.connect(pt.abspath(filename))
        cursor = conn.cursor()
        
        request = f"""SELECT userId FROM guests WHERE userId = '{userId}'"""
        requestToDb = cursor.execute(request).fetchall()

        if len(requestToDb) == 0 :
            pass
        else:
            requestString = f"""INSERT INTO guests VALUES ('{userId}','{userInfo['name']},{userInfo['phone']}')"""
            setData = cursor.execute(requestString)
            conn.commit()

    #def createAction()

if __name__ == '__main__' :
    dbInfo = {
        "name" : 'dd',
        "phone" : 'phone'
    }
    test = DataBase()
    test.createUser(userInfo = dbInfo,userId='331392389')