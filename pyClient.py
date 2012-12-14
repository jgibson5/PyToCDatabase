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

        
    def send(self, command, c, instances = None, args = None, method = ""):
        wait=100
        self.connect()
        self.sock.connect(self.server_address)
        
        
        if instances == None: instances = []
        if args == None: args = {}
        try:
            # Send data
            m = [command, c, instances, args, method]
            t = pickle.dumps(m)
            self.waiting = 1
            self.sock.sendall(pickle.dumps(m))

            # Look for the response
            t0 = datetime.datetime.now()
            t1 = datetime.datetime.now()
            self.response = ""
            while ((t1 - t0).microseconds / 1000.0) + ((t1-t0).seconds * 1000.0) < wait:
                
                t1 = datetime.datetime.now()

                data = self.sock.recv(1024)
                if data != "":
                    self.response += data
                    t0 = t1
                    t1 = datetime.datetime.now()
                
            self.waiting = 0

        finally:
            
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

    def addClass(self, *cls):
        self.send("addClass", [self.marshalClass(c) for c in cls])

    def addInstances(self, c, *instances):
        self.send("addInstances", c, list(instances))

    def getInstances(self, c, *instances, **kwargs):
        self.send("getInstances", c, list(instances), kwargs)
        # while self.waiting:
        #     pass
        return pickle.loads(self.response)

    def removeClass(self, c):
        self.send("removeClass", c)

    def executeMethod(self, c, m, *instances, **args):
        self.send("executeMethod", c, list(instances), args, m)
        # while self.waiting:
        #     pass
        return pickle.loads(self.response)

    def changeAttr(self, c, attr, *instances, **args):
        self.send("changeAttr", c, list(instances), args)


def constructClass(m):
    d = marshal.loads(m)
    new = type('Test', (object,), d)
    name = new.__dict__['__name__']
    globals()[name] = new
    for k, v in new.__dict__.items():
        if type(v) == types.CodeType:
            setattr(new, k, types.FunctionType(v, globals(), k))
    return new

class Test(object):
    def __init__(self, arg = 3):
        self.arg = arg

    def plus(self):
        self.arg += 1



if __name__ == "__main__":
    p = PickleMonger()
    p.addClass(Test)
    t = Test(5)
    b = Test()
    p.addInstances(Test, t, b)

    r = p.getInstances(Test, "pass", arg=3)

    r = p.executeMethod(Test, "plus")

    








