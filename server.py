from flask import Flask
from flask_restful import Api
from get_mappings import get_mapppings

app = Flask(__name__)
api = Api(app)


client = None


@app.route('/')
def start():
    return """<b>HII-C MedLearn API.</b><br><br>
            This a playground for HII-C MedLearn   
            """


app.run(host='0.0.0.0', port='5000')
