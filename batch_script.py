from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json, time

try:
    # wait for 30 seconds for the initialization of Kafka
    time.sleep(30)

    # try to create instances of Kafka and Elasticsearch
    es = Elasticsearch(['es'])
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])

finally:
    # initialize the Elasticsearch instance
    es = Elasticsearch(['es'])

    # Load fixture into elastic search
    data = {}
    with open('./models/data.json') as data_file:
        data = json.load(data_file)
    with open('./models/output.json') as data_file:
        data += json.load(data_file)
    
    for element in data:
        # General Index
        if 'id' in element['fields']:
            # password should not be included in search
            if 'password' in element['fields']:
                element['fields'].pop('password', None)
            es.index(index='general_index', doc_type='listing', id=element['fields']['id'], body=element)

        # Model Specific Indices
        if element['model'] == 'api.Instructor':
            es.index(index='instructor_index', doc_type='listing', id=element['fields']['id'], body=element)
        elif element['model'] == 'api.Student':
            es.index(index='student_index', doc_type='listing', id=element['fields']['id'], body=element)
        elif element['model'] == 'api.Course':
            es.index(index='course_index', doc_type='listing', id=element['fields']['id'], body=element)

    # Start listening to Kafka Queue
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
    while True:
        for message in consumer:
            new_listing = (json.loads(message.value.decode('utf-8')))

            # General Index
            es.index(index='general_index', doc_type='listing', id=new_listing['fields']['id'], body=new_listing)

            # Model Specific Indices
            if new_listing['model'] == 'api.Instructor':
                es.index(index='instructor_index', doc_type='listing', id=new_listing['fields']['id'], body=new_listing)
            elif new_listing['model'] == 'api.Student':
                es.index(index='student_index', doc_type='listing', id=new_listing['fields']['id'], body=new_listing)
            elif new_listing['model'] == 'api.Course':
                es.index(index='course_index', doc_type='listing', id=new_listing['fields']['id'], body=new_listing)

        # refresh all incides to make changes effective
        es.indices.refresh(index="listing_index")
