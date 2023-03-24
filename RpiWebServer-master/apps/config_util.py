import json,time
import mysql.connector

def createMysqlDbUsingConfigFile(filename):    
    with open(filename,"r") as f:
        conf=json.load(f)
    db = mysql.connector.connect(
        host=conf["host"],
        user=conf["user"],
        passwd=conf["passwd"],
        database=conf["db"]
        )
    return db
