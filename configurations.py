import sys
from Classes.View import LoginPage 
from Classes.module_socket import ModuleClient, ModuleServer
from PySide6.QtWidgets import QApplication

qapp = QApplication(sys.argv)

print("Configurations are setting...")

server = ModuleServer()
server.bind_and_listen(port=8765)


client = ModuleClient()

app = LoginPage(client, server)
print("Configurations are setten.")

