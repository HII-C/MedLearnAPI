import json
from flask_restful import Resource
from flask import Flask, Response
#import MySQLdb as sql
import pymysql as sql

class concept:
    def __init__(self, type, code, system, value, units):
        self.concept_type = type
        self.concept_code = code
        self.coding_system = system
        self.concept_value = value
        self.concept_units = units


class mapping:
    def __init__(self, hash1, hash2, relation, coeff_dict):
        self.concept1_hash = hash1
        self.concept2_hash = hash2
        self.relation = relation
        self.coeff_dict = coeff_dict

class get_mapppings(Resource):
    def __init__(self):
        self.user_ = 'hiic'  # i just put the connect and db access information because I was using a local database
        self.host_ = 'db01.healthcreek.org'
        self.pass_ = 'greenes2018'
        self.db_ = 'derived'

    def get(self, data_json):
        if data_json is not None:
            try:
                conn = sql.connect(user=self.user_, host=self.host_, db=self.db_, passwd=self.pass_)
                cursor = conn.cursor()
                subject_list = list()
                object_list = list()
                mapping_list = list()
                concept_dict = dict()
                json_list = list()
                #
                # Save JSON subject list
                # Save JSON object list
                #

                for n in subject_list:
                    for m in object_list:
                        where_query = f"""WHERE subject_code = \'{m.concept_code}\' AND object_code = \'{n.concept_code}\'"""
                        n = 1
                        query_row_string = f"""SELECT * FROM <Table_Name> {where_query} LIMIT {n}"""
                        print(query_row_string)
                        cursor.execute(query_row_string)
                        row = cursor.fetchall()

                        #initialize mapping object
                        temp = mapping(row[0], row[1], row[2], row[3])

                        #insert into mapping list
                        mapping_list.append(temp)

                        #contains all subjects and objects
                        concept_dict.update({n:m})

                        #return lists as JSON file
                        json_list.append(mapping_list, concept_dict)
                        response = Response(json.dumps(json_list), status=200, mimetype='application/json')
                        return response

            except:
                return json.dumps({})
