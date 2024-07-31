from View import ChatPage, LoginPage
from module_socket import ClientConnect
from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    entranceapp = QApplication(sys.argv)
    window = LoginPage(shared_buffer= any)
    window.show()
    sys.exit(entranceapp.exec())

connection_ip = "127.0.0.1"
connection_port = 9999
client = ClientConnect()

client.client_connect(
    host=connection_ip,
    port=connection_port
)
