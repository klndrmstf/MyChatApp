import socket
import threading
import time
import logging


logging.basicConfig(level=logging.ERROR)



class ModuleSocket:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class ModuleServer(ModuleSocket):
    def __init__(self) -> None:
        super().__init__()
        self.connection = None
        self.data = ""
        self.is_binded = False
        self.lock = threading.Lock()
        self.running = True

        self.task_connection_accept = threading.Thread(
            target=self.task_listen_and_accept,
            daemon=True
        )
        self.task_connection_accept.start()
        
        self.task_receive_thread = threading.Thread(
            target= self.task_receive,
            daemon=True
        )

        self.task_receive_thread.start()
    
    def task_listen_and_accept(self):
        while self.running:
            try:
                if self.is_binded:
                    self.socket.listen(1)
                    self.connection, addr = self.accept()
                    print(f"Conection received: {addr}")
                    self.task_receive_thread = threading.Thread(target=self.task_receive, daemon=True)
                    self.task_receive_thread.start()
            except Exception as e:
                logging.error(f"Error in listen_and_accept: {e}")
                time.sleep(0.01) 



    def bind_and_listen(self, host: str = "127.0.0.1", port:int=8765):
        # Server Bind
        print(f"Binding server to {host}:{port}")
        self.socket.bind((host, port))
        self.is_binded = True
        print("Listening...")
    
    def accept(self):
        # Server Accept
        return self.socket.accept()
    
    def send(self, msg):
        # Server Send
        if self.connection:
            try:
                self.connection.sendall(
                    msg.encode('utf-8')
                )
            except Exception as e:
                logging.error(f"Error recieving Message: {e}")
        
    def receive(self, connection):
        # Server Receive
        try:
            data = connection.recv(1024)
            return data.decode()

        except Exception as e:
                logging.error(f"Error recieving Message: {e}")
                      
    def task_receive(self):
        while True:
            data = self.receive(self.connection)
            if data:
                print(f"Client: {data}")
            else:
                print("Connection closed or no data received")
                break

    def server_serve(self, port:int=8765):
        print(f"Server serving on {port} port")
        self.bind_and_listen(host="127.0.0.1",port=port)
        while True:
            if self.connection:
            
                data = self.receive(self.connection)
                print("Client:", str(data))
                message = input(str("You: "))
                self.send(message)


class ModuleClient(ModuleSocket):
    
    def connect(self, host: str = "127.0.0.1", port:int=8765):
    # Client Connect
        self.socket.connect((host, port))
    
    def send(self, msg:str):
    # Client Send
        self.socket.sendall(msg.encode())
    
    def receivefrom(self):
        incoming_message = self.socket.recv(1024)
        incoming_message = incoming_message.decode()
        print(f"Server: {incoming_message}")

    def client_connect(self, host: str = "127.0.0.1", port:int=8765):
        self.connect(host=host,port=port)
        temp_input = ""
        while temp_input != "q":
            temp_input = input("You:")
            self.send(temp_input)
            self.receivefrom()

