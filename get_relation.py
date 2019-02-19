import json
from typing import Dict
from flask_restful import Resource
from flask import Response, request
import MySQLdb as sql
# import MySQLdb.connections as connections
#import pymysql as sql


class get_relation(Resource):
    host: str = ""
    db: str = ""
    table_name: str = ""
    connection = None
    cursor = None

    def __init__(self, db_params, table_name="relation"):
        # def __init__(self, user='root', host='localhost', pw_='', db='derived', table_name="tmp_relation"):
        # the connection to the database only has to occur once therefor, it can occur in the initialization
        self.host = db_params['host']
        self.db = db_params['db']
        self.table_name = table_name
        self.connection = sql.connect(**db_params)
        self.cursor = self.connection.cursor()
        print("connected")

    def get(self):
        try:
            response_list: list(dict) = list()
            arguments: Dict[str] = request.args.to_dict()
            response_len: int = int(arguments["response_len"])
            conc: str = str(arguments["concept_id"])
            conc_str = f'\'{conc}\''
            #relation: int = int(arguments["relation"])
            #relation_str = f'\'{relation}\''
            exec = f'''
                                SELECT concept2, coeff, relation FROM {self.table_name} WHERE concept1 = {conc_str}'''

            self.cursor.execute(exec)
            relations = self.cursor.fetchall()

            if len(relations) < response_len:
                response_len = len(relations)

            for x in relations:
                response_dict: Dict[str, str] = {
                    "concept_id": x[0], "coeff": x[1], "relation": x[2]}
                response_list.append(response_dict)

            response_list = response_list[0:response_len]

            # turn the response_list in to a json obj
            response = Response(json.dumps(response_list), status=200,
                                mimetype='application/json')

            return response
        except Exception:
            return Response(json.dumps({"Error": "Invalid request"}), status=400,
                            mimetype='application/json')
