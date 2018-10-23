import json
from dataclasses import dataclass
from typing import List, Tuple, Dict, Tuple
from enum import Enum
from flask_restful import Resource, reqparse
from flask import Flask, Response, request
from numpy import array
from operator import itemgetter
import MySQLdb as sql
#import pymysql as sql

class get_output(Resource):
    user: str = ""
    host: str = ""
    pw_: str = ""
    db: str = ""
    table_name: str = ""
    conn: sql.connections.Connection = None
    cursor: sql.cursors.Cursor = None

    def __init__(self, user='hiic', host='db01.healthcreek.org', pw_='greenes2018', db='derived', table_name="tmp"):
        # the connection to the database only has to occur once therefor, it can occur in the initialization
        self.user = user
        self.host = host
        self.pw_ = pw_
        self.db = db
        self.conn = sql.connect(user=self.user, host=self.host,
                                db=self.db, passwd=self.pw_)
        self.cursor = self.conn.cursor()
        self.table_name = table_name


    def get(self):
        arguments: Dict[str] = request.args.to_dict()
        num_rel_conc:int = int(arguments["num_rel_conc"])
        conc:str = str(arguments["conc"])
        exec = f'''
                    SELECT * FROM {self.table_name}
                        WHERE concept1 =  '{conc}' '''
        self.cursor.execute(exec)
        #[concept1, concept2, f_importance, model_accuracy]
        relations = self.cursor.fetchall()

        if len(relations) < num_rel_conc:
            num_rel_conc = len(relations)

        list_vals = list([x for x in relations])
        list_vals.sort(key=itemgetter(2), reverse = True)
        list_vals = list_vals[0:num_rel_conc]

        response = json.dumps(list_vals)

        return response
