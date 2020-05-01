from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from handlers import account_handler


class AddAccountsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 150, 800, 400)
        self.setMinimumSize(800, 400)
        self.setMaximumSize(800, 400)
        self.setStyleSheet(
            "font-family: 'Moon';"
            "background-color: #ffffff;"
        )
        self.setWindowTitle('Add Account')
        self.UI()

    def UI(self):
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

        self.billingStreetLabel = QLabel("Street")
        self.billingStreetLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.billingStreetInput = QLineEdit()
        self.billingStreetInput.setPlaceholderText("1234 N 99th St")
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
        self.addAccountsButton = QPushButton("＋    Add Account")
        self.addAccountsButton.setStyleSheet(
            "color: #000000;"
            "background-color: #fc9803;"
            "font-size: 15px;"
            "padding: 10px 50px 10px 50px;"
            "border-radius: 5px;"
            "font-weight: bold;"
        )
        self.buttonBox.addStretch()
        self.buttonBox.addWidget(self.addAccountsButton)
        self.buttonBox.addStretch()
        self.mainLayout.addLayout(self.mainBody)
        self.mainLayout.addLayout(self.buttonBox)
        self.mainLayout.setStretch(1, 2)
        self.setLayout(self.mainLayout)

        self.billingCheckbox.toggled.connect(self.setVisibility)
        self.addAccountsButton.clicked.connect(self.addAccount)

        self.show()

    def addAccount(self):
        can_add_account = True
        first = self.firstNameInput.text()
        if len(first) == 0:
            self.firstNameLabel.setText("First name*")
            self.firstNameLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_account = False
        last = self.lastNameInput.text()
        if len(last) == 0:
            self.lastNameLabel.setText("last name*")
            self.lastNameLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_account = False
        email = self.emailInput.text()
        if len(email) == 0:
            self.emailLabel.setText("email address*")
            self.emailLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_account = False
        phone = self.phoneInput.text()
        if len(phone) == 0:
            self.phoneLabel.setText("phone number*")
            self.phoneLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_account = False
        street = self.streetInput.text()
        if len(street) == 0:
            self.streetLabel.setText("street*")
            self.streetLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_account = False
        city = self.cityInput.text()
        if len(city) == 0:
            self.cityLabel.setText("city*")
            self.cityLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_account = False
        state = self.stateInput.currentText()
        if state == "Select State":
            self.stateLabel.setText("state*")
            self.stateLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_account = False
        zip = self.zipInput.text()
        if len(zip) == 0:
            self.zipLabel.setText("zip code*")
            self.zipLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_account = False
        number = self.cardNumberInput.text()
        if len(number) == 0:
            self.cardNumberLabel.setText("Card Number*")
            self.cardNumberLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_account = False
        exp = self.expInput.text()
        if len(exp) == 0 or "/" not in exp:
            self.expLabel.setText("expiration date*")
            self.expLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_account = False
        cvv = self.cvvInput.text()
        if len(cvv) == 0:
            self.cvvLabel.setText("cvv*")
            self.cvvLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_account = False
        name = self.nameInput.text()
        if len(name) == 0:
            self.nameLabel.setText("name on card*")
            self.nameLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_account = False
        if self.billingCheckbox.isChecked():
            billingStreet = street
            billingCity = city
            billingState = state
            billingZip = zip
        else:
            billingStreet = self.billingStreetInput.text()
            if len(billingStreet) == 0:
                self.billingStreetLabel.setText("street*")
                self.billingStreetLabel.setStyleSheet(
                    "color: red;"
                    "font-size: 15px;"
                    "font-weight: bold;"
                )
                can_add_account = False
            billingCity = self.billingCityInput.text()
            if len(billingCity) == 0:
                self.billingCityLabel.setText("city*")
                self.billingCityLabel.setStyleSheet(
                    "color: red;"
                    "font-size: 15px;"
                    "font-weight: bold;"
                )
                can_add_account = False
            billingState = self.billingStateInput.currentText()
            if billingState == 'Select State':
                self.billingStateLabel.setText("state*")
                self.billingStateLabel.setStyleSheet(
                    "color: red;"
                    "font-size: 15px;"
                    "font-weight: bold;"
                )
                can_add_account = False
            billingZip = self.billingZipInput.text()
            if len(billingZip) == 0:
                self.billingZipLabel.setText("zip code*")
                self.billingZipLabel.setStyleSheet(
                    "color: red;"
                    "font-size: 15px;"
                    "font-weight: bold;"
                )
                can_add_account = False
        if can_add_account:
            all_accounts = account_handler.get_all_accounts()
            all_accounts.append([first, last, email, phone, street, city, state, zip, number, exp, cvv, name, billingStreet, billingCity, billingState, billingZip])
            account_handler.insert_accounts(all_accounts)

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