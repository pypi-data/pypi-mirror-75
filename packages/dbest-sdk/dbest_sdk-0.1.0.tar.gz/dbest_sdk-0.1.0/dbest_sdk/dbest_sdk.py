import grpc
import uuid
import threading
import time
from threading import Lock
from dbest_sdk.generated import bidirectional_pb2_grpc as bidirectional_pb2_grpc
from dbest_sdk.generated import bidirectional_pb2 as bidirectional_pb2


class StatusChanged:
    def __init__(self, status_to_wait):
        self.status_to_wait = status_to_wait


class StatusChangedListener:
    def __init__(self, dbest_instance):
        self.dbest_instance = dbest_instance
        self.uid = str(uuid.uuid1())

    def _subscribe(self):
        stub = bidirectional_pb2_grpc.BidirectionalStub(
            self.dbest_instance.channel)
        responses = stub.SubscribeStateListener(
            bidirectional_pb2.Subscribe(id=self.uid)
        )
        try:
            for new_state_response in responses:
                t = threading.Thread(
                    target=self.onStateChanged, args=[new_state_response.state]
                )
                t.daemon = True
                t.start()
        except Exception as e:
            print("INFO: Channel closed, Listener closed.")
            print(e)

    def subscribe(self):
        t = threading.Thread(target=self._subscribe, args=[])
        t.daemon = True
        t.start()

    def unsubscribe(self):
        stub = bidirectional_pb2_grpc.BidirectionalStub(
            self.dbest_instance.channel)
        response = stub.UnsubscribeStateListener(
            bidirectional_pb2.Unsubscribe(id=self.uid)
        )
        return response

    def onStateChanged(self, state):
        pass


class _AwaitStateListener(StatusChangedListener):
    def __init__(self, dbest_instance, status_to_wait):
        self.status_to_wait = status_to_wait
        super().__init__(dbest_instance)
        self.lock = Lock()
        self.lock.acquire()
        self.subscribe()

    def onStateChanged(self, state):
        print("LOG: esperando %s, actual %s" % (self.status_to_wait, state))
        if state.strip() == self.status_to_wait.strip():
            self.lock.release()

    def wait(self):
        self.lock.acquire()
        self.lock.release()
        self.unsubscribe()


class Dbest(object):
    def __init__(self, ip="localhost:50051"):
        self.ip = ip
        self.channel = None

    def connect(self):
        self.channel = grpc.insecure_channel(self.ip)

    def wait_for_state(self, status_to_wait):
        await_state_listener = _AwaitStateListener(self, status_to_wait)
        await_state_listener.wait()

    @staticmethod
    def build_simple_request_message(data_str):
        id = str(data_str)  # str(uuid.uuid1()) # TODO
        return bidirectional_pb2.Message(id=id, data=data_str)

    def _simple_request(self, data_str):
        stub = bidirectional_pb2_grpc.BidirectionalStub(self.channel)
        response = stub.SimpleRequest(
            Dbest.build_simple_request_message(data_str), timeout=10
        )
        time.sleep(0.5)  # TODO remove sleep
        return response

    def disconnect(self):
        self.channel.close()
