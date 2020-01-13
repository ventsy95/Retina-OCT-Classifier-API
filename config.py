import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    CLASSIFIER_LOCATION = '/Users/Ventsy/Downloads/VGG16_v2-OCT_Retina_CSR_MH.pt'
    CASSANDRA_CLUSTER_ENDPOINTS = ['127.0.0.1']
    CASSANDRA_KEYSPACE = 'retina_oct'
    PREDICTIONS_TABLE = 'predictions'
    SECRET_KEY_LOCATION = '/Users/Ventsy/dev/Retina_OCT_Classifier_API/resources/key.key'
    CASSANDRA_AUTH_CONF_LOCATION = '/Users/Ventsy/dev/Retina_OCT_Classifier_API/resources/cassandra_auth.ini.encrypted'

