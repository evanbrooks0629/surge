from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from handlers import proxy_handler


class AddProxyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 150, 400, 400)
        self.setMinimumSize(400, 400)
        self.setMaximumSize(400, 400)
        self.setStyleSheet(
            "font-family: 'Moon';"
            "background-color: #ffffff;"
        )
        self.setWindowTitle('Add Proxy')
        self.UI()

    def UI(self):
        self.layout = QVBoxLayout()
        self.mainLabel = QLabel("Add proxies below")
        self.mainLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.proxyBox = QTextEdit()
        self.proxyBox.setPlaceholderText("Copy and paste proxies here")
        self.proxyBox.setStyleSheet(
            "border: 2px solid #03c6fc;"
            "color: #000000;"
        )
        self.addProxyButton = QPushButton("＋    Add Proxies")
        self.addProxyButton.setStyleSheet(
            "color: #000000;"
            "font-size: 20px;"
            "font-weight: bold;"
            "background-color: #fc9803;"
            "padding: 10px 20px 10px 20px;"
            "border-radius: 5px;"
            "margin-bottom: 0px;"
        )
        self.layout.addWidget(self.mainLabel)
        self.layout.addWidget(self.proxyBox)
        self.layout.addWidget(self.addProxyButton)
        self.setLayout(self.layout)
        self.addProxyButton.clicked.connect(self.addProxy)
        self.show()

    def addProxy(self):
        can_add_proxy = True
        all_proxies = self.proxyBox.toPlainText()
        if len(all_proxies) > 0:
            try:
                all_proxies = all_proxies.split('\n')
            except:
                pass
            proxies_list = []
            for proxy in all_proxies:
                try:
                    proxy = proxy.split(':')
                    ip = proxy[0]
                    port = proxy[1]
                    new_proxy = []
                    new_proxy.append(port)
                    new_proxy.append(ip)
                    proxies_list.append(new_proxy)
                except:
                    pass
        else:
            can_add_proxy = False
            self.mainLabel.setText("Add proxies below*")
            self.mainLabel.setStyleSheet(
                "color: red;"
                "font-weight: bold;"
                "font-size: 15px;"
            )
        if can_add_proxy:
            all_proxies = proxy_handler.get_all_proxies()
            all_proxies += proxies_list
            proxy_handler.insert_proxies(all_proxies)
            self.close()
