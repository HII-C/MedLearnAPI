import json
from dataclasses import dataclass
from typing import List, T, Dict
from enum import Enum
from flask_restful import Resource
from flask import Flask, Response, request
#import MySQLdb as sql
import pymysql as sql


class ConceptType(Enum):
    COND = "Condition"
    OBS = "Observation"
    TRT = "Treatment"


class EncodingSystem(Enum):
    LOINC = "LOINC"
    SNMD = "SNOMED"
    RX = "RxNorm"


class Relation(Enum):
    TRTS = "0"


@dataclass
class concept:
    concept_type: ConceptType
    concept_code: str = ""
    encoding_system: EncodingSystem
    concept_value: float = 0.0
    concept_units: str = ""

    def __init__(self, type_, code, system, value, units):
        self.concept_type = type_
        self.concept_code = code
        self.encoding_system = system
        self.concept_value = value
        self.concept_units = units


@dataclass
class mapping:
    concept1_hash: str = ""
    concept2_hash: str = ""
    relation: Relation
    coeff_dict: Dict = None

    def __init__(self, hash1, hash2, relation, coeff_dict):
        self.concept1_hash = hash1
        self.concept2_hash = hash2
        self.relation = relation
        self.coeff_dict = coeff_dict


class get_mapppings(Resource):
    def __init__(self):
        # i just put the connect and db access information because I was using a local database
        self.user_ = 'hiic'
        self.host_ = 'db01.healthcreek.org'
        self.pass_ = 'greenes2018'
        self.db_ = 'derived'

    # {'subj_list': [ ... ], 'obj_list': [ ... ]}
    def get(self):
        subj_list = request.args.get('subj_list')
        obj_list = request.args.get('obj_list')
        table_name = "tmp"

        if (len(subj_list) == 0) or (len(obj_list) == 0):
            raise ValueError("Data must have non-zero length")

        try:
            conn = sql.connect(
                user=self.user_, host=self.host_, db=self.db_, passwd=self.pass_)
            cursor = conn.cursor()
            mapping_list = list()
            concept_dict = dict()
            json_list = list()
            #
            # Save JSON subject list
            # Save JSON object list
            #

            for subj in subj_list:
                for obj in obj_list:
                    where_query = f"""WHERE subject_code = \'{subj.concept_code}\' AND object_code = \'{obj.concept_code}\'"""
                    subj = 1
                    query_row_string = f"""SELECT * FROM {table_name} {where_query} LIMIT {obj}"""
                    print(query_row_string)
                    cursor.execute(query_row_string)
                    row = cursor.fetchall()

                    # initialize mapping object
                    temp = mapping(row[0], row[1], row[2], row[3])

                    # insert into mapping list
                    mapping_list.append(temp)

                    # contains all subjects and objects
                    concept_dict.update({subj: obj})

                    # return lists as JSON file
                    json_list.append(mapping_list, concept_dict)
                    response = Response(json.dumps(
                        json_list), status=200, mimetype='application/json')
                    return response

        except:
            return json.dumps({})
