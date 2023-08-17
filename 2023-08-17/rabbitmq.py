import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
queue_name = 'my_queue'

channel.queue_declare(queue=queue_name)
message = 'Hello, RabbitMQ!'
channel.basic_publish(exchange='', routing_key=queue_name, body=message)
print(f" [x] Sent '{message}'")

def callback(ch, method, properties, body):
    print(f" [x] Received '{body.decode()}'")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
connection.close()

