#2018-04-06T23:08:37.604169Z 1 [Note] A temporary password is generated for root@localhost: *0%jZ=ncXbqk
#new pass: star2222
#made a user james w/ pass star2222
import json
from flask_restful import Resource
from flask import Flask, Response
#import MySQLdb as sql
import pymysql as sql

class pred_occ_query(Resource):
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
                #assuming that the url is something like: "http://something.com/get_results/SUBJECT_CUI+PREDICATE+OBJECT_CUI"
                vals = query_params.split("+")
                subject_ = vals[0]
                predicate_ = vals[1]
                object_ = vals[2]
                where_query = ''
                if predicate_ is 'NULL':
                    where_query = "WHERE SUBJECT_CUI = '" + subject_ + "' AND OBJECT_CUI = '" + object_ + "'"
                else:
                    where_query = "WHERE PREDICATE = '" + predicate_ + "' AND SUBJECT_CUI = '" + subject_ + "' AND OBJECT_CUI = '" + object_ + "'"
                query_row_string = "SELECT * FROM austin_pred_occ_test " + where_query + " LIMIT 1;"
                print(query_row_string)
                cursor.execute(query_row_string)
                row = cursor.fetchall()
                #I gotta find the last coloumn and print the result of the last coloumn
                reponse = Response(json.dumps(row), status=200, mimetype='application/json')
                return reponse

            except:
                return json.dumps({})