import json
from flask_restful import Resource
from flask import Flask, Response
#import MySQLdb as sql
import pymysql as sql

class getRow(Resource):
    def __init__(self):
        self.user_ = 'root'  # i just put the connect and db access information because I was using a local database
        self.host_ = 'localhost'
        self.pass_ = 'star2222'
        self.db_ = 'derived'

    def get(self, row_params):
        if row_params is not None:
            try:
                print('started')
                conn = sql.connect(user=self.user_, host=self.host_, db=self.db_, passwd=self.pass_)
                print('connected')
                cursor = conn.cursor()
                # assuming that the url is something like: "http://something.com/get_results/Predicate/Subject/Object"
                vals = row_params.split("+")
                subject_ = vals[0]
                predicate_ = vals[1]
                object_ = vals[2]
                where_query = "WHERE PREDICATE = '" + predicate_ + "' AND SUBJECT_NAME = '" + subject_ + "' AND OBJECT_NAME = '" + object_ + "'"
                query_row_string = "SELECT * FROM austin_pred_occ_test " + where_query + " LIMIT 1;"
                print("this is the query: " + query_row_string)
                cursor.execute(query_row_string)
                row = cursor.fetchall()
                # I gotta find the last coloumn and print the result of the last coloumn
                reponse = Response(json.dumps(row), status=200, mimetype='application/json')
                return reponse

            except:
                return json.dumps({})