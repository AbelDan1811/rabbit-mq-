import pika
import requests
import lxml.html

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='requests', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='requests', queue=queue_name)

def handle_message(ch, method, properties, body) : 
    message = body.decode('utf-8')
    print("Receive message : %r" % message)
    if message == 'fetch' : 
        articles = fetch_articles()
        for articles_title in articles : 
            print(articles_title)

def fetch_articles() : 
    response = requests.get('https://vnexpress.net/thoi-su')
    tree = lxml.html.fromstring(response.text)
    urls = tree.xpath('//h4[@class="title-news"]/a/text()')

    return urls


channel.basic_consume(queue=queue_name, on_message_callback=handle_message, auto_ack=True)
channel.start_consuming()
