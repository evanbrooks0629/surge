from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from handlers import proxy_handler

import sys, os


class EditProxyWindow(QWidget):
    def __init__(self, index, port, ip):
        self.index = index
        self.port = port
        self.ip = ip
        super().__init__()
        self.setGeometry(400, 150, 400, 150)
        self.setMinimumSize(400, 150)
        self.setMaximumSize(400, 150)
        self.setStyleSheet(
            "font-family: 'Moon';"
            "background-color: #ffffff;"
        )
        self.setWindowTitle('Edit Proxy')
        self.UI()

    def UI(self):
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app
            # path into variable _MEIPASS'.
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            application_path = application_path.split("/")
            application_path.remove(application_path[6])
            application_path.remove(application_path[0])
            appstr = '/'
            for char in application_path:
                appstr += char + '/'
            application_path = appstr
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        self.portLabel = QLabel("Port")
        self.portLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold"
        )
        self.portInput = QLineEdit()
        self.portInput.setPlaceholderText("Enter a port")
        self.portInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.portInput.setText(self.port)
        layout.addWidget(self.portLabel, 0, 0)
        layout.addWidget(self.portInput, 0, 1, 1, 2)
        self.ipLabel = QLabel("IP Address")
        self.ipLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold"
        )
        self.ipInput = QLineEdit()
        self.ipInput.setPlaceholderText("Enter an IP address")
        self.ipInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.ipInput.setText(self.ip)
        layout.addWidget(self.ipLabel, 1, 0)
        layout.addWidget(self.ipInput, 1, 1, 1, 2)
        self.editProxyButton = QPushButton("    Edit Proxy")
        img_path = os.path.join(application_path, 'images/iconeditblack.icns')
        self.editProxyButton.setIcon(QIcon(img_path))
        self.editProxyButton.setStyleSheet(
            "color: #000000;"
            "font-size: 20px;"
            "font-weight: bold;"
            "background-color: #fc9803;"
            "padding: 10px 20px 10px 20px;"
            "border-radius: 5px;"
            "margin-bottom: 0px;"
        )
        layout.addWidget(self.editProxyButton, 2, 0, 1, 3)
        self.setLayout(layout)
        self.editProxyButton.clicked.connect(self.editProxy)
        self.show()

    def editProxy(self):
        can_add_proxy = True
        port = self.portInput.text()
        if len(port) == 0:
            self.portLabel.setText("Port*")
            self.portLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
        ip = self.ipInput.text()
        if len(ip) == 0:
            self.ipLabel.setText("IP Address*")
            self.ipLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
        if can_add_proxy:
            all_proxies = proxy_handler.get_all_proxies()
            proxy = all_proxies[self.index]
            proxy[0] = port
            proxy[1] = ip
            proxy_handler.insert_proxies(all_proxies)

            self.close()
