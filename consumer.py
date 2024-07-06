from pymongo import MongoClient
import pika
import datetime

# Database setup
client = MongoClient('localhost', 27017)
db = client['status_db']
collection = db['status_collection']

# RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters(host="127.0.0.1"))
channel = connection.channel()
channel.queue_declare(queue="status_code", durable=True)

def callback(ch, method, properties, body):
    status_code = int(body.decode())
    timestamp = datetime.datetime.now()
    record = {
        'status_code': status_code,
        'timestamp': timestamp
    }
    collection.insert_one(record)
    print(f"Data from RabbitMQ with timestamp {timestamp}")

def start_consumer():
    channel.basic_consume(queue="status_code", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        start_consumer()
    except KeyboardInterrupt:
        print("process ended by user.")
    finally:
        connection.close()
