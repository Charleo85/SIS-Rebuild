from kafka import KafkaConsumer
from kafka import KafkaProducer
from elasticsearch import Elasticsearch
import json
import time

# Delay to allow Kafka and Elastic Search to complete initialization
time.sleep(30)

es = Elasticsearch(['es'])

# Load fixture into elastic search
with open('./models/data.json') as data_file:
    data = json.load(data_file)
for element in data:
    # General Index
    if 'id' in element['fields']
        es.index(index='general_index', doc_type='listing', id=element['fields']['id'], body=element)

    # Model Specific Indices (Not sure if necessary)
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
        if 'id' in element['fields']
            es.index(index='general_index', doc_type='listing', id=new_listing['fields']['id'], body=new_listing)

        # Model Specific Indices (Not sure if necessary)
        if new_listing['model'] == 'api.Instructor':
            es.index(index='instructor_index', doc_type='listing', id=new_listing['fields']['id'], body=new_listing)
        elif new_listing['model'] == 'api.Student':
            es.index(index='student_index', doc_type='listing', id=new_listing['fields']['id'], body=new_listing)
        elif new_listing['model'] == 'api.Course':
            es.index(index='course_index', doc_type='listing', id=new_listing['fields']['id'], body=new_listing)

        es.index(index='general_index', doc_type='listing', id=new_listing['id'], body=new_listing)
    es.indices.refresh(index="listing_index")
