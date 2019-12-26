import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    CLASSIFIER_LOCATION = '/Users/a112233/Downloads/VGG16_v2-OCT_Retina_CSR_MH.pt'
    CASSANDRA_CLUSTER_ENDPOINTS = ['127.0.0.1']
    CASSANDRA_KEYSPACE = 'test'
    PREDICTIONS_TABLE = 'predictions'
    SECRET_KEY_LOCATION = 'resources/key.key'
    CASSANDRA_AUTH_CONF_LOCATION = 'resources/cassandra_auth.ini.encrypted'

