from argparse import ArgumentParser
from getpass import getpass

from flask import Flask
from flask_restful import Api
from get_mappings import get_mapppings
from get_output import get_output
from get_assoc import get_assoc
from get_relation import get_relation

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
    params[arg] = getattr(args, arg)

app = Flask(__name__)
api = Api(app)
client = None


@app.route('/')
def start():
    return """<b>HII-C MedLearn API.</b><br><br>
            This a playground for HII-C MedLearn   
            """


# api.add_resource(get_mapppings, '/get_mappings')
api.add_resource(get_relation, '/get_relation',
                 methods=['GET'], resource_class_kwargs={**params, })
api.add_resource(get_assoc, '/get_assoc',
                 methods=['GET'], resource_class_kwargs={**params, })
api.add_resource(get_output, '/get_output',
                 methods=['GET'], resource_class_kwargs={**params, })


app.run(host='0.0.0.0', port='5000')
