import json
from typing import Dict
from flask_restful import Resource
from flask import Response, request
from associations.util.db_util import DatabaseHandle



class get_assoc(Resource):
    assoc_db: DatabaseHandle = None

    def __init__(self, db_params, table_name="assoc"):
        # def __init__(self, user='root', host='localhost', pw_='', db='derived', table_name="tmp_assoc"):
        # the connection to the database only has to occur once therefor, it can occur in the initialization
        self.host = db_params['host']
        self.db = db_params['db']
        self.table_name = table_name
        self.assoc_db = DatabaseHandle(**db_params)

    def get(self):
        response_list: list(dict) = list()
        arguments: Dict[str] = request.args.to_dict()
        response_len: int = int(arguments["response_len"])
        conc: str = str(arguments["concept_id"])
        conc_str = f'\'{conc}\''
        exec = f'''
                    SELECT concept2, coeff FROM {self.table_name} WHERE concept1 = {conc_str}'''

        self.assoc_db.cursor.execute(exec)
        relations = self.assoc_db.cursor.fetchall()

        if len(relations) < response_len:
            response_len = len(relations)

        for x in relations:
            response_dict: Dict[str, str] = {"concept_id": x[0], "coeff": x[1]}
            response_list.append(response_dict)

        response_list = response_list[0:response_len]

        # turn the response_list in to a json obj
        response = Response(json.dumps(response_list), status=200,
                            mimetype='application/json')

        return response
