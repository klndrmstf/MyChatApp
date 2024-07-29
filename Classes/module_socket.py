import socket
import threading
import time



class ModuleSocket:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class ModuleServer(ModuleSocket):
    def __init__(self) -> None:
        super().__init__()
        self.connection = None
        self.data = ""
        self.is_binded = False

        self.task_connection_acept = threading.Thread(
            target=self.task_listen_and_accept,
            daemon=True
        )
        self.task_connection_acept.start()
        
        self.task_recieve_thread = threading.Thread(
            target= self.task_recieve,
            daemon=True
        )

        self.task_recieve_thread.start()
    
    def task_listen_and_accept(self):
        while True:
            if self.is_binded:
                self.socket.listen(1)
                self.connection, addr = self.accept()
                print(f"Conection receiver: {addr}")
            time.sleep(0.01)


    def bind_and_listen(self, host: str = "127.0.0.1", port:int=8765):
        # Server Bind
        print(f"Binding server to {host}:{port}")
        self.socket.bind((host, port))
        self.socket.listen(1)
        self.is_binded = True
        print("Listening...")
    
    def accept(self):
        # Server Accept
        connection, addr = self.socket.accept()
        return connection, addr
    
    def send(self, msg):
        # Server Send
        if self.connection is not None:
            self.connection.sendall(
                msg.encode('utf-8')
            )
        else:
            print("No connection.")
        
    def recieve(self, connection):
        # Server Receive
        data = connection.recv(1024)
        data = data.decode()
        return data
    
    def task_recieve(self):
        while True:
            if self.connection is not None and self.is_binded:
                self.data = self.recieve(
                    connection= self.connection
                )
            time.sleep(0.01)
    
    def send_to(self, connection, msg):
        # Server Send
        connection.sendall(msg.encode('utf-8'))
    
    def server_serve(self, port:int=8765):
        print(f"Server serving on {port} port")
        self.bind_and_listen(host="127.0.0.1",port=port)
    
        connection, address = self.accept()
        print("Connection received from", address)
        while True:
            data = self.recieve(connection)
            print("Client:", str(data))
            message = input(str("You: "))
            message = message.encode()
            connection.send(message)


class ModuleClient(ModuleSocket):
    
    def connect(self, host: str = "127.0.0.1", port:int=8765):
    # Client Connect
        self.socket.connect((host, port))
    
    def send(self, msg:str):
    # Client Send
        self.socket.sendall(msg.encode())
    
    def recievefrom(self):
        incoming_message = self.socket.recv(1024)
        incoming_message = incoming_message.decode()
        print(f"Server: {incoming_message}")

    def client_connect(self, host: str = "127.0.0.1", port:int=8765):
        self.connect(host=host,port=port)
        temp_input = ""
        while temp_input != "q":
            temp_input = input("You:")
            self.send(temp_input)
            self.recievefrom()

