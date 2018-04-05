#connect to local mysql using mysqldb
#pull out one row
#return the row statement as a json file
from flask import Flask
from flask_restful import Api
from MedLearnQuery import MedLearnQuery
#from get_row import getRow
import os

app = Flask(__name__)
api = Api(app)

client = None

@app.route('/')
def start():
    return """<b>HII-C MedLearn API.</b><br><br>
              This a playground for HII-C MedLearn
              """

api.add_resource(MedLearnQuery, '/query_results', '/query_results/<string:query_params>', '/query_results/<string:query_params>/')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), threaded=True)
