import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

def start(system):
    app = Flask(__name__)
    CORS(app, support_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'

    @app.route("/", methods=['POST', 'OPTIONS'])
    @cross_origin(supports_credentials=True)
    def predict():
        input_object = request.get_json()['input']
        return jsonify(output=system.output(input_object))

    app.run(port=5000, debug=True)