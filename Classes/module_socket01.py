import socket
import threading
import time



class ModuleSocket:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class ModuleServer(ModuleSocket):
    
    def bind_and_listen(self, host: str = "127.0.0.1", port:int=8765):
        # Server Bind
        self.socket.bind((host, port))
        self.socket.listen(1)
    
    def accept(self):
        # Server Accept
        connection, addr = self.socket.accept()
        return connection, addr
    
    def send(self, connection, msg):
        # Server Send
        connection.sendall(
            msg.encode('utf-8')
        )
        
    def recieve(self, connection):
        # Server Receive
        data = connection.recv(1024)
        return data
    
    def recieve_from(self, connection):
        # Server Receive
        data = connection.recv(1024)
        return data
    
    def send_to(self, connection, msg):
        # Server Send
        connection.sendall(msg.encode('utf-8'))
    
class ServerServe(ModuleServer):

    def server_serve(self, port:int=8765):
        self.bind_and_listen(
        host="127.0.0.1",
        port=port
        )
    
        connection, address = self.accept()
        print("Connection received from", address)
        while True:
            message = input(str("Waiting Message to Send:"))
            message = message.encode()
            connection.send(message)
            print(f"You: {message}")
            data = self.recieve_from(connection)
            print("Data:", data)
            self.send_to(
                connection=connection,
                msg=f"=> OK:{data} <="
            )


class ModuleClient(ModuleSocket):
    
    def connect(self, host: str = "127.0.0.1", port:int=8765):
    # Client Connect
        self.socket.connect((host, port))
    
    def send(self, msg:str):
    # Client Send
        self.socket.sendall(
        msg.encode('utf-8')
        )

    def recieve(self):
    # Client Receive0
        data = self.socket.recv(1024)
    # print(f'received event: "{event[0]}" with arguments {event[1:]}')
        return data


    

class ClientConnect(ModuleClient):

    def client_connect(self, host: str = "127.0.0.1", port:int=8765):
        self.connect(host=host,port=port)
        temp_input = ""
        while temp_input != "q":
            message = self.recieve(1024)
            print(f"server:{message}")
            temp_input = input("Waiting message to send:")
            self.send(temp_input)
            message = self.recieve()
            print("Server Message:", message)





        




    """ def bind_listen(self, host: str = "127.0.0.1", port:int=8765):
        # Server Bind
        self.socket.bind((host, port))
        self.socket.listen(1)

    def connect(self, host: str = "127.0.0.1", port:int=8765):
        # Client Connect
        self.socket.connect((host, port))
  
    def accept(self):
        # Server Accept
        connection, addr = self.socket.accept()
        return connection, addr

    def send(self, msg:str):
        # Client Send
        self.socket.sendall(
            msg.encode('utf-8')
        )

    def send_to(self, connection, msg):
        # Server Send
        connection.sendall(
            msg.encode('utf-8')
        )

    def recieve(self):
        # Client Receive
        data = self.socket.recv(1024)
        # print(f'received event: "{event[0]}" with arguments {event[1:]}')
        return data

    def recieve_from(self, connection):
        # Server Receive
        data = connection.recv(1024)
        return data
    
    def server_serve(self, port:int=8765):
        self.bind_listen(
            host="127.0.0.1",
            port=port
        )
        connection, address = self.accept()
        print("Connection received from", address)
        while True:
            data = self.recieve_from(connection)
            print("Data:", data)
            self.send_to(
                connection=connection,
                msg=f"=> OK:{data} <="
            )

    def client_connect(self, host: str = "127.0.0.1", port:int=8765):
        self.connect(
            host=host,
            port=port
        )
        temp_input = ""
        while temp_input != "q":
            temp_input = input("Waiting message to send:")
            self.send(
                temp_input
            )
            message = self.recieve()
            print("Server Message:", message)
    
    def task(self, host: str = "127.0.0.1", port:int=8765):
        self.connect(
            host=host,
            port=port
        )
        temp_input = ""
        while temp_input != "q":
            temp_input = input("Waiting message to send:")
            self.send(
                temp_input
            )
            message = self.recieve()
            print("Server Message:", message)"""