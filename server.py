from flask import Flask
from flask_restful import Api
from pred_occ_query import pred_occ_query
from ml_query import ml_query
#from random_row import rand_r
import os

app = Flask(__name__)
api = Api(app)

client = None

@app.route('/')
def start():
    return """<b>HII-C MedLearn API.</b><br><br>
            This a playground for HII-C MedLearn   
              """

api.add_resource(pred_occ_query, '/query_results', '/query_results/<string:query_params>', '/query_results/<string:query_params>/')
api.add_resource(ml_query, '/query_ml', '/query_ml/<string:query_params>', '/query_results/<string:query_params>/')
#api.add_resource(rand_r, '/rand_row', '/rand_row/')


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), threaded=True)
