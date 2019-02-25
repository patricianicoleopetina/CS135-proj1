import socket
import sys
import select

message = None

class BasicClient(object):

    def __init__(self, name, address, port):
        self.address = address
        self.port = int(port)
        self.name = name
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(2)
        self.socket.connect((self.address, self.port))
        
    def send(self, message):
        
        self.socket.send(message)
    
    def recv(self):
        response = self.socket.recv(1024)
        return response
    
    def get_socket(self):
        return self.socket


def main(argv):
    args = sys.argv
    if len(args) != 4:
        print "Please supply a client name, server address and port."
        sys.exit()
    client = BasicClient(args[1], args[2], args[3])
    
    run(client)
    
    return

def run(client):
    s = client.get_socket()
    client.send("/name"+client.name)

    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(1024)
                if not data:
                    print '\nDisconnected from chat server'
                    sys.exit()
                else:
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] ');
                    sys.stdout.flush()
            else:
                # user entered a message
                send_request(client)
                
             
    return

def send_request(client):
    msg = sys.stdin.readline()

    if msg.startswith("/create"):
        msg = msg.replace("/create", "/create["+client.name+"]")
    elif msg.startswith("/join"):
        msg = msg.replace("/join", "/join[" + client.name + "]")

    client.send(msg)
            
    sys.stdout.write('[Me] ');
    sys.stdout.flush()
    return

if __name__ == '__main__':main( sys.argv[1:2])