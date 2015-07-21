#encoding: utf8

import pymongo

class MongoDB:
    def __init__(self,user,password,dbname, host='127.0.0.1',port=27017):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.conn = pymongo.Connection(self.host,int(self.port))
        self.db = self.conn[dbname]
        self.db.authenticate(self.user,self.password)

guandan_db = MongoDB(user='guandan', password='jiaojiao', dbname='guandan').db