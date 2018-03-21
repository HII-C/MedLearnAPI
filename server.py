#connect to local mysql using mysqldb
#pull out one row
#return the row statement as a json file
from MedLearnAPI.random_row import app
import os


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), threaded=True)
