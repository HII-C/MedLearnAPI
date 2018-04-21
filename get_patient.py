import json
from flask import Flask, Response, Resource, request
import MySQLdb as sql
#import pymysql as sql
app = Flask(__name__)

@app_route('/get_patient')
class GetPatient(Resource):
    def __init__(self):
        print("")
    
    def post(self):
        pat = request.args.get('id')
        