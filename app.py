#!flask/bin/python
import base64

from flask import Flask, jsonify, request
from cassandra.cluster import Cluster
from datetime import datetime
import uuid

app = Flask(__name__)
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('test')


@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"


@app.route('/predictions', methods=['GET'])
def get_predictions():
    predictions = []
    rows = session.execute(
        'SELECT prediction_timestamp, record_id, image_name, image, predicted_disease FROM predictions')
    for prediction_row in rows:
        prediction = {
            'prediction_timestamp': prediction_row.prediction_timestamp,
            'record_id': prediction_row.record_id,
            'image_name': prediction_row.image_name,
            'predicted_disease': prediction_row.predicted_disease,
            'image': base64.b64encode(prediction_row.image).decode('utf-8')
        }
        predictions.append(prediction)
    return jsonify(predictions)


@app.route('/predictions', methods=['POST'])
def save_prediction():
    insert_prediction_stmt = session.prepare("""INSERT INTO predictions (prediction_timestamp, record_id, image,
     image_name, predicted_disease) VALUES (?, ?, ?, ?, ?)""")

    image = request.args.get('image', '')
    image_name = request.args.get('image_name', '')
    predicted_disease = request.args.get('predicted_disease', '')
    prediction_timestamp = datetime.now()
    record_id = uuid.uuid4()

    statement = session.execute(insert_prediction_stmt,
                                [prediction_timestamp, record_id, image, image_name, predicted_disease])
    print(statement)
    return request


if __name__ == '__main__':
    app.run(debug=True)
