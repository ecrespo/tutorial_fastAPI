import pika

def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")

def consume_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='fastapi_queue')

    channel.basic_consume(queue='fastapi_queue',
                          on_message_callback=callback,
                          auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()