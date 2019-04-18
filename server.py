from argparse import ArgumentParser
from getpass import getpass

from flask import Flask
from flask_restful import Api
from get_mappings import get_mapppings
from get_output import get_output
from get_assoc import get_assoc
from get_relation import get_relation
from get_obs_assoc import get_obs_assoc
from flask_cors import CORS, cross_origin


# Set ''default'' parameters for database connections
params = {'user': 'root',
          'host': 'localhost',
          'db': 'example',
          'password': ''}

# parse command line (or dockerfile) modifications to the default params
parser = ArgumentParser()
parser.add_argument('--user')
parser.add_argument('--host')
parser.add_argument('--db')
parser.add_argument('--password')
args = parser.parse_args()

# iterate all vars in namespace 'args' and set their param equiv to passed value
for arg in vars(args):
    # print(arg, vars(args)[arg])
    params[arg] = str(vars(args)[arg])

print(params)

app = Flask(__name__)
api = Api(app)
CORS(app)


client = None


@app.route('/')
def main():
    return """<b>HII-C MedLearn API.</b><br><br>
            This a playground for HII-C MedLearn   
            """


#api.add_resource(get_mapppings, '/get_mappings', methods=['GET'])
api.add_resource(get_relation, '/get_relation',
                 methods=['GET'], resource_class_kwargs={"db_params": params, "table_name": "derived"})
api.add_resource(get_assoc, '/get_assoc',
                 methods=['GET'], resource_class_kwargs={"db_params": params, })
api.add_resource(get_output, '/get_output',
                 methods=['GET'], resource_class_kwargs={"db_params": params, })
api.add_resource(get_obs_assoc, '/get_obs_assoc',
                 methods=['GET'])

app.debug = True

app.run(host='0.0.0.0', port='80', threaded=True)
