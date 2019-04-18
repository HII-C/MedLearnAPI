import json
from typing import Dict
from flask_restful import Resource
from flask import Response, request
from associations.util.db_util import DatabaseHandle
from flask_restful import Resource, reqparse
from associations.util.concept_util import ConceptType
from dataclasses import dataclass
from typing import List, Tuple
import MySQLdb as sql

@dataclass
class Concept:
    # setting the types of the attributes of Concept
    type_: ConceptType
    code: str

    # constructor for Concept
    def __init__(self, type_, code, system, value, units):
        self.type_ = type_
        self.code = code
        self.system = system
        self.value = value
        self.units = units

class get_obs_assoc(Resource):
    user: str = ""
    host: str = ""
    pw_: str = ""
    db: str = ""
    table_name: str = ""
    conn: sql.connections.Connection = None
    cursor: sql.cursors.Cursor = None

    rel_db: DatabaseHandle = None

    #def __init__(self, db_params, table_name="ModelStorage"):
    def __init__(self, user='root', host='localhost', pw_='Kikikabob2016!', db='knowledge', table_name="ModelStorage"):
        # the connection to the database only has to occur once therefor, it can occur in the initialization
        #self.host = db_params['host']
        #self.db = db_params['db']
        #self.table_name = table_name
        #self.rel_db = DatabaseHandle(**db_params)


        self.user = user
        self.pw_ = pw_
        self.db = db
        self.conn = sql.connect(user=self.user, host=self.host,
                                db=self.db, passwd=self.pw_)
        self.cursor = self.conn.cursor()
        self.table_name = table_name

    def get(self):
        db_name : str = "knowledge"
        ret_list : List[Tuple] = None
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('concept', type=str, action='append')
        req_parser.add_argument('obs_list', type=str, action='append')
        args = req_parser.parse_args()

        conc_str = args['concept'][0]
        raw_obs_list = args['obs_list']
        obs_list = list(map(lambda ob: ob.strip(), raw_obs_list[0].split(",")))
        #bs_list: List[Concept] = [
            #Concept(**json.loads(obs.replace("'", "\""))) for obs in raw_obs_list]

        if (len(obs_list) == 0):
            raise ValueError("Data must have non-zero length")

        # check if the table exists in the first place


        # tbl_query = f'''
        #             SELECT TABLE_NAME FROM {db_name}.TABLES WHERE TABLE_NAME = '{self.table_name}'
        #             AND AND TABLE_SCHEMA = '{db_name}'
        #             '''
        # self.rel_db.cursor.execute(tbl_query)
        # target_tables: Tuple[Tuple[str]] = self.rel_db.cursor.fetchall()
        # print(tbl_query)
        # num_target_tables: int = len(target_tables)

        # if the number of tables is 0 then a table must be created
        num_target_tables = 1
        if num_target_tables > 0:
            for obs in obs_list:
                tbl_query = f'''
                            SELECT Concept1, Concept2, Coefficient FROM {db_name}.{self.table_name} WHERE Concept1 = '{conc_str}' AND Concept2 = '{obs}'
                            '''
                self.cursor.execute(tbl_query) #add rel_db back
                ret_tables: Tuple[Tuple[str]] = self.cursor.fetchall() #add rel_db back
                if ret_list == None:
                    ret_list = [ret_tables]
                else:
                    ret_list.append(ret_tables)

        else:
            raise ValueError("Table is empty")

        print(ret_list)
        response = Response(json.dumps(ret_list), status=200,
                            mimetype='application/json')

        return response
