import uuid
from datetime import datetime

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

from ..config import Config
from ..util.configuration_crypto_util import decrypt_configuration_file


class CassandraService:

    def __init__(self):
        self.cassandra_auth_config = decrypt_configuration_file(Config.CASSANDRA_AUTH_CONF_LOCATION)

        self.provider = PlainTextAuthProvider(username=self.cassandra_auth_config.get('cassandra', 'username'),
                                              password=self.cassandra_auth_config.get('cassandra', 'password'))

        self.cluster = Cluster(Config.CASSANDRA_CLUSTER_ENDPOINTS, auth_provider=self.provider)
        self.session = self.cluster.connect(Config.CASSANDRA_KEYSPACE)

    def get_predictions(self, organization):
        get_predictions_stmt = self.session.prepare(
            'SELECT prediction_timestamp, record_id, image_name, image, predicted_disease, race, age, gender FROM '
            + Config.PREDICTIONS_TABLE +
            ' WHERE organization=? ALLOW FILTERING')
        print(organization)
        rows = self.session.execute(get_predictions_stmt, [organization, ])
        return rows

    def insert_prediction(self, image, image_name, predicted_disease, organization, race, age, gender):
        prediction_timestamp = datetime.now()
        record_id = uuid.uuid4()

        insert_prediction_stmt = self.session.prepare('INSERT INTO ' + Config.PREDICTIONS_TABLE +
                                                      '(prediction_timestamp, record_id, image, image_name, '
                                                      'predicted_disease, organization, race, age, gender)'
                                                      ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)')

        self.session.execute(insert_prediction_stmt, [prediction_timestamp, record_id, image, image_name,
                                                      predicted_disease, organization, race, age, gender])

    def delete_prediction(self, predicted_disease, organization, record_id, age, race, gender):

        delete_prediction_stmt = self.session.prepare('DELETE FROM ' + Config.PREDICTIONS_TABLE +
                                                      ' WHERE predicted_disease=? and organization=? and age=? and '
                                                      'race=? and gender=? and record_id=?')

        self.session.execute(delete_prediction_stmt, [predicted_disease, organization, age, race, gender, record_id])
