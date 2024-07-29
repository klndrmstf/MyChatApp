import sys
import socket

sys.path.append("../QTCHATAPPNEW")

from Libraries.tools import validate_ip
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QTextEdit, QComboBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader



class LoginPage(QMainWindow):

    def __init__(self, client):
        super().__init__()
        print("Initializing Login Page...")
        self.client = client
        
        ent_ui_file = QFile("adress1.ui")
        ent_ui_file.open(QFile.ReadOnly)

        ent_loader = QUiLoader()
        ent_loaded_ui = ent_loader.load(ent_ui_file)
        ent_ui_file.close()
        print("UI file loaded.")

        self.setCentralWidget(ent_loaded_ui)

        self.enterButton = ent_loaded_ui.findChild(QPushButton, "enterbutton")
        # self.enterbutton
        self.userIP = ent_loaded_ui.findChild(QLineEdit, "user_IP")
        # self.user_IP
        self.userPort = ent_loaded_ui.findChild(QLineEdit, "user_Port")
        # self.user_Port
        self.otheruserIP = ent_loaded_ui.findChild(QLineEdit, "otheruser_IP")
        # self.otheruser_IP
        self.otheruserPort = ent_loaded_ui.findChild(QLineEdit, "otheruser_Port")
        # self.otheruser_Port

        self.userIP.setText("127.0.0.1")
        self.userIP.setReadOnly(True)

        self.userPort.setText("8765")

        self.enterButton.clicked.connect(self.enterButton_clicked)
        print("Login Page Initialized.")

    def enterButton_clicked(self):
        userIP = self.userIP.displayText()

        # ip regex 0-255.0-255.0-255.0-255
        otheruserIP = self.otheruserIP.displayText()
        is_otheruserIP_validation = validate_ip(otheruserIP)

        # port range 65535-0
        userPort = self.userPort.displayText()
        is_userPort_validation = userPort.isdigit() and int(userPort) < 65535 and 0 < int(userPort)

        otheruserPort = self.otheruserPort.displayText()
        is_otherUserPort_validation = otheruserPort.isdigit() and int(otheruserPort) < 65535 and 0 < int(otheruserPort)

        if is_otheruserIP_validation and is_userPort_validation and is_otherUserPort_validation:
            

            self.chatWindow = ChatPage(
                connection_ip=otheruserIP,
                connection_port=otheruserPort,
                local_ip=userIP,
                local_port=userPort,
                client = self.client
            )
            self.chatWindow.show()
            self.close()
        else:
            if not is_otheruserIP_validation:
                self.otheruserIP.clear()
                print("other user ip can not be validated.")
            if not is_otherUserPort_validation:
                self.otheruserPort.clear()
                print("other user port can not be validated.")
            if not is_userPort_validation:
                self.userPort.clear()
                print("user port can not be validated.")

class ChatPage(QMainWindow):
    
    def __init__(self, 
            connection_ip,
            connection_port,
            local_ip,
            local_port,
            client
        ):
        super().__init__()
        print("Initializing Chat Page...")
        self.connection_ip = connection_ip
        self.connection_port = connection_port
        self.local_ip = local_ip
        self.local_port = local_port
        self.client = client
        
        self.setGeometry(400,200,600,600)
        
        ui_file = QFile("myqtchatapp.ui")
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        loaded_ui = loader.load(ui_file)
        ui_file.close()

        self.setCentralWidget(loaded_ui)

        self.msgBar = loaded_ui.findChild(QLineEdit, "msg_bar")
        self.msgHistory = loaded_ui.findChild(QTextEdit, "msg_history")
        self.sentButton = loaded_ui.findChild(QPushButton, "sent_button")
        self.profileBox = loaded_ui.findChild(QComboBox, "my_profile_box")
        self.clientButton = loaded_ui.findChild(QPushButton, "clientbutton")

        self.sentButton.setEnabled(False)
        self.sentButton.clicked.connect(self.button_clicked)
        print("Chat Page Initialized.")


    def action_connect(self):
        try:
            self.client.connect(
                host=self.connection_ip,
                port=self.connection_port
            )
            self.sentButton.setEnabled(True)
            # TODO: Unlock send buton*
        except Exception as error:
            print(f"Error: {error}")


    def button_clicked(self):
        
        hostname = socket.gethostname()
        
        user_msg = self.msgBar.text()
        
        # TODO: Change the local ip as local network ip such as 192.168.x.x*
        formated_msg = f"{hostname}: {user_msg}"
        self.client.send(
            msg=formated_msg
        )

        self.msgHistory.append(formated_msg)
        self.msgBar.clear()
