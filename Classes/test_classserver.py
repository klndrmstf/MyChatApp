from View import ChatPage, LoginPage
from module_socket import ServerServe
from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    entranceapp = QApplication(sys.argv)
    window = LoginPage(shared_buffer= any)
    window.show()
    sys.exit(entranceapp.exec())

server_ip = "127.0.0.1"
server_port = 9999
server = ServerServe()
server.server_serve(port=server_port)