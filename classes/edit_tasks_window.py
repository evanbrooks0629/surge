from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from handlers import task_handler


class EditTasksWindow(QWidget):
    def __init__(self, indexes, product, size, delay):
        super().__init__()
        self.indexes = indexes
        self.product = product
        self.size = size
        self.delay = delay
        self.setGeometry(400, 150, 400, 200)
        self.setMinimumSize(400, 200)
        self.setMaximumSize(400, 200)
        self.setStyleSheet(
            "font-family: 'Moon';"
            "background-color: #ffffff;"
        )
        self.setWindowTitle('Edit Tasks')
        self.UI()

    def UI(self):
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)

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
        self.productInput.setText(self.product)
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
        self.sizeComboBox.setCurrentText(self.size)
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
        self.delayLabel = QLabel("Delay")
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
        self.delayInput.setText(self.delay)
        layout.addWidget(self.delayLabel, 3, 0)
        layout.addWidget(self.delayInput, 3, 1, 1, 2)

        self.editTasksButton = QPushButton("    Edit Tasks")
        self.editTasksButton.setIcon(QIcon("images/iconeditblack.icns"))
        self.editTasksButton.setStyleSheet(
            "color: #000000;"
            "font-size: 20px;"
            "font-weight: bold;"
            "background-color: #fc9803;"
            "padding: 10px 20px 10px 20px;"
            "border-radius: 5px;"
            "margin-bottom: 0px;"
        )
        layout.addWidget(self.editTasksButton, 6, 0, 1, 3)
        self.setLayout(layout)
        self.editTasksButton.clicked.connect(self.editTasks)
        self.show()

    def editTasks(self):
        new_product = self.productInput.text()
        new_size = self.sizeComboBox.currentText()
        new_delay = self.delayInput.text()
        new_delay += "ms"
        all_tasks = task_handler.get_all_tasks()
        num_tasks = task_handler.get_num_tasks()
        for i in range(0, num_tasks):
            for index in self.indexes:
                if index == i:
                    all_tasks[i][1] = new_product
                    all_tasks[i][2] = new_size
                    all_tasks[i][3] = new_delay
        task_handler.insert_tasks(all_tasks)
        # get the indexes of the tasks that are checked
        # replace the tasks at those indexes with the new updated tasks (put in new prod, size, and delay)
        self.close()
