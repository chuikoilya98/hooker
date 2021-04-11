import json
from datetime import datetime,timedelta
import os.path as pt
import csv


class DataBase:

    def createUser(self:dict, userId:str) :
        filename = 'db/users.json'
        userData = json.load(open(pt.abspath(filename), mode="r"))
        if str(userId) in userData :
            pass
        else:
            userData[userId] = self
            with open(pt.abspath(filename), mode="w") as file :
                json.dump(userData, file, ensure_ascii=False)
                file.close()
    
    def createAction(self:str, name:str) :
        filename = 'db/actions.json'
        actionData = json.load(open(pt.abspath(filename), mode="r"))
        actionId = len(actionData) + 1
        actionData[actionId] = {
            "userId" : str(self),
            "actionTime" : str(datetime.now()) ,
        }
        with open(pt.abspath(filename), mode="w") as file :
            json.dump(actionData, file, ensure_ascii=False )
            file.close()

    def updateAction(self:str, funcName: str, userId:str) :    
        
        #TODO: добавить условие по проверке, брать с конца 

        if funcName == "getGuests" :

            filename = 'db/actions.json'
            actionData = json.load(open(pt.abspath(filename), mode="r"))
            for actionId in actionData :
                if actionData[actionId].get('userId') == str(userId):
                    actionData[actionId]['reserveTime'] = self

            with open(pt.abspath(filename), mode="w") as file :
                json.dump(actionData, file, ensure_ascii=False)
                file.close()

        elif funcName == "getHoldTime" :

            filename = 'db/actions.json'
            actionData = json.load(open(pt.abspath(filename), mode="r"))
            for actionId in actionData :
                if actionData[actionId].get('userId') == str(userId):
                    actionData[actionId]['guests'] = self

            with open(pt.abspath(filename), mode="w") as file :
                json.dump(actionData, file, ensure_ascii=False)
                file.close()

        elif funcName == "getPhone" :

            filename = 'db/actions.json'
            actionData = json.load(open(pt.abspath(filename), mode="r"))
            for actionId in actionData :
                if actionData[actionId].get('userId') == str(userId):
                    actionData[actionId]['longTime'] = self

            with open(pt.abspath(filename), mode="w") as file :
                json.dump(actionData, file, ensure_ascii=False)
                file.close()    

    def getInfoByUser(self:str) -> dict:
        
        filename = 'db/users.json'
        data = json.load(open(pt.abspath(filename), mode="r"))
        info = {}
        for user in data :
            if user == str(self) :
                info = data[user]
        
        return info

    def getUsersList(self:str) -> list :

        userList = []

        filename = 'db/users.json'
        data = json.load(open(pt.abspath(filename), mode="r"))

        for user in data:
            userList.append(user)

        return userList

    def getLastActionByUser(self:str) -> dict :
        
        filename = 'db/actions.json'
        actionData = json.load(open(pt.abspath(filename), mode="r"))
        info = {}
        timeDelta = datetime.now() - timedelta(minutes=5)

        for user in actionData :
            if actionData[user]['userId'] == str(self) and datetime.strptime(actionData[user]['actionTime'], '%Y-%m-%d %H:%M:%S.%f') > timeDelta  :
                info = actionData[user]
            else :
                pass
        return info

    def updatePlace(self) -> None :

        filename = 'db/contacts.csv'

        with open(pt.abspath(filename), mode='a', encoding='utf-8') as file :
            file_writer = csv.writer(file, delimiter= ';')
            file_writer.writerow(self)
