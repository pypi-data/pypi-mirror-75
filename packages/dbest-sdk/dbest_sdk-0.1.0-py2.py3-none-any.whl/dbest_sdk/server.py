from concurrent import futures

import grpc
import time
import uuid
import asyncio
import logging
import janus
from grpc.experimental import aio
from dbest_sdk.generated import bidirectional_pb2_grpc as bidirectional_pb2_grpc
from dbest_sdk.generated import bidirectional_pb2 as bidirectional_pb2
from dbest_sdk.serial_broker import SerialBroker


class State:
    def __init__(self, state):
        self.state = state


class Unsubscribe:
    def __init__(self, uid):
        self.uid = uid


class BidirectionalService(bidirectional_pb2_grpc.BidirectionalServicer):
    def __init__(self):
        self.queues = {}
        self.simple_requests = {}
        self.sb = SerialBroker()
        self.sb.start()

    async def SubscribeStateListener(self, request, context):
        uid = request.id
        queue = janus.Queue()
        self.queues[uid] = queue
        while True:
            message = await self.queues[uid].async_q.get()
            if isinstance(message, State):
                yield bidirectional_pb2.NewState(state=message.state)

            if isinstance(message, Unsubscribe):
                self.queues[uid].close()
                self.queues[uid] = None
                break

    def UnsubscribeStateListener(self, request, context):
        uid = request.id
        self.queues[uid].sync_q.put(Unsubscribe(uid))
        return bidirectional_pb2.Ok()

    def UpdateState(self, request, context):
        new_state = request
        dbest_state = State(new_state.state)
        for key in self.queues:
            if self.queues[key] and not self.queues[key].closed:
                self.queues[key].sync_q.put(dbest_state)
        response = bidirectional_pb2.Ok()
        return response

    async def UpdateAnswer(self, request, context):
        message = request
        print(
            "UpdateAnswer: message id %s, message data %s" % (
                message.id, message.data)
        )
        uid = int(message.id)
        data = str(message.data)
        self.simple_requests[uid].set_result(data)
        response = bidirectional_pb2.Ok()
        return response

    @staticmethod
    def message_to_str(message):
        message_str = "%s,%s" % (message.data, message.id)
        return message_str

    async def SimpleRequest(self, request, context):
        message = request

        # Send data by serial comunnication
        message_str = BidirectionalService.message_to_str(message)

        # Make a future
        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        uid = int(message.id)
        self.simple_requests[uid] = fut

        print("SimpleRequest, enviando '%s' por comunicacion serial" % message_str)
        self.sb.serial_utils.send_data(message_str)

        # Await for that future
        data = await self.simple_requests[uid]

        # Send message response
        self.simple_requests[uid] = None
        response = bidirectional_pb2.Message(data=data)
        return response


async def _start_async_server():
    server = aio.server()
    server.add_insecure_port("[::]:50051")
    bidirectional_pb2_grpc.add_BidirectionalServicer_to_server(
        BidirectionalService(), server
    )
    await server.start()
    await server.wait_for_termination()


def run_server():
    logging.basicConfig()
    loop = asyncio.get_event_loop()
    loop.create_task(_start_async_server())
    loop.run_forever()
