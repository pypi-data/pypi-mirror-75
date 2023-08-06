Required modules:
Flask
requests
celery
NECESSAIRLY have RabbitMQ

Install broker RabbitMQ:
If you’re using Ubuntu or Debian install RabbitMQ by executing this command:

$ sudo apt-get install rabbitmq-server
$ sudo service rabbitmq-server start

Or, if you want to run it on Docker execute this:

$ docker run -d -p 5672:5672 rabbitmq


BEFORE running server
activate worker from server directory
celery -A start.celery worker -l info -n my_worker
