# main.py

from flask import Blueprint, Response, jsonify, request
import base64
import io

from PIL import Image
from flask_login import login_required, current_user

from .predictions import get_prediction
from .service.cassandra_service import CassandraService
from flask_cors import cross_origin
import uuid

main = Blueprint('main', __name__)
cassandra_service = CassandraService()


@main.route('/', methods=['GET'])
@login_required
def index():
    return "Hello, World!"


@main.route('/predictions', methods=['GET'])
@login_required
@cross_origin(origin='dev.retina.classifier')
def get_predictions():
    predictions = []

    rows = cassandra_service.get_predictions(current_user.email)
    for prediction_row in rows:
        prediction = {
            'prediction_timestamp': prediction_row.prediction_timestamp,
            'record_id': prediction_row.record_id,
            'race': prediction_row.race,
            'age': prediction_row.age,
            'gender': prediction_row.gender,
            'image_name': prediction_row.image_name,
            'predicted_disease': prediction_row.predicted_disease,
            'image': base64.b64encode(prediction_row.image).decode('utf-8')
        }
        predictions.append(prediction)
    return jsonify(predictions)


@main.route('/predictions', methods=['POST'])
@login_required
@cross_origin(origin='dev.retina.classifier')
def save_prediction():
    image = request.files["image"]
    image_bytes = image.read()
    image_name = request.form.get('image_name', '')
    predicted_disease = request.form.get('predicted_disease', '')
    race = request.form.get('race', '')
    age = int(request.form.get('age', ''))
    gender = request.form.get('gender', '')
    cassandra_service.insert_prediction(image=image_bytes, image_name=image_name, predicted_disease=predicted_disease,
                                        organization=current_user.email, race=race, age=age, gender=gender)
    return Response('Successfully saved.', 200)


@main.route('/delete-prediction', methods=['POST'])
@login_required
@cross_origin(origin='dev.retina.classifier')
def delete_prediction():
    predicted_disease = request.form.get('predicted_disease', '')
    record_id = uuid.UUID(request.form.get('record_id', ''))
    age = int(request.form.get('age', ''))
    race = request.form.get('race', '')
    gender = request.form.get('gender', '')

    cassandra_service.delete_prediction(predicted_disease=predicted_disease, record_id=record_id, age=age, race=race,
                                        gender=gender, organization=current_user.email)
    return Response('Successfully deleted.', 200)


@main.route('/predict', methods=['POST'])
@login_required
@cross_origin(origin='dev.retina.classifier')
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

