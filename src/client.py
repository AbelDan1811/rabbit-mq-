import pika


connection = pika.BlockingConnection()
channel = connection.channel()
channel.exchange_declare(exchange='requests', exchange_type='fanout')

while True :
    request = input('Give request: ')
    if request == 'all' :
        print('All')
        channel.basic_publish(exchange='requests', routing_key='article', body='fetch'.encode('utf-8'))  
    elif request == 'vnexpress' : 
        print('A')
    elif request == 'end' : 
        break 

requeued_messages = channel.cancel()
print('Requeued %i messages' % requeued_messages)
connection.close()