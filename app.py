from bson import objectid
from flask import Flask, request, jsonify, Response
from flask import render_template
from flask_pymongo import PyMongo
from pymongo import message
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.wrappers import response

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/gym"
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/traing', methods=['POST'])
def create_traing():
    
    monday =request.json['monday']
    tuesday =request.json['tuesday']
    wednesday =request.json['wednesday']
    thursday =request.json['thursday']
    friday =request.json['friday']
    
    if monday and tuesday and wednesday and thursday and friday:
        id = mongo.db.traing.insert(
            {'monday': monday, 'tuesday': tuesday, 'wednesday': wednesday, 'thursday': thursday, 'friday': friday}
        )
        response = {
            'id': str(id),
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday
        }
        return response
    else:
        return not_found

@app.route('/ejercicios', methods=['POST'])
def ejercicios():

    pecho = request.json['pecho']
    espalda = request.json['espalda']
    abdomen = request.json['abdomen']
    piernas = request.json['piernas']
    brazos = request.json['brazos']

    if pecho and espalda and abdomen and piernas and brazos:
        id = mongo.db.ejercicios.insert(
            {'pecho': pecho, 'espalda': espalda, 'abdomen': abdomen, 'piernas': piernas, 'brazos': brazos}
        )

        response = {
            'id': str(id),
            'pecho': pecho,
            'espalda': espalda,
            'abdomen': abdomen,
            'piernas': piernas,
            'brazos': brazos
        }
        return response
    else:
        return not_found

@app.route('/traing', methods=['GET'])
def get_traing():
    traing = mongo.db.traing.find()
    response = json_util.dumps(traing)
    return Response(response, mimetype="application/json")

@app.route('/traing/<id>', methods=['GET'])
def search_traing(id):
    train = mongo.db.traing.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(train)
    return Response(response, mimetype="application/json")

@app.route('/traing/<id>', methods=['DELETE'])
def delete_traing(id):
    mongo.db.traing.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'entrenamiento ' + id + 'se a eliminado '})
    return response

@app.route('/traing/<id>', methods=['PUT'])
def update_traing(id):
    monday =request.json['monday']
    tuesday =request.json['tuesday']
    wednesday =request.json['wednesday']
    thursday =request.json['thursday']
    friday =request.json['friday']

    if monday and tuesday and wednesday and thursday and friday:
        mongo.db.traing.update_one({'_id': ObjectId(id)}, {'$set': {
            'id': str(id),
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday
        }})
        response = jsonify({'message': 'entrenamiento' + id + 'a sido actualizado'})
        return response
    else:
        return not_found()
        

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify ({
        'message': 'Recurso no Encontrado:' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True)