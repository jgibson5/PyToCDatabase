import socket
import sys
import marshal
import types
import datetime
import pickle
import time

class PickleMonger(object):
    """docstring for PickleMonger"""
    def __init__(self):
        pass

    def connect(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.server_address = ('localhost', 80)

        
    def send(self, command, c, instances = None, wait=100, **kwargs):
        print >>sys.stderr, 'pre connection'
        self.connect()
        self.sock.connect(self.server_address)
        print >>sys.stderr, 'connecting to %s port %s' % self.server_address
        if instances == None: instances = []
        try:
            # Send data
            m = [command, c, instances]
            t = pickle.dumps(m)
            print t
            self.sock.sendall(pickle.dumps(m))

            # Look for the response
            t0 = datetime.datetime.now()
            t1 = datetime.datetime.now()
            while ((t1 - t0).microseconds / 1000.0) + ((t1-t0).seconds * 1000.0) < wait:
                t1 = datetime.datetime.now()

                data = self.sock.recv(1024)
                if data != "":
                    t0 = t1
                    t1 = datetime.datetime.now()
                # print >>sys.stderr, 'received "%s"' % data

        finally:
            print >>sys.stderr, 'closing socket'
            self.sock.close()

        

    # Takes a Class definition and returns changed
    # __dict__ for serialization.
    def marshalClass(self, c):
        d = {}
        d['__name__'] = c.__name__
        for a, b in c.__dict__.items():
            if type(b) == types.FunctionType:
                d[a] = b.func_code
            elif type(b) == types.GetSetDescriptorType:
                pass
            else:
                d[a] = b
        return marshal.dumps(d)

    def addClass(self, c):
        self.send("addClass", self.marshalClass(c))

    def addInstances(self, c, *instances):
        ms = list(instances)
        self.send("addInstances", None, ms)


class Test2(object):
    def __init__(self, arg = 3):
        self.arg = arg

    def plus(self):
        self.arg += 1



if __name__ == "__main__":
    p = PickleMonger()
    p.addClass(Test2)
    t = Test2()
    b = Test2()
    print Test2.__dict__
    p.addInstances(Test2, t, b)








