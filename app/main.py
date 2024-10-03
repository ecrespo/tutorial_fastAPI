import threading
from fastapi import FastAPI
import time
import pika

app = FastAPI()


def wait_for_rabbitmq_to_be_ready(host, user, password, retries=5, delay=5):
    for i in range(retries):
        try:
            credentials = pika.PlainCredentials(user, password)
            parameters = pika.ConnectionParameters(host=host, credentials=credentials)
            connection = pika.BlockingConnection(parameters)
            connection.close()
            print(f"Successfully connected to RabbitMQ on attempt {i + 1}")
            return
        except pika.exceptions.AMQPConnectionError:
            print(f"RabbitMQ not ready, attempt {i + 1} of {retries}")
            time.sleep(delay)
    raise Exception("Failed to connect to RabbitMQ after several retries")


def get_rabbitmq_connection(host='rabbitmq', user='myuser', password='mypassword'):
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(host=host, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    return channel


def consume_rabbitmq_messages():
    try:
        print("Attempting to consume messages from RabbitMQ")
        channel = get_rabbitmq_connection()
        print("Declaring queue as durable")
        channel.queue_declare(queue='fastapi_queue', durable=True)

        def callback(ch, method, properties, body):
            print(f"Received {body}")
            # Procesar el cuerpo del mensaje
            print(f"Processed message: {body}")

        print("Setting up basic consume")
        channel.basic_consume(queue='fastapi_queue', on_message_callback=callback, auto_ack=True)
        print("Starting to consume messages")
        channel.start_consuming()
    except Exception as e:
        print(f"Failed to consume messages: {e}")
        raise e



@app.on_event("startup")
def startup_event():
    print("FastAPI started")
    # Verificar que RabbitMQ está listo antes de iniciar el consumidor
    wait_for_rabbitmq_to_be_ready(host='rabbitmq', user='myuser', password='mypassword')
    threading.Thread(target=consume_rabbitmq_messages, daemon=True).start()


@app.get("/")
def read_root():
    return {"message": "Hello RabbitMQ with FastAPI"}

@app.post("/send")
def send_message(message: str):
    try:
        channel = get_rabbitmq_connection()
        channel.queue_declare(queue='fastapi_queue', durable=True)
        channel.basic_publish(exchange='', routing_key='fastapi_queue', body=message)
        print(f"Sent message: {message}")
        return {"status": "Message sent"}
    except Exception as e:
        print(f"Failed to send message: {e}")
        return {"status": "Failed to send message"}