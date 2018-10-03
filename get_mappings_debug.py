import json
from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum
from flask_restful import Resource, reqparse
from flask import Flask, Response, request
from numpy import array
# import MySQLdb as sql
import pymysql as sql
import requests


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
class Concept:
    # setting the types of the attributes of Concept
    type_: ConceptType
    code: str
    system: EncodingSystem
    value: float
    units: str

    #constructor for Concept
    def __init__(self, type_, code, system, value, units):
        self.type_ = type_
        self.code = code
        self.system = system
        self.value = value
        self.units = units


@dataclass
class Mapping:
    # setting the types of the attributes of Concept
    c1_hash: str
    c2_hash: str
    relation: Relation
    coeff_dict: Dict

    # constructor for Concept
    def __init__(self, hash1, hash2, relation, coeff_dict):
        self.c1_hash = hash1
        self.c2_hash = hash2
        self.relation = relation
        self.coeff_dict = coeff_dict


class get_mapppings(Resource):
    user: str = ""
    host: str = ""
    pw_: str = ""
    db: str = ""
    table_name: str = ""
    coeff_dict_form: Dict[str, int] = {"gain": 3}
    conn: sql.connections.Connection = None
    cursor: sql.cursors.Cursor = None

    def __init__(self, user='root', pw_='star2222', db='derived', table_name="mappings"):
        # the connection to the database only has to occur once therefor, it can occur in the initialization
        self.user = user
        self.pw_ = pw_
        self.db = db
        self.conn = sql.connect(user=self.user, host=self.host,
                                db=self.db, passwd=self.pw_)
        self.cursor = self.conn.cursor()
        self.table_name = table_name
        print('connected')


    # Parameters of form: {'subj_list': [ ... ], 'obj_list': [ ... ]}
    def get(self):
        # the json objects are recieved via request
        req_parser = reqparse.RequestParser()
        req_parser.add_argument('subj_list', type = str, action = 'append')
        req_parser.add_argument('obj_list', type = str, action = 'append')
        args = req_parser.parse_args()
        raw_subj_list = args['subj_list']
        raw_obj_list = args['obj_list']
        subj_list = list()
        for x in raw_subj_list:
            json_accpetable_string = x.replace("'", "\"")
            json_x = json.loads(json_accpetable_string)
            temp_concept = Concept(**json_x)
            subj_list.append(temp_concept)
        print(len(subj_list))

        obj_list = list()
        for x in raw_obj_list:
            json_accpetable_string = x.replace("'", "\"")
            json_x = json.loads(json_accpetable_string)
            temp_concept = Concept(**json_x)
            obj_list.append(temp_concept)
        print(len(obj_list))


        # checks to see if the lists for the subj_list and the obj_list are zero
        if (len(raw_subj_list) == 0) or (len(raw_obj_list) == 0):
            raise ValueError("Data must have non-zero length")

        # the result will be ret_dict which is hash_to_mappings over hash_to_concept
        hash_to_mappings: Dict[str, dict()] = dict()
        hash_to_concept: Dict[str, json] = dict()
        ret_dict: Dict[str, dict] = dict()

        # creating a list of subj and obj by iterating the raw_subj_list and passing in the attributes as an argument to the constructor
        #subj_list: List[Concept] = [Concept(**subj) for subj in raw_subj_list]
        #obj_list: List[Concept] = [Concept(**obj) for obj in raw_obj_list]

        # create the hash to concept dict by utilizing the subj and obj hash as the key the the subj/obj as a value
        for conc in (subj_concept_list + obj_concept_list):
            hash_to_concept[hash(conc.code)] = (conc.__dict__)

        #created tuple of subj with its hash and obj with its hash (hash: 0, sub/obj: 1)
        subj_code_tup: tuple(tuple[hash, str]) = tuple(tuple([hash(subj.code), subj.code]) for subj in subj_concept_list)

        print(subj_code_tup)
        obj_code_tup: tuple(tuple[hash, str]) = tuple([tuple([hash(obj.code), obj.code]) for obj in obj_concept_list])
        print(obj_code_tup)

        for subj_code in subj_code_tup:
            mappings_list: list(dict) = list()
            for obj_code in obj_code_tup:
                print(subj_code[1])
                print(obj_code[1])
                where_query = f"""WHERE c1 = '{subj_code[1]}' AND c2 = '{obj_code[1]}'"""
                exec_str = f"""SELECT * FROM {self.table_name} {where_query}"""
                print(exec_str)

                self.cursor.execute(exec_str)
                # assuming: c1 | c2 | rela | gain | boost | bs
                row = self.cursor.fetchall()
                print(row)
                if (len(row) == 0):
                    next()
                else:

                    for x in row:
                        coefficient: Dict[str, int] = {"gain": x[3]}
                        tmp_mapping = Mapping(x[0], x[1], x[2], coefficient)
                        mappings_list.append(tmp_mapping.__dict__)



                    tmp = {"c1_hash": subj_code[0], "c2_hash": obj_code[0],
                           "relation": [x[2] for x in row], "coeff_dict": [x[3] for x in row]}

                    print(tmp)


            hash_to_mappings[subj_code[0]] = mappings_list

        ret_dict = dict({"hash_to_mappings": hash_to_mappings,
                    "hash_to_concept": hash_to_concept})

        #turn the ret_dict in to a json obj
        response = Response(json.dumps(ret_dict), status=200,
                            mimetype='application/json')
        return response
