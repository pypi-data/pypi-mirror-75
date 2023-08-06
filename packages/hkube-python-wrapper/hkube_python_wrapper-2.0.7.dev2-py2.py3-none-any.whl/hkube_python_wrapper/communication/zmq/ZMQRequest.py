
# import zmq
import zmq.green as zmq
import time
context = zmq.Context()


class ZMQRequest(object):
    def __init__(self, reqDetails):
        self.poller = zmq.Poller()
        self.socket = context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.connect('tcp://' + reqDetails['host'] + ':' + str(reqDetails['port']))
        self.poller.register(self.socket, zmq.POLLIN)
        self.content = reqDetails['content']
        self.timeout = int(reqDetails['timeout'])

    def invokeAdapter(self):
        print(time.time(), 'before send')
        self.socket.send(self.content)
        print(time.time(), 'after send')
        result = self.poller.poll(self.timeout)
        print(time.time(), 'after poll')
        if (result):
            print(time.time(), 'before recv')
            message = self.socket.recv()
            print(time.time(), 'after recv')
            return message
        raise Exception('Timed out:' + str(self.timeout))

    def close(self):
        self.socket.close()
