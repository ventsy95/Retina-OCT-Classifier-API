#!flask/bin/python
import base64
import io

from PIL import Image
from flask import Flask, jsonify, request

from predictions import get_prediction
from service.cassandra_service import CassandraService

app = Flask(__name__)
cassandra_service = CassandraService()


@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"


@app.route('/predictions', methods=['GET'])
def get_predictions():
    predictions = []
    rows = cassandra_service.get_predictions()
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
    image = request.args.get('image', '')
    image_name = request.args.get('image_name', '')
    predicted_disease = request.args.get('predicted_disease', '')
    cassandra_service.insert_prediction(image=image, image_name=image_name, predicted_disease=predicted_disease)
    return request


@app.route('/predict', methods=['POST'])
def predict():
    image = request.files["image"]
    image_bytes = Image.open(io.BytesIO(image.read()))
    class_name = get_prediction(pred_image=image_bytes)
    return jsonify(prediction=class_name)


if __name__ == '__main__':
    app.run(debug=True, ssl_context=('ssl/cert.pem', 'ssl/key.pem'))
