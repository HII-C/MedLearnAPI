import json
from flask import Flask, Response, abort
import MySQLdb as mysql

app = Flask(__name__)

@app.route('/rand_row')
def get_random_row():
    user_ = 'james' #i just put the connect and db access information because I was using a local database
    host_ = 'localhost'
    pass_ = 'hiic'
    db_ = 'derived'
    conn = mysql.connect(user_, host_, db_, pass_)
    cursor = conn.cursor()
    query_row_string = 'SELECT * FROM FAKE_DIAGNOSIS ORDER BY RAND() LIMIT 1;'
    cursor.execute(query_row_string);
    row = cursor.fetchall()
    reponse = Response(json.dumps(row), status=200, mimetype= 'application/json')
    return reponse

@app.errorhandler(404)
def not_found(e):
    return '', 404