import json
from dataclasses import dataclass
from typing import List, Tuple, Dict, Tuple
from enum import Enum
from flask_restful import Resource, reqparse
from flask import Flask, Response, request
# from numpy import array
from operator import itemgetter
import MySQLdb as sql
import MySQLdb.connections as connections
#import pymysql as sql


class get_output(Resource):
    host: str = ""
    db: str = ""
    table_name: str = ""
    connection: connections.Connection = None
    cursor: connections.cursors.Cursor = None

    # def __init__(self, user='hiic', host='db01.healthcreek.org', pw_='greenes2018', db='derived', table_name="tmp"):
    def __init__(self, db_params, table_name="model_output"):
        # the connection to the database only has to occur once therefor, it can occur in the initialization
        self.host = db_params['host']
        self.db = db_params['db']
        self.table_name = table_name
        self.connection = sql.connect(**db_params)
        self.cursor = self.connection.cursor()
        print("connected")

    def get(self):
        arguments: Dict[str] = request.args.to_dict()
        num_rel_conc: int = int(arguments["num_rel_conc"])
        conc: str = str(arguments["concept_id"])
        conc_str = f'\'{conc}\''
        exec = f'''
                    SELECT * FROM {self.table_name} WHERE concept1 = {conc_str}'''

        self.cursor.execute(exec)
        #[concept1, concept2, f_importance, model_accuracy]
        relations = self.cursor.fetchall()

        if len(relations) < num_rel_conc:
            num_rel_conc = len(relations)

        list_vals = list([x for x in relations])
        list_vals.sort(key=itemgetter(2), reverse=True)
        list_vals = list_vals[0:num_rel_conc]

        response = json.dumps(list_vals)
        response = response.replace("\"", "")

        return response
