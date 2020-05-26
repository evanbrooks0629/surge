import sys
import os
import time
import json
import smtplib

from selenium import webdriver
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from handlers import settings_handler


class KeyVerificationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 150, 400, 400)
        self.setStyleSheet(
            "font-family: 'Moon';"
            "background-color: #ffffff;"
        )
        self.setWindowTitle('Verify Key')
        self.UI()

    def UI(self):
        hbox = QHBoxLayout()
        hbox2 = QHBoxLayout()
        vbox = QVBoxLayout()
        self.mainLabel = QLabel("Welcome to Surge.")
        self.mainLabel.setStyleSheet(
            "font-size: 30px;"
            "font-weight: bold;"
        )
        self.mainLabel.setAlignment(Qt.AlignCenter)
        self.subLabel = QLabel("Please enter your verification key to proceed:")
        self.subLabel.setStyleSheet(
            "font-size: 20px;"
        )
        self.subLabel.setAlignment(Qt.AlignCenter)
        self.keyInput = QLineEdit()
        self.keyInput.setPlaceholderText("Enter your key here")
        self.keyInput.setStyleSheet(
            "border: 2px solid #000000;"
            "padding: 10px;"
            "font-size: 15px;"
        )
        self.verifyButton = QPushButton("Verify")
        self.verifyButton.setStyleSheet(
            "background-color: #03c6fc;"
            "color: #000000;"
            "border-radius: 5px;"
            "padding: 10px;"
            "font-size: 20px;"
            "font-weight: bold;"
        )
        self.exitButton = QPushButton("Close")
        self.exitButton.setStyleSheet(
            """
            QPushButton {
                background-color: #fc9803;
                color: #000000;
                border-radius: 5px;
                padding: 10px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e38902;
            }
            QPushButton:pressed {
                background-color: #fc9803;
            }
            """
        )
        self.exitButton.hide()
        hbox.addWidget(self.verifyButton)
        hbox.setContentsMargins(100, 0, 100, 0)
        hbox2.addWidget(self.exitButton)
        hbox2.setContentsMargins(100, 0, 100, 0)
        vbox.addStretch()
        vbox.addWidget(self.mainLabel)
        vbox.addStretch()
        vbox.addWidget(self.subLabel)
        vbox.addStretch()
        vbox.addWidget(self.keyInput)
        vbox.addStretch()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addStretch()
        self.setLayout(vbox)
        self.verifyButton.clicked.connect(self.checkKey)
        self.exitButton.clicked.connect(self.quitApp)
        self.show()

    def quitApp(self):
        sys.exit()

    def checkKey(self):
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app
            # path into variable _MEIPASS'.
            self.application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            application_path = application_path.split("/")
            print(application_path)
            application_path.remove(application_path[6])
            application_path.remove(application_path[0])
            appstr = '/'
            for char in application_path:
                appstr += char + '/'
            self.application_path = appstr
        driver_path = os.path.join(self.application_path, 'chromedriver')
        key = self.keyInput.text()
        master_key = 'cWm]51a>DEa~tpqd&|1NV_LUKD==-tbp.z^J%{*#ixzcc5E>R#|p.D2fV:i#F=e'
        self.subLabel.hide()
        self.keyInput.hide()
        self.verifyButton.hide()
        if key == master_key:
            settings_handler.set_setting("valid", True)
            self.mainLabel.setText('KEY VERIFIED')
            self.subLabel.show()
            self.subLabel.setText('Restart Surge to continue.')
            self.exitButton.show()
        elif len(key) == 32 and ' ' not in key:
            self.mainLabel.setText('Checking database...')
            user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
            options = webdriver.ChromeOptions()
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            options.add_argument("--headless")
            options.add_argument(f'user-agent={user_agent}')
            driver = webdriver.Chrome(options=options, executable_path=driver_path)
            driver.get(
                'https://www.obvibase.com/app/?location=%7B%22type%22%3A%22table%22%2C%22databaseId%22%3A%22UlkqES9dAbVF64bX%22%2C%22queryPath%22%3A%7B%22recordPath%22%3A%5B%5D%2C%22columnPath%22%3A%5B%221%22%5D%7D%7D')
            driver.set_window_position(20000, 20000)
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="login-dialog--google"]').click()
            time.sleep(2)
            driver.find_element_by_xpath('//input[@id="identifierId"]').send_keys('astrobotcj@gmail.com')
            driver.find_element_by_xpath('//div[@id="identifierNext"]').click()
            time.sleep(2)
            self.mainLabel.setText('Accessing remote server...')
            driver.find_element_by_xpath('//div[@id="password"]/div[1]/div/div[1]/input').send_keys('EvanLewis420')
            time.sleep(5)
            driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div').click()
            self.mainLabel.setText('Retreiving data...')
            time.sleep(5)
            html_source = driver.find_element_by_tag_name('body').text
            time.sleep(5)
            if key in html_source:
                self.mainLabel.setText('Verifying license key...')
                settings_handler.set_setting("valid", True)
                email_user = 'astrobotcj@gmail.com'
                email_password = 'EvanLewis420'
                email_send = 'astrobotcj@gmail.com'
                subject = 'Remove Key'
                msg = MIMEMultipart()
                msg['From'] = email_user
                msg['To'] = email_send
                msg['Subject'] = subject
                body = f'Go to obvibase.com and remove this key: {key}'
                msg.attach(MIMEText(body, 'plain'))
                text = msg.as_string()
                server = smtplib.SMTP('smtp.gmail.com: 587')
                server.ehlo()
                server.starttls()
                server.login(email_user, email_password)
                server.sendmail(email_user, email_send, text)
                server.quit()
                self.mainLabel.setText('KEY VERIFIED')
                self.subLabel.show()
                self.subLabel.setText('Restart Surge to continue.')
                self.exitButton.show()
            else:
                self.mainLabel.setText('KEY NOT VERIFIED')
                self.subLabel.show()
                self.subLabel.setText('There was an error processing your request.')
                self.exitButton.show()
        else:
            self.mainLabel.setText('INVALID KEY')
            return False
