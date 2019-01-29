import json
from dataclasses import dataclass
from typing import List, Tuple, Dict, Tuple
from enum import Enum
from flask_restful import Resource, reqparse
from flask import Flask, Response, request
from numpy import array
from operator import itemgetter
import MySQLdb as sql
import MySQLdb.connections as connections
#import pymysql as sql

class get_assoc(Resource):
    user: str = ""
    host: str = ""
    pw_: str = ""
    db: str = ""
    table_name: str = ""
    connection: connections.Connection = None
    cursor: connections.cursors.Cursor = None

    def __init__(self, user='hiic', host='db01.healthcreek.org', pw_='greenes2018', db='derived', table_name="tmp"):
    #def __init__(self, user='root', host='localhost', pw_='', db='derived', table_name="tmp_assoc"):
        # the connection to the database only has to occur once therefor, it can occur in the initialization
        self.user = user
        self.host = host
        self.pw_ = pw_
        self.db = db
        self.table_name = table_name
        print("not_connected")
        self.connection = sql.connect(user=self.user, host=self.host,
                                db=self.db, passwd=self.pw_)
        self.cursor = self.connection.cursor()
        print("connected")


    def get(self):
        response_list: list(dict) = list()
        arguments: Dict[str] = request.args.to_dict()
        response_len:int = int(arguments["response_len"])
        conc:str = str(arguments["concept_id"])
        conc_str = f'\'{conc}\''
        exec = f'''
                    SELECT concept2, coeff FROM {self.table_name} WHERE concept1 = {conc_str}'''


        self.cursor.execute(exec)
        relations = self.cursor.fetchall()

        if len(relations) < response_len:
            response_len = len(relations)

        for x in relations:
            response_dict: Dict[str, str] = {"concept_id" : x[0], "coeff" : x[1]}
            response_list.append(response_dict)

        response_list = response_list[0:response_len]

        # turn the ret_dict in to a json obj
        response = Response(json.dumps(response_list), status=200,
                            mimetype='application/json')

        return response