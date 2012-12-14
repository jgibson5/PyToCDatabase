import socket
import sys
import marshal
import types
import datetime

class PickleMonger(object):
    """docstring for PickleMonger"""
    def __init__(self):
        self.connect()

    def connect(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.server_address = ('localhost', 80)

        
    def send(self, m, wait=100):
        self.sock.connect(self.server_address)
        print >>sys.stderr, 'connecting to %s port %s' % self.server_address

        try:
            
            # Send data
            self.sock.sendall(m)

            # Look for the response
            # amount_received = 0
            # amount_expected = len(message)
            t0 = datetime.datetime.now()
            t1 = datetime.datetime.now()
            print (t1 - t0).microseconds
            while ((t1 - t0).microseconds / 1000.0) + ((t1-t0).seconds * 1000.0) < wait:
                t1 = datetime.datetime.now()

                data = self.sock.recv(32)
                print >>sys.stderr, 'received "%s"' % data

        finally:
            print >>sys.stderr, 'closing socket'
            self.sock.close()

        

    # Takes a Class definition and returns changed
    # __dict__ for serialization.
    def marshalClass(self, c):
        d = {}
        for a, b in c.__dict__.items():
            if type(b) == types.FunctionType:
                d[a] = b.func_code
            elif type(b) == types.GetSetDescriptorType:
                pass
            else:
                d[a] = b
        return d

    def addClass(self, c):
        m = self.marshalClass(c)
        self.send(m)

class Test(object):
    def __init__(self, arg = 3):
        self.arg = arg

    def plus(self):
        self.arg += 1

# t = Test()

# print marshalClass(Test)
# m = marshal.dumps(marshalClass(Test))
# print m
# for i in range(len(m)):
#     a = m[i]
#     if a == "\0":
#         print a
#         print "NULL"

if __name__ == "__main__":
    p = PickleMonger()
    p.connect()
    p.send("test")








