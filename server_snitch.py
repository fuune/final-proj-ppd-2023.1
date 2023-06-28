import grpc
from concurrent import futures
import time
import snitch_pb2_grpc as pb2_grpc
import snitch_pb2 as pb2

import pika
import sys

class SnitchService(pb2_grpc.SnitchServicer):

    def __init__(self, *args, **kwargs):
        pass

    def SnitchUser(self, request, context):

        # get the string from the incoming request
        message = request.message

        print(message)
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)

        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)
        connection.close()

        return pb2.MessageResponse(**result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    pb2_grpc.add_SnitchServicer_to_server(SnitchService(), server)
    server.add_insecure_port('[::]:8080')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()