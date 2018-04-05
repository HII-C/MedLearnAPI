import json
from flask import Flask, Response
#import MySQLdb as sql
import pymysql as sql


@app.route('/rand_row')
def get_random_row():
    user_ = 'james' #i just put the connect and db access information because I was using a local database
    host_ = 'localhost'
    pass_ = 'hiic'
    db_ = 'derived'
    conn = sql.connect(user = user_, host = host_, db = db_, passwd = pass_)
    cursor = conn.cursor()
    query_row_string = 'SELECT * FROM FAKE_DIAGNOSIS ORDER BY RAND() LIMIT 1;'
    cursor.execute(query_row_string)
    row = cursor.fetchall()
    reponse = Response(json.dumps(row), status=200, mimetype= 'application/json')
    return reponse

@app.errorhandler(404)
def not_found(e):
    return '', 404

