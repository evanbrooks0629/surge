from PyQt5.QtWidgets import *

from handlers import task_handler, settings_handler


class QuickTasksWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 150, 400, 200)
        self.setMinimumSize(400, 200)
        self.setMaximumSize(400, 200)
        self.setStyleSheet(
            "font-family: 'Moon';"
            "background-color: #ffffff;"
        )
        self.setWindowTitle('Quick Tasks')
        self.UI()

    def UI(self):
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        self.shopLabel = QLabel("Shop")
        self.shopLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold"
        )
        self.shopsComboBox = QComboBox()
        self.shopsComboBox.addItems(['Select Shop', 'Cactus Jack', 'KITH', 'Bape', 'Supreme (T-Shirts)', 'Supreme (Accessories)'])
        self.shopsComboBox.setStyleSheet(
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
        layout.addWidget(self.shopLabel, 0, 0)
        layout.addWidget(self.shopsComboBox, 0, 1, 1, 2)
        self.productLabel = QLabel("Product")
        self.productLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold"
        )
        self.productInput = QLineEdit()
        self.productInput.setPlaceholderText("Enter a product")
        self.productInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        layout.addWidget(self.productLabel, 1, 0)
        layout.addWidget(self.productInput, 1, 1, 1, 2)
        numTasks = ['Select Amount',
                    '1',
                    '2',
                    '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36',
                    '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52',
                    '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68',
                    '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84',
                    '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100']
        self.numTasksLabel = QLabel("Num Tasks")
        self.numTasksLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold"
        )
        self.numTasksComboBox = QComboBox()
        self.numTasksComboBox.addItems(
            numTasks)
        self.numTasksComboBox.setStyleSheet(
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

        layout.addWidget(self.numTasksLabel, 2, 0)
        layout.addWidget(self.numTasksComboBox, 2, 1, 1, 2)
        self.addTasksButton = QPushButton("＋    Add Tasks")
        self.addTasksButton.setStyleSheet(
            "color: #000000;"
            "font-size: 20px;"
            "font-weight: bold;"
            "background-color: #fc9803;"
            "padding: 10px 20px 10px 20px;"
            "border-radius: 5px;"
            "margin-bottom: 0px;"
        )
        layout.addWidget(self.addTasksButton, 3, 0, 1, 3)
        self.setLayout(layout)
        self.addTasksButton.clicked.connect(self.addTask)
        self.show()

    def addTask(self):
        can_add_task = True
        shop = self.shopsComboBox.currentText()
        if shop == 'Select Shop':
            self.shopLabel.setText("Shop*")
            self.shopLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_task = False
        product = self.productInput.text()
        if len(product) == 0:
            self.productLabel.setText("Product*")
            self.productLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_task = False
        default_settings = settings_handler.get_setting("quick task default")
        size = default_settings[0]
        delay = str(default_settings[1])
        delay += 'ms'
        start_time = 'Manual'
        manual_start = 'True'

        num_tasks = self.numTasksComboBox.currentText()
        if num_tasks == 'Select Amount':
            self.numTasksLabel.setText("Num Tasks*")
            self.numTasksLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_task = False
            num_tasks = '0'
        num_tasks = int(num_tasks)
        if can_add_task:
            all_tasks = task_handler.get_all_tasks()
            num_previous_tasks = len(all_tasks)
            for i in range(0, num_tasks):
                account = f"Account " + str(num_previous_tasks + i + 1)
                all_tasks.append([shop, product, size, delay, account, manual_start, start_time])
            task_handler.insert_tasks(all_tasks)

            self.close()
