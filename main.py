from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS  # Certifique-se de que flask-cors está instalado

import os
from pymongo import MongoClient  # Certifique-se de que pymongo está instalado

from db import db

app = Flask(__name__)
api = Api(app)
CORS(app)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

collection = db["list_numbers"]

class ListData(Resource):
    def get(self, number_sim):
        data = list(collection.find({'number_sim': number_sim}).sort('_id', -1))

        # Converta o campo _id (ObjectId) para uma string
        for item in data:
            item['_id'] = str(item['_id'])

        response = {
            'messages': data,
            'totalItems': len(data)
        }

        return jsonify(response)

api.add_resource(ListData, '/api/list/<string:number_sim>')

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
