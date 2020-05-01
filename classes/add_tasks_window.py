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
        self.shopsComboBox.addItems(['Select Shop', 'Cactus Jack', 'KITH', 'Bape', 'Supreme (T-Shirts)', 'Supreme (Accessories)', 'Supreme (Tops / Sweaters)'])
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
        timesList = [
            "Select Time", "1:00 AM", "1:05 AM", "1:10 AM", "1:15 AM", "1:20 AM", "1:25 AM", "1:30 AM", "1:35 AM",
            "1:40 AM", "1:45 AM", "1:50 AM", "1:55 AM", "2:00 AM", "2:05 AM", "2:10 AM", "2:15 AM", "2:20 AM",
            "2:25 AM", "2:30 AM", "2:35 AM", "2:40 AM", "2:45 AM", "2:50 AM", "2:55 AM", "3:00 AM", "3:05 AM",
            "3:10 AM", "3:15 AM", "3:20 AM", "3:25 AM", "3:30 AM", "3:35 AM", "3:40 AM", "3:45 AM", "3:50 AM",
            "3:55 AM", "4:00 AM", "4:05 AM", "4:10 AM", "4:15 AM", "4:20 AM", "4:25 AM", "4:30 AM", "4:35 AM",
            "4:40 AM", "4:45 AM", "4:50 AM", "4:55 AM", "5:00 AM", "5:05 AM", "5:10 AM", "5:15 AM", "5:20 AM",
            "5:25 AM", "5:30 AM", "5:35 AM", "5:40 AM", "5:45 AM", "5:50 AM", "5:55 AM", "6:00 AM", "6:05 AM",
            "6:10 AM", "6:15 AM", "6:20 AM", "6:25 AM", "6:30 AM", "6:35 AM", "6:40 AM", "6:45 AM", "6:50 AM",
            "6:55 AM", "7:00 AM", "7:05 AM", "7:10 AM", "7:15 AM", "7:20 AM", "7:25 AM", "7:30 AM", "7:35 AM",
            "7:40 AM", "7:45 AM", "7:50 AM", "7:55 AM", "8:00 AM", "8:05 AM", "8:10 AM", "8:15 AM", "8:20 AM",
            "8:25 AM", "8:30 AM", "8:35 AM", "8:40 AM", "8:45 AM", "8:50 AM", "8:55 AM", "9:00 AM", "9:05 AM",
            "9:10 AM", "9:15 AM", "9:20 AM", "9:25 AM", "9:30 AM", "9:35 AM", "9:40 AM", "9:45 AM", "9:50 AM",
            "9:55 AM", "10:00 AM", "10:05 AM", "10:10 AM", "10:15 AM", "10:20 AM", "10:25 AM", "10:30 AM", "10:35 AM",
            "10:40 AM", "10:45 AM", "10:50 AM", "10:55 AM", "11:00 AM", "11:05 AM", "11:10 AM", "11:15 AM", "11:20 AM",
            "11:25 AM", "11:30 AM", "11:35 AM", "11:40 AM", "11:45 AM", "11:50 AM", "11:55 AM", "12:00 AM", "12:05 AM",
            "12:10 AM", "12:15 AM", "12:20 AM", "12:25 AM", "12:30 AM", "12:35 AM", "12:40 AM", "12:45 AM", "12:50 AM",
            "12:55 AM", "1:00 PM", "1:05 PM", "1:10 PM", "1:15 PM", "1:20 PM", "1:25 PM", "1:30 PM", "1:35 PM",
            "1:40 PM", "1:45 PM", "1:50 PM", "1:55 PM", "2:00 PM", "2:05 PM", "2:10 PM", "2:15 PM", "2:20 PM",
            "2:25 PM", "2:30 PM", "2:35 PM", "2:40 PM", "2:45 PM", "2:50 PM", "2:55 PM", "3:00 PM", "3:05 PM",
            "3:10 PM", "3:15 PM", "3:20 PM", "3:25 PM", "3:30 PM", "3:35 PM", "3:40 PM", "3:45 PM", "3:50 PM",
            "3:55 PM", "4:00 PM", "4:05 PM", "4:10 PM", "4:15 PM", "4:20 PM", "4:25 PM", "4:30 PM", "4:35 PM",
            "4:40 PM", "4:45 PM", "4:50 PM", "4:55 PM", "5:00 PM", "5:05 PM", "5:10 PM", "5:15 PM", "5:20 PM",
            "5:25 PM", "5:30 PM", "5:35 PM", "5:40 PM", "5:45 PM", "5:50 PM", "5:55 PM", "6:00 PM", "6:05 PM",
            "6:10 PM", "6:15 PM", "6:20 PM", "6:25 PM", "6:30 PM", "6:35 PM", "6:40 PM", "6:45 PM", "6:50 PM",
            "6:55 PM", "7:00 PM", "7:05 PM", "7:10 PM", "7:15 PM", "7:20 PM", "7:25 PM", "7:30 PM", "7:35 PM",
            "7:40 PM", "7:45 PM", "7:50 PM", "7:55 PM", "8:00 PM", "8:05 PM", "8:10 PM", "8:15 PM", "8:20 PM",
            "8:25 PM", "8:30 PM", "8:35 PM", "8:40 PM", "8:45 PM", "8:50 PM", "8:55 PM", "9:00 PM", "9:05 PM",
            "9:10 PM", "9:15 PM", "9:20 PM", "9:25 PM", "9:30 PM", "9:35 PM", "9:40 PM", "9:45 PM", "9:50 PM",
            "9:55 PM", "10:00 PM", "10:05 PM", "10:10 PM", "10:15 PM", "10:20 PM", "10:25 PM", "10:30 PM", "10:35 PM",
            "10:40 PM", "10:45 PM", "10:50 PM", "10:55 PM", "11:00 PM", "11:05 PM", "11:10 PM", "11:15 PM", "11:20 PM",
            "11:25 PM", "11:30 PM", "11:35 PM", "11:40 PM", "11:45 PM", "11:50 PM", "11:55 PM", "12:00 PM", "12:05 PM",
            "12:10 PM", "12:15 PM", "12:20 PM", "12:25 PM", "12:30 PM", "12:35 PM", "12:40 PM", "12:45 PM", "12:50 PM",
            "12:55 PM"
        ]
        self.startTime = QComboBox()
        self.startTime.addItems(
            timesList)
        self.startTime.setStyleSheet(
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
            "color: #000000;"
            "font-size: 20px;"
            "font-weight: bold;"
            "background-color: #fc9803;"
            "padding: 10px 20px 10px 20px;"
            "border-radius: 5px;"
            "margin-bottom: 0px;"
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
        start_time = self.startTime.currentText()
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