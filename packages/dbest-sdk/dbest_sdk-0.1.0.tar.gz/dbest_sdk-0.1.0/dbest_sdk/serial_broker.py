import grpc
import threading
import serial
import six
import serial.tools.list_ports
import time
from dbest_sdk.generated import bidirectional_pb2_grpc as bidirectional_pb2_grpc
from dbest_sdk.generated import bidirectional_pb2 as bidirectional_pb2
from threading import Lock


class SerialUitls:
    # serial config
    BAUDRATE = 38400
    GET_STATE = "01"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    NO_SERIAL_PORT = "NO_SERIAL_PORT"
    SENT = "SENT"
    NO_DATA = "NO_DATA"

    def __init__(self):
        self.ser = None
        self.lock = Lock()

    @staticmethod
    def is_error(message):
        return message in [
            SerialUitls.TIMEOUT_ERROR,
            SerialUitls.INTERNAL_ERROR,
            SerialUitls.NO_SERIAL_PORT,
            SerialUitls.NO_DATA,
        ]

    def get_port(self):
        try:
            comports = serial.tools.list_ports.comports()
            if self.ser and len(comports) != 0:
                if not self.ser.is_open:
                    self.ser.open()
            if self.ser and len(comports) == 0:
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
                if self.ser.is_open:
                    self.ser.close()
                self.ser = None
            elif not self.ser and len(comports) != 0:
                device_name = comports[0].device
                self.ser = serial.Serial(
                    device_name,
                    timeout=0.2,
                    baudrate=SerialUitls.BAUDRATE,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                )
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
                if not self.ser.is_open:
                    self.ser.open()
            elif not self.ser and len(comports) == 0:
                pass
            return self.ser
        except Exception as e:
            print(e)
            return None

    def send_data(self, message):
        self.lock.acquire()
        print("SerialUitls: send_data, sending %s" % message)
        ser = self.get_port()
        result = None
        if ser:
            try:
                if six.PY2:
                    ser.write(bytes(message))  # Python 2 syntax
                else:
                    ser.write(bytes(message, "utf-8"))  # Python 3 syntax
                result = SerialUitls.SENT
            except serial.SerialTimeoutException:
                result = SerialUitls.TIMEOUT_ERROR
            except Exception as e:
                print(e)
                result = SerialUitls.INTERNAL_ERROR
        else:
            result = SerialUitls.NO_SERIAL_PORT
        self.lock.release()
        return result

    def receive_data(self):
        self.ser = self.get_port()
        result = None
        if self.ser:
            try:
                received_message = self.ser.readline()
                received_message = str(received_message.decode("utf-8"))
                result = received_message
            except Exception as e:
                print(e)
                result = SerialUitls.INTERNAL_ERROR
        else:
            result = SerialUitls.NO_SERIAL_PORT
        if result == "":
            result = SerialUitls.NO_DATA
        return result


class SerialBroker:
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.serial_utils = SerialUitls()
        self.running = True

    def start(self):
        """ Receive states from serial port and redirect to grpc server """
        t = threading.Thread(target=self._start, args=[])
        t.start()

    def _start(self):
        while self.running:
            message = self._receive_from_serial()
            if not SerialUitls.is_error(message):
                print("MESSAGE RECEIVED %s" % message)
            message = message.split(",")
            if message[0] == "S":
                message = message[1]
                if not SerialUitls.is_error(message):
                    response = self._send_state(message)
                    if response is not None and isinstance(
                        response, bidirectional_pb2.Ok
                    ):
                        pass
                    else:
                        print("BAD STATUS UPDATE on _start")
            elif message[0] == "A":
                data = message[1]
                id = message[2]
                self._send_answer(id, data)
        print("THREAD SerialBroker FINISHED")

    def _receive_from_serial(self):
        return self.serial_utils.receive_data()

    def _send_state(self, state):
        try:
            stub = bidirectional_pb2_grpc.BidirectionalStub(self.channel)
            message = bidirectional_pb2.NewState(state=state)
            response_future = stub.UpdateState.future(message)
            response = response_future.result()
            return response
        except Exception as e:
            print(e)
        return None

    def _send_answer(self, id, data):
        try:
            stub = bidirectional_pb2_grpc.BidirectionalStub(self.channel)
            message = bidirectional_pb2.Message(id=id, data=data)
            response_future = stub.UpdateAnswer.future(message)
            response = response_future.result()
            return response
        except Exception as e:
            print(e)
        return None

    def close(self):
        self.channel.close()
        self.running = False
