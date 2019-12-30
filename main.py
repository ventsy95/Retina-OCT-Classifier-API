# main.py

from flask import Blueprint
import base64
import io

from PIL import Image
from flask import jsonify, request
from flask_login import login_required, current_user

from .predictions import get_prediction
from .service.cassandra_service import CassandraService

main = Blueprint('main', __name__)
cassandra_service = CassandraService()


@main.route('/', methods=['GET'])
def index():
    return "Hello, World!"


@main.route('/predictions', methods=['GET'])
@login_required
def get_predictions():
    predictions = []
    rows = cassandra_service.get_predictions(current_user.email)
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


@main.route('/predictions', methods=['POST'])
@login_required
def save_prediction():
    image = request.args.get('image', '')
    image_name = request.args.get('image_name', '')
    predicted_disease = request.args.get('predicted_disease', '')
    cassandra_service.insert_prediction(image=image, image_name=image_name, predicted_disease=predicted_disease,
                                        organization=current_user.email)
    return request


@main.route('/predict', methods=['POST'])
@login_required
def predict():
    image = request.files["image"]
    image_bytes = Image.open(io.BytesIO(image.read()))
    class_name = get_prediction(pred_image=image_bytes)
    prediction = {
        'image_name': image.filename,
        'predicted_disease': class_name,
    }
    predictions = [prediction]
    return jsonify(predictions)

