import json
from dataclasses import dataclass
from typing import List, T, Dict, Tuple
from enum import Enum
from flask_restful import Resource
from flask import Flask, Response, request
from numpy import array
# import MySQLdb as sql
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
class Concept:
    type_: ConceptType
    code: str = ""
    system: EncodingSystem
    value: float = 0.0
    units: str = ""

    def __init__(self, type_, code, system, value, units):
        self.type_ = type_
        self.code = code
        self.system = system
        self.value = value
        self.units = units


@dataclass
class Mapping:
    c1_hash: str = ""
    c2_hash: str = ""
    relation: Relation
    coeff_dict: Dict = None

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

    def __init__(self, user='hiic', host='db01.healthcreek.org', pw_='greenes2018', db='derived', table_name="tmp"):
        # i just put the connect and db access information because I was using a local database
        self.user = user
        self.host = host
        self.pw_ = pw_
        self.db = db
        self.conn = sql.connect(user=self.user, host=self.host,
                                db=self.db, passwd=self.pw_)
        self.cursor = self.conn.cursor()
        self.table_name = table_name

    # Parameters of form: {'subj_list': [ ... ], 'obj_list': [ ... ]}
    def get(self):
        raw_subj_list = request.args['subj_list']
        raw_obj_list = request.args['obj_list']

        if (len(raw_subj_list) == 0) or (len(raw_obj_list) == 0):
            raise ValueError("Data must have non-zero length")

        hash_to_mappings: Dict[str, List[Mapping]] = dict()
        hash_to_concept: Dict[str, Concept] = dict()
        ret_dict: Dict[str, dict] = dict()

        subj_list: List[Concept] = [Concept(**subj) for subj in raw_subj_list]
        obj_list: List[Concept] = [Concept(**obj) for obj in raw_obj_list]

        for conc in (subj_list + obj_list):
            hash_to_concept[hash(conc)] = conc

        subj_code_tup: Tuple[Tuple[str, str]] = tuple(
            [tuple([hash(subj), subj.code]) for subj in subj_list])
        obj_code_tup = tuple([[hash(obj), obj.code] for obj in obj_list])

        for subj_code in subj_code_tup:
            for obj_code in obj_code_tup:
                where_query = f"""WHERE subject_code = '{subj_code[1]}' AND object_code in {obj_code_tup[1]}"""
                exec_str = f"""SELECT * FROM {self.table_name} {where_query}"""
                print(exec_str)

                self.cursor.execute(exec_str)
                # assuming: c1 | c2 | rela | gain | boost | bs
                row = self.cursor.fetchall()

                coeff_dict = dict()
                for k, v in self.coeff_dict_form.items():
                    coeff_dict[k] = float(row[v])

                tmp = {"hash1": subj_code[0], "hash2": obj_code[0],
                       "relation": row[2], "coeff_dict": coeff_dict}
                hash_to_mappings[subj_code[0]].extend([Mapping(**tmp)])

        ret_dict = {"hash_to_mappings": hash_to_mappings,
                    "hash_to_concept": hash_to_concept}
        response = Response(json.dumps(ret_dict), status=200,
                            mimetype='application/json')
        return response
