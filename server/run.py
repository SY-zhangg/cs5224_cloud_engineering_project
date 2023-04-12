from flask import Flask, request, jsonify
from db_helpers import DB_Connector
from db_helpers import *
from mock_service import *
from flask_cors import CORS, cross_origin

app = Flask(__name__)  # Setup the flask app by creating an instance of Flask
CORS(app, support_credentials=True)

mk = Mock_Service()

@app.route('/setup', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def setup():
    if request.method == 'GET':
        return jsonify({"result": "Setup test"}), 200
    elif request.method == 'POST':
        db = DB_Connector
        try:
            db.get_mysql_connection()
            db.set_up_mysql_tables()
            return jsonify({"success": True}), 200
        except:
            return jsonify({"error": "cannot initialize the database"}), 400
    else: 
        return jsonify({"error": "cannot process this type of request"}), 400


@app.route('/search', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def search():
    if request.method == 'GET':
        return jsonify({"result": "Search test"}), 200
    elif request.method == 'POST':
        response = mk.mockSearch(request.get_json())
        return response
    else:
        return jsonify({"error": "cannot process this type of request"}), 400
    
@app.route('/predict', methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def predict():
    if request.method == 'GET':
        return jsonify({"result": "Predict test"}), 200
    elif request.method == 'POST':
        response = mk.mockPredict()#request.get_json()
        return response
    else:
        return jsonify({"error": "cannot process this type of request"}), 400

# Running app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'admin'
# app.config['MYSQL_DB'] = 'flask'
# app.config['CORS_HEADERS'] = 'Content-Type'
