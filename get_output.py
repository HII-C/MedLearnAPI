import json
from dataclasses import dataclass
from typing import List, Tuple, Dict, Tuple
from enum import Enum
from flask_restful import Resource, reqparse
from flask import Flask, Response, request
# from numpy import array
from operator import itemgetter
from associations.util.db_util import DatabaseHandle

class get_output(Resource):
    output_db: DatabaseHandle = None

    def __init__(self, db_params, table_name="model_output"):
        # the connection to the database only has to occur once therefor, it can occur in the initialization
        self.host = db_params['host']
        self.db = db_params['db']
        self.table_name = table_name
        self.output_db = DatabaseHandle(**db_params)

    def get(self):
        arguments: Dict[str] = request.args.to_dict()
        num_rel_conc: int = int(arguments["num_rel_conc"])
        conc: str = str(arguments["concept_id"])
        conc_str = f'\'{conc}\''
        exec = f'''
                    SELECT * FROM {self.table_name} WHERE concept1 = {conc_str}'''

        self.output_db.cursor.execute(exec)
        #[concept1, concept2, f_importance, model_accuracy]
        relations = self.output_db.cursor.fetchall()

        if len(relations) < num_rel_conc:
            num_rel_conc = len(relations)

        list_vals = list([x for x in relations])
        list_vals.sort(key=itemgetter(2), reverse=True)
        list_vals = list_vals[0:num_rel_conc]

        response = json.dumps(list_vals)
        response = response.replace("\"", "")

        return response
