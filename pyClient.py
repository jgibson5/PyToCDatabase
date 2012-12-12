import socket
import sys
import marshal
import types

# Takes a Class definition and returns changed
# __dict__ for serialization.
def marshalClass(c):
    d = {}
    for a, b in c.__dict__.items():
        if type(b) == types.FunctionType:
            d[a] = b.func_code
        elif type(b) == types.GetSetDescriptorType:
            pass
        else:
            d[a] = b
    return d


class Test(object):
    def __init__(self, arg = 3):
        self.arg = arg

    def plus(self):
        self.arg += 1

t = Test()

print t.__dict__
print Test.__dict__
print marshalClass(Test)
m = marshal.dumps(marshalClass(Test))

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 80)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    # Send data
    sock.sendall(m)

    # Look for the response
    # amount_received = 0
    # amount_expected = len(message)
    
    # while amount_received < amount_expected:
    #     data = sock.recv(32)
    #     amount_received += len(data)
    #     print >>sys.stderr, 'received "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()



