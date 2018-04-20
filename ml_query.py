import json
from flask_restful import Resource
from flask import Flask, Response
#import MySQLdb as sql
import pymysql as sql

class ml_query(Resource):
    def __init__(self):
        self.user_ = 'hiic'  # i just put the connect and db access information because I was using a local database
        self.host_ = 'db01.healthcreek.org'
        self.pass_ = 'greenes2018'
        self.db_ = 'derived'

    def get(self, query_params):
        if query_params is not None:
            try:
                conn = sql.connect(user=self.user_, host=self.host_, db=self.db_, passwd=self.pass_)
                cursor = conn.cursor()
                #assuming that the url is something like: "http://something.com/get_results/STRING+code+pred"
                vals = query_params.split("+")
                encode_ = vals[0]
                if encode_ is 'condition':
                    encode_ = int (0)
                elif encode_ is 'observation':
                    encode_ = int (1)
                elif encode is 'medication':
                    encode_ = int (2)
                else:
                    encode_ = int (-1)
                subject_cui = vals[1]
                pred_ = vals[2]
                where_query = "WHERE PREDICATE = '" + pred_ + "' AND SUBJECT_CUI = '" + subject_cui + "' AND <SEN_TYPE> = '" + encode_ + "'"
                query_row_string = "SELECT * FROM <ml_output_table> " + where_query + " LIMIT 1;"
                print(query_row_string)
                cursor.execute(query_row_string)
                row = cursor.fetchall()
                #I gotta find the last coloumn and print the result of the last coloumn
                reponse = Response(json.dumps(row), status=200, mimetype='application/json')
                return reponse

            except:
                return json.dumps({})