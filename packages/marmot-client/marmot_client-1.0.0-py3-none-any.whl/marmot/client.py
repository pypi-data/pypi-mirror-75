import grpc
import marmot_dataset_pb2_grpc as dataset_grpc

__channel = None
__dataset_server_stub = None

def connect(host, port):
    target = '{host}:{port}'.format(host=host, port=port)
    global __channel
    __channel = grpc.insecure_channel(target)
    global __dataset_server_stub
    __dataset_server_stub = dataset_grpc.DataSetServiceStub(__channel)

def disconnect():
    if __channel:
        __channel.close()

def marmot_channel():
    if __channel:
        return __channel
    else:
        raise NotConnected

def dataset_server_stub():
    if __dataset_server_stub:
        return __dataset_server_stub
    else:
        raise NotConnected

class NotConnected(Exception):
    pass