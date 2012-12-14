import socket
import sys
import marshal
import pickle
import types
import PickleMonger

class PickleMongerServer(object):
    """docstring for PickleMongerServer"""
    def __init__(self):
        self.PickleMonger = PickleMonger.PickleMonger(newDB = 1)

    def connect(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        self.server_address = ('localhost', 80)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.sock.bind(self.server_address)

        # Listen for incoming connections
        self.sock.listen(1)

    def listen(self):
        while True:
            # Wait for a connection
            
            self.connection, self.client_address = self.sock.accept()
            
            try:
                

                # Receive the data in small chunks and retransmit it
                while True:
                    data = self.connection.recv(8096)
                    
                    if data:
                        try:
                            data = pickle.loads(data)
                        except Exception as e:
                            name = e.__str__().split("'")[-2]
                            globals()[name] = self.PickleMonger.constructClass(self.PickleMonger.classDB[name])
                            data = pickle.loads(data)
                        
                        cmd = data[0]
                        if cmd == "addClass":
                            cls = (self.PickleMonger.constructClass(cl) for cl in data[1])
                            for cl in data[1]:
                                t = self.PickleMonger.constructClass(cl)
                            self.PickleMonger.addClass(*cls)
                            self.connection.sendall("SUCCESS")
                        elif cmd == "addInstances":
                            self.PickleMonger.addInstance(data[1], data[2])

                        elif cmd == "getInstances":
                            ret = self.PickleMonger.get(data[1], data[2], data[3])
                            self.connection.sendall(pickle.dumps(ret))
                            
                        elif cmd == "removeClass":
                            pass
                        elif cmd == "executeMethod":
                            cl = data[1]
                            ins = data[2]
                            kws = data[3]
                            method = data[4]
                            res = self.PickleMonger.executeMethod(cl, method, ins, kws)
                            self.connection.sendall(pickle.dumps(res))
                        elif cmd == "changeAttr":
                            pass
                        else:
                            self.connection.sendall("NOT A VALID COMMAND")
                        break
                    else:
                        
                        break
                    
            finally:
                # Clean up the connection
                self.connection.close()
        

    

if __name__ == "__main__":
    p = PickleMongerServer()
    p.connect()
    p.listen()




