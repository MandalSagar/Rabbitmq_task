import pika
import time
import random

def sender():
    #RabbitMq
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.01'))
    channel = connection.channel()
    channel.queue_declare(queue='status_code', durable=True)

    try:
        while True:
            status_code = random.randint(0, 6)
            message = str(status_code)
            channel.basic_publish(exchange='',routing_key='status_code',body=message)
            print(f"sent status code: {message}")

            time.sleep(1)
    except KeyboardInterrupt:
        print("process ended by user.")
    finally:

        connection.close()

if __name__ == "__main__":
    sender()
