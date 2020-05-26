from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from handlers import account_handler

import sys, os


class EditAccountsWindow(QWidget):
    def __init__(self, index, first, last, email, phone, street, city, state, zip, number, exp, cvv, name, billingStreet, billingCity, billingState, billingZip):
        super().__init__()
        self.index = index
        self.first = first
        self.last = last
        self.email = email
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.number = number
        self.exp = exp
        self.cvv = cvv
        self.name = name
        self.billingStreet = billingStreet
        self.billingCity = billingCity
        self.billingState = billingState
        self.billingZip = billingZip
        self.setGeometry(300, 150, 800, 400)
        self.setMinimumSize(800, 400)
        self.setMaximumSize(800, 400)
        self.setStyleSheet(
            "font-family: 'Moon';"
            "background-color: #ffffff;"
        )
        self.setWindowTitle('Edit Account')
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
        self.mainLayout = QVBoxLayout()
        self.mainBody = QHBoxLayout()
        self.accountLayout = QGridLayout()
        self.accountLayout.setColumnStretch(1, 4)
        self.accountLayout.setColumnStretch(2, 4)

        self.profileLabel = QLabel("Account Profile")
        self.profileLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 20px;"
            "font-weight: bold;"
        )
        self.accountLayout.addWidget(self.profileLabel, 1, 0)

        self.firstNameLabel = QLabel("First Name")
        self.firstNameLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.firstNameInput = QLineEdit()
        self.firstNameInput.setPlaceholderText("First Name")
        self.firstNameInput.setText(self.first)
        self.firstNameInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.accountLayout.addWidget(self.firstNameLabel, 2, 0)
        self.accountLayout.addWidget(self.firstNameInput, 2, 1, 1, 2)

        self.lastNameLabel = QLabel("Last Name")
        self.lastNameLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.lastNameInput = QLineEdit()
        self.lastNameInput.setPlaceholderText("Last Name")
        self.lastNameInput.setText(self.last)
        self.lastNameInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.accountLayout.addWidget(self.lastNameLabel, 3, 0)
        self.accountLayout.addWidget(self.lastNameInput, 3, 1, 1, 2)

        self.emailLabel = QLabel("Email Address")
        self.emailLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.emailInput = QLineEdit()
        self.emailInput.setPlaceholderText("user@email.com")
        self.emailInput.setText(self.email)
        self.emailInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.accountLayout.addWidget(self.emailLabel, 4, 0)
        self.accountLayout.addWidget(self.emailInput, 4, 1, 1, 2)

        self.phoneLabel = QLabel("Phone Number")
        self.phoneLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.phoneInput = QLineEdit()
        self.phoneInput.setPlaceholderText("xxx-xxx-xxxx")
        self.phoneInput.setText(self.phone)
        self.phoneInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.accountLayout.addWidget(self.phoneLabel, 5, 0)
        self.accountLayout.addWidget(self.phoneInput, 5, 1, 1, 2)

        self.accountAddressLabel = QLabel("Address")
        self.accountAddressLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 15px;"
            "font-weight: bold;"
            "padding: 0px;"
        )
        self.accountLayout.addWidget(self.accountAddressLabel, 6, 0)

        self.streetLabel = QLabel("Street")
        self.streetLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.streetInput = QLineEdit()
        self.streetInput.setPlaceholderText("1234 N 99th St")
        self.streetInput.setText(self.street)
        self.streetInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.accountLayout.addWidget(self.streetLabel, 7, 0)
        self.accountLayout.addWidget(self.streetInput, 7, 1, 1, 2)

        self.cityLabel = QLabel("City")
        self.cityLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.cityInput = QLineEdit()
        self.cityInput.setPlaceholderText("City Name")
        self.cityInput.setText(self.city)
        self.cityInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.accountLayout.addWidget(self.cityLabel, 8, 0)
        self.accountLayout.addWidget(self.cityInput, 8, 1, 1, 2)

        self.stateLabel = QLabel("State")
        self.stateLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.stateInput = QComboBox()
        self.stateInput.addItems(
            ['Select State', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
             'KS', 'KY', 'LA',
             'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
             'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])
        self.stateInput.setStyleSheet(
            """
            QComboBox {
                color: #000000;
                border: 1px solid #03c6fc;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
            }

            QComboBox:editable {
                color: #000000;
                background-color: white;
            }

            QComboBox:!editable, QComboBox::drop-down:editable {
                 color: #000000;
                 background-color: #03c6fc;
            }

            QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                color: #000000;
                background-color: #03c6fc;
            }

            QComboBox:on { 
                color: #000000;
                padding-top: 3px;
                padding-left: 4px;
            }

            QComboBox::drop-down {
                color: #000000;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;

                border-left-width: 1px;
                border-left-color: #03c6fc;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(images/downArrowIcon.png);
                left: -5px;
            }
            QComboBox::down-arrow:on {
                color: #000000;
                left: -5px;
            }
            """
        )
        self.stateInput.setCurrentText(self.state)
        self.accountLayout.addWidget(self.stateLabel, 9, 0)
        self.accountLayout.addWidget(self.stateInput, 9, 1, 1, 2)

        self.zipLabel = QLabel("Zip Code")
        self.zipLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.zipInput = QLineEdit()
        self.zipInput.setPlaceholderText("12345")
        self.zipInput.setText(self.zip)
        self.zipInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.accountLayout.addWidget(self.zipLabel, 10, 0)
        self.accountLayout.addWidget(self.zipInput, 10, 1, 1, 2)

        self.billingLayout = QGridLayout()
        self.billingLayout.setColumnStretch(1, 4)
        self.billingLayout.setColumnStretch(2, 4)

        self.billingLabel = QLabel("Billing Profile")
        self.billingLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 20px;"
            "font-weight: bold;"
        )
        self.billingLayout.addWidget(self.billingLabel, 1, 0)

        self.cardNumberLabel = QLabel("Card Number")
        self.cardNumberLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.cardNumberInput = QLineEdit()
        self.cardNumberInput.setPlaceholderText("CC Number")
        self.cardNumberInput.setText(self.number)
        self.cardNumberInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.billingLayout.addWidget(self.cardNumberLabel, 2, 0)
        self.billingLayout.addWidget(self.cardNumberInput, 2, 1, 1, 2)

        self.expLabel = QLabel("Expiration Date")
        self.expLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.expInput = QLineEdit()
        self.expInput.setPlaceholderText("MM/YY")
        self.expInput.setText(self.exp)
        self.expInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.billingLayout.addWidget(self.expLabel, 3, 0)
        self.billingLayout.addWidget(self.expInput, 3, 1, 1, 2)

        self.cvvLabel = QLabel("CVV")
        self.cvvLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.cvvInput = QLineEdit()
        self.cvvInput.setPlaceholderText("123")
        self.cvvInput.setText(self.cvv)
        self.cvvInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.billingLayout.addWidget(self.cvvLabel, 4, 0)
        self.billingLayout.addWidget(self.cvvInput, 4, 1, 1, 2)

        self.nameLabel = QLabel("Name on Card")
        self.nameLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("John Smith")
        self.nameInput.setText(self.name)
        self.nameInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.billingLayout.addWidget(self.nameLabel, 5, 0)
        self.billingLayout.addWidget(self.nameInput, 5, 1, 1, 2)

        self.sameAdressLabel = QLabel("Use same Address for billing")
        self.sameAdressLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 15px;"
            "font-weight: bold;"
            "padding-top: 5px;"
            "padding-bottom: 5px;"
        )
        self.sameAdressLabel.setAlignment(Qt.AlignCenter)
        self.billingCheckbox = QCheckBox()
        self.billingLayout.addWidget(self.sameAdressLabel, 6, 0)
        self.billingLayout.addWidget(self.billingCheckbox, 6, 1)

        if self.street == self.billingStreet and self.city == self.billingCity and self.state == self.billingState and self.zip == self.billingZip:
            self.billingCheckbox.setChecked(True)
        else:
            self.billingCheckbox.setChecked(False)

        self.billingStreetLabel = QLabel("Street")
        self.billingStreetLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.billingStreetInput = QLineEdit()
        self.billingStreetInput.setPlaceholderText("1234 N 99th St")
        self.billingStreetInput.setText(self.billingStreet)
        self.billingStreetInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.billingLayout.addWidget(self.billingStreetLabel, 7, 0)
        self.billingLayout.addWidget(self.billingStreetInput, 7, 1, 1, 2)

        self.billingCityLabel = QLabel("City")
        self.billingCityLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.billingCityInput = QLineEdit()
        self.billingCityInput.setPlaceholderText("City Name")
        self.billingCityInput.setText(self.billingCity)
        self.billingCityInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.billingLayout.addWidget(self.billingCityLabel, 8, 0)
        self.billingLayout.addWidget(self.billingCityInput, 8, 1, 1, 2)

        self.billingStateLabel = QLabel("State")
        self.billingStateLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.billingStateInput = QComboBox()
        self.billingStateInput.addItems(
            ['Select State', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
             'KS', 'KY', 'LA',
             'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
             'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])
        self.billingStateInput.setStyleSheet(
            """
            QComboBox {
                color: #000000;
                border: 1px solid #03c6fc;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
            }

            QComboBox:editable {
                color: #000000;
                background-color: white;
            }

            QComboBox:!editable, QComboBox::drop-down:editable {
                 color: #000000;
                 background-color: #03c6fc;
            }

            QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                color: #000000;
                background-color: #03c6fc;
            }

            QComboBox:on { 
                color: #000000;
                padding-top: 3px;
                padding-left: 4px;
            }

            QComboBox::drop-down {
                color: #000000;
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;

                border-left-width: 1px;
                border-left-color: #03c6fc;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(images/downArrowIcon.png);
                left: -5px;
            }
            QComboBox::down-arrow:on {
                color: #000000;
                left: -5px;
            }
            """
        )
        self.billingStateInput.setCurrentText(self.billingState)
        self.billingLayout.addWidget(self.billingStateLabel, 9, 0)
        self.billingLayout.addWidget(self.billingStateInput, 9, 1, 1, 2)

        self.billingZipLabel = QLabel("Zip Code")
        self.billingZipLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.billingZipInput = QLineEdit()
        self.billingZipInput.setPlaceholderText("12345")
        self.billingZipInput.setText(self.billingZip)
        self.billingZipInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        self.billingLayout.addWidget(self.billingZipLabel, 10, 0)
        self.billingLayout.addWidget(self.billingZipInput, 10, 1, 1, 2)

        self.mainBody.addLayout(self.accountLayout)
        self.mainBody.addLayout(self.billingLayout)

        self.buttonBox = QHBoxLayout()
        self.editAccountsButton = QPushButton("    Edit Account")
        self.editAccountsButton.setStyleSheet(
            """
            QPushButton {
                background-color: #fc9803;
                color: #000000;
                border-radius: 5px;
                padding: 10px 20px 10px 20px;
                font-weight: bold;
                font-size: 20px;
                margin-bottom: 0px;
            }
            QPushButton::hover {
                background-color: #e38902;
            }
            QPushButton:pressed {
                background-color: #fc9803;
            }
            """
        )
        img_path = os.path.join(application_path, 'images/iconeditblack.icns')
        self.editAccountsButton.setIcon(QIcon(img_path))
        self.buttonBox.addStretch()
        self.buttonBox.addWidget(self.editAccountsButton)
        self.buttonBox.addStretch()
        self.mainLayout.addLayout(self.mainBody)
        self.mainLayout.addLayout(self.buttonBox)
        self.mainLayout.setStretch(1, 2)
        self.setLayout(self.mainLayout)

        self.setVisibility()
        self.billingCheckbox.toggled.connect(self.setVisibility)
        self.editAccountsButton.clicked.connect(self.editAccount)

        self.show()

    def editAccount(self):
        new_first = self.firstNameInput.text()
        new_last = self.lastNameInput.text()
        new_email = self.emailInput.text()
        new_phone = self.phoneInput.text()
        new_street = self.streetInput.text()
        new_city = self.cityInput.text()
        new_state = self.stateInput.currentText()
        new_zip = self.zipInput.text()
        new_number = self.cardNumberInput.text()
        new_exp = self.expInput.text()
        new_cvv = self.cvvInput.text()
        new_name = self.nameInput.text()
        new_billingStreet = self.billingStreetInput.text()
        new_billingCity = self.billingCityInput.text()
        new_billingState = self.billingStateInput.currentText()
        new_billingZip = self.billingZipInput.text()

        if self.billingCheckbox.isChecked():
            new_billingStreet = new_street
            new_billingCity = new_city
            new_billingState = new_state
            new_billingZip = new_zip
        accounts = account_handler.get_all_accounts()
        new_account = [new_first, new_last, new_email, new_phone, new_street, new_city, new_state, new_zip, new_number, new_exp, new_cvv, new_name, new_billingStreet, new_billingCity, new_billingState, new_billingZip]
        accounts[self.index] = new_account
        account_handler.insert_accounts(accounts)
        self.close()

    def setVisibility(self):
        if self.billingCheckbox.isChecked():
            self.billingStreetLabel.setStyleSheet(
                "color: #ffffff;"
            )
            self.billingStreetInput.hide()
            self.billingCityLabel.setStyleSheet(
                "color: #ffffff;"
            )
            self.billingCityInput.hide()
            self.billingStateLabel.setStyleSheet(
                "color: #ffffff;"
            )
            self.billingStateInput.hide()
            self.billingZipLabel.setStyleSheet(
                "color: #ffffff;"
            )
            self.billingZipInput.hide()
        else:
            self.billingStreetLabel.setStyleSheet(
                "color: #000000;"
            )
            self.billingStreetInput.show()
            self.billingCityLabel.setStyleSheet(
                "color: #000000;"
            )
            self.billingCityInput.show()
            self.billingStateLabel.setStyleSheet(
                "color: #000000;"
            )
            self.billingStateInput.show()
            self.billingZipLabel.setStyleSheet(
                "color: #000000;"
            )
            self.billingZipInput.show()