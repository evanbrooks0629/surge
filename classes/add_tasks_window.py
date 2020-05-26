from PyQt5.QtWidgets import *

from handlers import task_handler


class AddTasksWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 150, 400, 300)
        self.setMinimumSize(400, 300)
        self.setMaximumSize(400, 300)
        self.setStyleSheet(
            "font-family: 'Moon';"
            "background-color: #ffffff;"
        )
        self.setWindowTitle('Add Tasks')
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
        self.shopsComboBox.addItems(['Select Shop', 'Supreme (T-Shirts)', 'Supreme (Accessories)', 'Supreme (Tops / Sweaters)', 'Supreme (Jackets)', 'Supreme (Shirts)', 'Supreme (Sweatshirts)', 'Supreme (Pants)', 'Supreme (Shorts)', 'Supreme (Hats)', 'Supreme (Bags)', 'Supreme (Shoes)', 'Supreme (Skate)'])
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
        self.sizeLabel = QLabel("Size")
        self.sizeLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold"
        )
        self.sizeComboBox = QComboBox()
        self.sizeComboBox.addItems(
            ['Select Size', 'Random', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0', '9.5', '10.0', '10.5', '11.0',
             '11.5', '12.0',
             '12.5', '13.0', 'S', 'M', 'L', 'XL'])
        self.sizeComboBox.setStyleSheet(
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
        layout.addWidget(self.sizeLabel, 2, 0)
        layout.addWidget(self.sizeComboBox, 2, 1, 1, 2)
        self.delayLabel = QLabel("Delay (ms)")
        self.delayLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold"
        )
        self.delayInput = QLineEdit()
        self.delayInput.setPlaceholderText("Enter a delay in milliseconds")
        self.delayInput.setStyleSheet(
            "color: #000000;"
            "background-color: #ffffff;"
            "border: 2px solid #03c6fc;"
        )
        layout.addWidget(self.delayLabel, 3, 0)
        layout.addWidget(self.delayInput, 3, 1, 1, 2)
        self.startLabel = QLabel("Manual Start")
        self.startLabel.setStyleSheet(
            "color: #000000;"
            "font-size: 15px;"
            "font-weight: bold"
        )
        self.startInput = QCheckBox()
        self.startInput.setStyleSheet(
            "padding-left: 50px;"
        )
        self.startTime = QTimeEdit()
        layout.addWidget(self.startLabel, 4, 0)
        layout.addWidget(self.startInput, 4, 1)
        layout.addWidget(self.startTime, 4, 2)
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

        layout.addWidget(self.numTasksLabel, 5, 0)
        layout.addWidget(self.numTasksComboBox, 5, 1, 1, 2)
        self.addTasksButton = QPushButton("＋    Add Tasks")
        self.addTasksButton.setStyleSheet(
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
        layout.addWidget(self.addTasksButton, 6, 0, 1, 3)
        self.setLayout(layout)
        self.startInput.toggled.connect(self.setVisibility)
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
        size = self.sizeComboBox.currentText()
        if size == 'Select Size':
            self.sizeLabel.setText("Size*")
            self.sizeLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            can_add_task = False
        delay = self.delayInput.text()
        if len(delay) == 0:
            self.delayLabel.setText("Delay*")
            self.delayLabel.setStyleSheet(
                "color: red;"
                "font-size: 15px;"
                "font-weight: bold;"
            )
            delay = '0 ms'
        else:
            delay += 'ms'
        checked = self.startInput.isChecked()
        start_time = self.startTime.text()
        if not checked:
            if start_time == 'Select Time':
                self.startLabel.setText("Manual Start*")
                self.startLabel.setStyleSheet(
                    "color: red;"
                    "font-size: 15px;"
                    "font-weight: bold;"
                )
                can_add_task = False
            manual_start = 'False'
        else:
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

    def setVisibility(self):
        if self.startInput.isChecked():
            self.startTime.hide()
        else:
            self.startTime.show()