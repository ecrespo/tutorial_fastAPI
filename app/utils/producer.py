import pika

def publish_message(message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='fastapi_queue')

    channel.basic_publish(exchange='',
                          routing_key='fastapi_queue',
                          body=message)
    connection.close()
