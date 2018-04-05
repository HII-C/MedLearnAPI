import json
from flask_restful import Resource
from flask import Flask, Response
#import MySQLdb as sql
import pymysql as sql

class getRow(Resource):
    def __init__(self):
        user_ = 'james'  # i just put the connect and db access information because I was using a local database
        host_ = 'localhost'
        pass_ = 'hiic'
        db_ = 'derived'
        conn = sql.connect(user=user_, host=host_, db=db_, passwd=pass_)
        cursor = conn.cursor()

    def get(self, row_params):
        if row_params is not None:
            try:
                #assuming that the url is something like: "http://something.com/get_row/Subject+Predicate+Object"
                vals = row_params.split("+")
                subject_ = vals[0]
                predicate_ = vals[1]
                object_ = vals[2]

                where_query = "WHERE PREDICATE = " + predicate_ + " AND SUBJECT_NAME = " + subject_ + "AND OBJECT_NAME = " + object_

                query_row_string = "SELECT * FROM austin_pred_occ_test " + where_query + " LIMIT 1;"
                cursor.execute(query_row_string)
                row = cursor.fetchall()
                reponse = Response(json.dumps(row), status=200, mimetype='application/json')
                return reponse

            except:
                return json.dumps({})
