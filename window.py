import sys
import json
import time
import threading
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from classes.add_tasks_window import AddTasksWindow
from classes.quick_tasks_window import QuickTasksWindow
from classes.edit_tasks_window import EditTasksWindow
from classes.edit_task_window import EditTaskWindow
from classes.add_accounts_window import AddAccountsWindow
from classes.edit_accounts_window import EditAccountsWindow
from classes.add_proxy_window import AddProxyWindow
from classes.edit_proxy_window import EditProxyWindow
from classes.proxies_tester import Worker as ProxiesWorker
from classes.proxy_tester import Worker as ProxyWorker
from classes.verification_window import KeyVerificationWindow

from workers.time_check_worker import Worker as TimeCheckWorker
from workers.task_workers import Worker as TaskWorker

from handlers import task_handler, account_handler, proxy_handler, settings_handler, import_handler, export_handler


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 1200, 700)
        self.setMinimumSize(1200, 700)
        self.setMaximumSize(1200, 700)
        self.setStyleSheet(
            "font-family: 'Moon';"
            "background-color: #303030;"
        )
        self.setWindowTitle('Surge')
        #self.setWindowFlag(Qt.FramelessWindowHint) #removes window
        # find out how to add a close windsow button and a way
        # to move it around
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle, the PyInstaller bootloader
            # extends the sys module by a flag frozen=True and sets the app
            # path into variable _MEIPASS'.
            self.application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
            application_path = application_path.split("/")
            #application_path.remove(application_path[6])
            application_path.remove(application_path[0])
            appstr = '/'
            for char in application_path:
                appstr += char + '/'
            self.application_path = appstr
        self.css_path = os.path.join(self.application_path, 'main.css')
        self.UI()

    def UI(self):
        mainBox = QVBoxLayout()
        self.headerBox = QHBoxLayout()
        self.headerUI()
        self.tabUI()
        self.dashboardUI()
        self.accountsUI()
        self.proxiesUI()
        self.settingsUI()
        mainBox.addLayout(self.headerBox)
        mainBox.addWidget(self.tabs)
        mainBox.setStretch(1, 2)
        self.setLayout(mainBox)
        self.show()

    def headerUI(self):
        settings = settings_handler.get_all_settings()
        self.surgeLabel = QLabel()
        img_path = os.path.join(self.application_path, 'images/headerLogo.png')
        pic = QPixmap(img_path)
        self.surgeLabel.setPixmap(pic)
        self.surgeLabel.setAlignment(Qt.AlignLeft)
        if settings["webhook"] == '':
            self.userLabel = QLabel("Welcome user")
        else:
            self.userLabel = QLabel(f"Welcome {settings['webhook']}")
        self.userLabel.setAlignment(Qt.AlignHCenter)
        self.userLabel.setObjectName("userLabel")
        self.userLabel.setStyleSheet(open(self.css_path).read())
        self.versionLabel = QLabel("Surge Bot Version 1.0 (Beta)")
        self.versionLabel.setAlignment(Qt.AlignRight)
        self.versionLabel.setObjectName("versionLabel")
        self.versionLabel.setStyleSheet(open(self.css_path).read())
        self.headerBox.addWidget(self.surgeLabel)
        self.headerBox.addWidget(self.userLabel)
        self.headerBox.addWidget(self.versionLabel)

    def tabUI(self):
        self.tabs = QTabWidget()
        self.dashboardTab = QTabBar()
        self.tabs.addTab(self.dashboardTab, "          Dashboard          ")
        img_path = os.path.join(self.application_path, 'images/dashboardTabIcon.icns')
        self.tabs.setTabIcon(0, QIcon(img_path))
        self.accountsTab = QTabBar()
        self.tabs.addTab(self.accountsTab, "          Accounts          ")
        img_path = os.path.join(self.application_path, 'images/accountsTabIcon.icns')
        self.tabs.setTabIcon(1, QIcon(img_path))
        self.proxiesTab = QTabBar()
        self.tabs.addTab(self.proxiesTab, "          Proxies          ")
        img_path = os.path.join(self.application_path, 'images/proxiesTabIcon.icns')
        self.tabs.setTabIcon(2, QIcon(img_path))
        self.settingsTab = QTabBar()
        self.tabs.addTab(self.settingsTab, "          Settings          ")
        img_path = os.path.join(self.application_path, 'images/settingsTabIcon.icns')
        self.tabs.setTabIcon(3, QIcon(img_path))
        self.tabs.setStyleSheet(open(self.css_path).read())
        self.dashboardTab.setStyleSheet(
            "background-color: #000000;"
            "border-bottom-left-radius: 5px;"
            "border-bottom-right-radius: 5px;"
        )
        self.accountsTab.setStyleSheet(
            "background-color: #000000;"
            "border-bottom-left-radius: 5px;"
            "border-bottom-right-radius: 5px;"
        )
        self.proxiesTab.setStyleSheet(
            "background-color: #000000;"
            "border-bottom-left-radius: 5px;"
            "border-bottom-right-radius: 5px;"
        )
        self.settingsTab.setStyleSheet(
            "background-color: #000000;"
            "border-bottom-left-radius: 5px;"
            "border-bottom-right-radius: 5px;"
        )

    # DASHBOARD

    def dashboardUI(self):
        num_tasks = task_handler.get_num_tasks()
        self.tasksLabel = QLabel(f"Current Tasks   [{num_tasks}]")
        self.tasksLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 20px;"
            "font-weight: bold;"
        )
        self.quickTasksButton = QPushButton("Quick tasks")
        img_path = os.path.join(self.application_path, 'images/lightningicon.icns')
        self.quickTasksButton.setIcon(QIcon(img_path))
        self.quickTasksButton.setStyleSheet(
            """
            QPushButton {
                background-color: #000000;
                color: #fc9803;
                border: 2px solid #fc9803;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #101010;
                border: 3px solid #fc9803;
            }
            QPushButton:pressed {
                background-color: #000000;
            }
            """
        )
        self.selectAllTasksButton = QPushButton("Select All")
        img_path = os.path.join(self.application_path, 'images/checkIcon.icns')
        self.selectAllTasksButton.setIcon(QIcon(img_path))
        self.selectAllTasksButton.setStyleSheet(
            """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #ffffff;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #dcdcdc;
                border: 2px solid #dcdcdc;
            }
            QPushButton:pressed {
                background-color: #ffffff;
            }
            """
        )
        self.selectAllTasksButton.hide()
        self.editTasksButton = QPushButton("Edit Tasks")
        img_path = os.path.join(self.application_path, 'images/editIcon.icns')
        self.editTasksButton.setIcon(QIcon(img_path))
        self.editTasksButton.setStyleSheet(
            """
            QPushButton {
                background-color: #03c6fc;
                color: #000000;
                border: 2px solid #03c6fc;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #03b2e3;
                border: 2px solid #03b2e3;
            }
            QPushButton:pressed {
                background-color: #03c6fc;
            }
            """
        )
        self.editTasksButton.hide()
        self.deleteTasksButton = QPushButton("Delete Tasks")
        img_path = os.path.join(self.application_path, 'images/trashIcon.icns')
        self.deleteTasksButton.setIcon(QIcon(img_path))
        self.deleteTasksButton.setStyleSheet(
            """
            QPushButton {
                background-color: #fc9803;
                color: #000000;
                border: 2px solid #fc9803;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #e38902;
                border: 2px solid #e38902;
            }
            QPushButton:pressed {
                background-color: #fc9803;
            }
            """
        )
        self.deleteTasksButton.hide()
        num_tasks = task_handler.get_num_tasks()
        if num_tasks != 0:
            self.selectAllTasksButton.show()
            self.editTasksButton.show()
            self.deleteTasksButton.show()
        self.refreshTasksButton = QPushButton("Refresh Feed")
        img_path = os.path.join(self.application_path, 'images/refreshIcon.icns')
        self.refreshTasksButton.setIcon(QIcon(img_path))
        self.refreshTasksButton.setStyleSheet(
            """
            QPushButton {
                background-color: #000000;
                color: #03c6fc;
                border: 2px solid #03c6fc;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #101010;
                border: 3px solid #03c6fc;
            }
            QPushButton:pressed {
                background-color: #000000;
            }
            """
        )
        self.refreshTasksButton.clicked.connect(self.resetDashboardUI)
        self.quickTasksButton.clicked.connect(self.quickTasksWindow)
        self.dashboardHeaderBox = QVBoxLayout()
        self.dashboardHeaderBoxTop = QHBoxLayout()
        self.dashboardHeaderBoxTop.addWidget(self.tasksLabel)
        self.dashboardHeaderBoxTop.addStretch()
        self.dashboardHeaderBoxTop.addWidget(self.quickTasksButton)
        self.dashboardHeaderBoxTop.addWidget(self.selectAllTasksButton)
        self.dashboardHeaderBoxTop.addWidget(self.editTasksButton)
        self.dashboardHeaderBoxTop.addWidget(self.deleteTasksButton)
        self.dashboardHeaderBoxTop.addWidget(self.refreshTasksButton)
        self.shopLabel = QLabel('             Shop')
        self.shopLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
            "padding-left: 1px;"
        )
        self.shopLabel.setFixedWidth(160)
        self.shopLabel.setAlignment(Qt.AlignLeft)
        self.productLabel = QLabel('                   Product')
        self.productLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
        )
        self.productLabel.setFixedWidth(140)
        self.productLabel.setAlignment(Qt.AlignLeft)
        self.sizeLabel = QLabel('                         Size')
        self.sizeLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
        )
        self.sizeLabel.setFixedWidth(130)
        self.sizeLabel.setAlignment(Qt.AlignLeft)
        self.delayLabel = QLabel('           Delay')
        self.delayLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
            "margin-left: -5px;"
        )
        self.delayLabel.setFixedWidth(120)
        self.delayLabel.setAlignment(Qt.AlignLeft)
        self.accountLabel = QLabel('Account')
        self.accountLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
        )
        self.accountLabel.setFixedWidth(120)
        self.accountLabel.setAlignment(Qt.AlignLeft)
        self.startLabel = QLabel('Start')
        self.startLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
        )
        self.startLabel.setFixedWidth(120)
        self.startLabel.setAlignment(Qt.AlignLeft)
        self.statusLabel = QLabel('Status')
        self.statusLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
        )
        self.statusLabel.setFixedWidth(150)
        self.statusLabel.setAlignment(Qt.AlignLeft)
        self.controlsLabel = QLabel('            Controls')
        self.controlsLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
        )
        self.controlsLabel.setFixedWidth(150)
        self.controlsLabel.setAlignment(Qt.AlignLeft)
        self.dashboardHeaderBoxBottom = QHBoxLayout()
        self.dashboardHeaderBoxBottom.setContentsMargins(0, 30, 0, 0)
        self.dashboardHeaderBoxBottom.addStretch()
        self.dashboardHeaderBoxBottom.addWidget(self.shopLabel)
        self.dashboardHeaderBoxBottom.addStretch()
        self.dashboardHeaderBoxBottom.addWidget(self.productLabel)
        self.dashboardHeaderBoxBottom.addStretch()
        self.dashboardHeaderBoxBottom.addWidget(self.sizeLabel)
        self.dashboardHeaderBoxBottom.addStretch()
        self.dashboardHeaderBoxBottom.addWidget(self.delayLabel)
        self.dashboardHeaderBoxBottom.addStretch()
        self.dashboardHeaderBoxBottom.addWidget(self.accountLabel)
        self.dashboardHeaderBoxBottom.addStretch()
        self.dashboardHeaderBoxBottom.addWidget(self.startLabel)
        self.dashboardHeaderBoxBottom.addStretch()
        self.dashboardHeaderBoxBottom.addWidget(self.statusLabel)
        self.dashboardHeaderBoxBottom.addStretch()
        self.dashboardHeaderBoxBottom.addWidget(self.controlsLabel)
        self.dashboardHeaderBoxBottom.addStretch()
        self.dashboardHeaderBox.addLayout(self.dashboardHeaderBoxTop)
        self.dashboardHeaderBox.addLayout(self.dashboardHeaderBoxBottom)
        # sub-header
        self.tasksScrollView = QScrollArea()
        self.tasksWidget = QWidget()
        self.tasksWidget.setObjectName("tasksWidget")
        self.tasksBox = QVBoxLayout()
        self.tasksBox.setSpacing(5)
        self.showTasks()
        self.tasksScrollView.setWidget(self.tasksWidget)
        self.tasksScrollView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tasksScrollView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tasksScrollView.setWidgetResizable(True)
        self.dashboardButtonsBox = QHBoxLayout()
        self.addTasksButton = QPushButton("＋    Add Tasks")
        self.addTasksButton.setStyleSheet(
            """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border-radius: 5px;
                padding: 10px 50px 7px 50px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton::hover {
                background-color: #dcdcdc;
            }
            QPushButton:pressed {
                background-color: #ffffff;
            }
            """
        )
        self.startTasksButton = QPushButton("►    Start Tasks")
        self.startTasksButton.setStyleSheet(
            """
            QPushButton {
                background-color: #03c6fc;
                color: #000000;
                border-radius: 5px;
                padding: 10px 50px 10px 50px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton::hover {
                background-color: #03b2e3;
            }
            QPushButton:pressed {
                background-color: #03c6fc;
            }
            """
        )
        self.stopTasksButton = QPushButton("◼    Stop Tasks")
        self.stopTasksButton.setStyleSheet(
            """
            QPushButton {
                background-color: #fc9803;
                color: #000000;
                border-radius: 5px;
                padding: 10px 50px 10px 50px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton::hover {
                background-color: #e38902;
            }
            QPushButton:pressed {
                background-color: #fc9803;
            }
            """
        )
        self.dashboardButtonsBox.addWidget(self.addTasksButton)
        self.dashboardButtonsBox.addWidget(self.startTasksButton)
        self.dashboardButtonsBox.addWidget(self.stopTasksButton)
        self.dashboardBodyBox = QVBoxLayout()
        self.dashboardBodyBox.addWidget(self.tasksScrollView)
        self.dashboardBodyBox.addLayout(self.dashboardButtonsBox)
        self.dashboard = QVBoxLayout()
        self.dashboard.addLayout(self.dashboardHeaderBox)
        self.dashboard.addLayout(self.dashboardBodyBox)
        self.dashboard.setStretch(1, 2)
        self.dashboardTab.setLayout(self.dashboard)
        self.addTasksButton.clicked.connect(self.addTasksWindow)
        self.editTasksButton.clicked.connect(self.editTasksWindow)
        self.startTasksButton.clicked.connect(lambda: self.startTasks(True, 0, self.start_objects_list_tasks))
        self.stopTasksButton.clicked.connect(lambda: self.stopTasks(True, 0))

    def resetDashboardUI(self):
        while self.tasksBox.count():
            child = self.tasksBox.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        num_tasks = task_handler.get_num_tasks()
        if num_tasks > 0:
            self.showTasks()
            self.selectAllTasksButton.show()
            self.editTasksButton.show()
            self.deleteTasksButton.show()
        else:
            self.showTasks()
            self.selectAllTasksButton.hide()
            self.editTasksButton.hide()
            self.deleteTasksButton.hide()
        self.tasksLabel.setText(f"Current Tasks   [{num_tasks}]")
        self.tasksLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 20px;"
            "font-weight: bold;"
        )

    def showTasks(self):
        edit_objects_list_tasks = []
        delete_objects_list_tasks = []
        self.start_objects_list_tasks = []
        self.tasks_status_labels = []
        num_tasks = task_handler.get_num_tasks()
        all_tasks = task_handler.get_all_tasks()
        # first, resort them
        if num_tasks > 0:
            acc_num = 0
            for sort_task in all_tasks:
                number = int(sort_task[4][8:])
                if number - 1 != acc_num:
                    sort_task[4] = 'Account ' + str(acc_num + 1)
                acc_num += 1
            task_handler.insert_tasks(all_tasks)
            all_tasks = task_handler.get_tasks_as_string()
            for i in range(0, num_tasks):
                task = all_tasks[i]
                self.tasksWidgetBox = QWidget()
                self.tasksWidgetBox.setStyleSheet(
                    "border-radius: 5px;"
                )
                self.taskLine = QHBoxLayout()
                self.shop = QLabel(str(i+1) + '   ' + task[0])
                self.shop.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.shop.setAlignment(Qt.AlignLeft)
                self.shop.setFixedWidth(160)
                self.product = QLabel(task[1])
                self.product.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.product.setAlignment(Qt.AlignLeft)
                self.product.setFixedWidth(160)
                self.size = QLabel(task[2])
                self.size.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.size.setAlignment(Qt.AlignLeft)
                self.size.setFixedWidth(80)
                self.delay = QLabel(task[3])
                self.delay.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.delay.setAlignment(Qt.AlignLeft)
                self.delay.setFixedWidth(80)
                self.account = QLabel(task[4])
                self.account.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.account.setAlignment(Qt.AlignLeft)
                self.account.setFixedWidth(120)
                self.start = QLabel(task[5])
                self.start.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.start.setAlignment(Qt.AlignLeft)
                self.start.setFixedWidth(120)
                self.status = QLabel()
                if task[5] == 'Manual       ':
                    self.status.setText("Ready to start...")
                else:
                    self.status.setText(f"Starting at {task[5]}")
                self.status.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.status.setAlignment(Qt.AlignLeft)
                self.status.setObjectName("status")
                self.status.setFixedWidth(180)
                self.tasks_status_labels.append(self.status)
                self.editButtonTasks = QPushButton()
                img_path = os.path.join(self.application_path, 'images/iconedit.icns')
                self.editButtonTasks.setIcon(QIcon(img_path))
                self.editButtonTasks.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #000000;
                        color: #000000;
                        border-radius: 5px;
                        padding: 0px;
                        font-weight: bold;
                    }
                    QPushButton::hover {
                        background-color: #FF00FF;
                    }
                    QPushButton:pressed {
                        background-color: #000000;
                    }
                    """
                )
                self.editButtonTasks.setObjectName("editButtonTasks")
                edit_objects_list_tasks.append(self.editButtonTasks)
                self.startButtonTasks = QPushButton()
                img_path = os.path.join(self.application_path, 'images/iconstart.icns')
                self.startButtonTasks.setIcon(QIcon(img_path))
                self.startButtonTasks.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #000000;
                        color: #000000;
                        border-radius: 5px;
                        padding: 0px;
                        font-weight: bold;
                    }
                    QPushButton::hover {
                        background-color: #FF00FF;
                    }
                    QPushButton:pressed {
                        background-color: #000000;
                    }
                    """
                )
                self.startButtonTasks.setObjectName("startButtonTasks")
                self.start_objects_list_tasks.append(self.startButtonTasks)
                self.deleteButtonTasks = QPushButton()
                img_path = os.path.join(self.application_path, 'images/icontrash.icns')
                self.deleteButtonTasks.setIcon(QIcon(img_path))
                self.deleteButtonTasks.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #000000;
                        color: #000000;
                        border-radius: 5px;
                        padding: 0px;
                        font-weight: bold;
                    }
                    QPushButton::hover {
                        background-color: #FF00FF;
                    }
                    QPushButton:pressed {
                        background-color: #000000;
                    }
                    """
                )
                self.deleteButtonTasks.setObjectName("deleteButtonTasks")
                delete_objects_list_tasks.append(self.deleteButtonTasks)
                self.checkboxTasks = QCheckBox()
                self.taskLine.addWidget(self.checkboxTasks)
                self.taskLine.addStretch()
                self.taskLine.addWidget(self.shop)
                self.taskLine.addStretch()
                self.taskLine.addWidget(self.product)
                self.taskLine.addStretch()
                self.taskLine.addWidget(self.size)
                self.taskLine.addStretch()
                self.taskLine.addWidget(self.delay)
                self.taskLine.addStretch()
                self.taskLine.addWidget(self.account)
                self.taskLine.addStretch()
                self.taskLine.addWidget(self.start)
                self.taskLine.addStretch()
                self.taskLine.addWidget(self.status)
                self.taskLine.addStretch()
                self.taskLine.addWidget(self.startButtonTasks)
                self.taskLine.addStretch()
                self.taskLine.addWidget(self.editButtonTasks)
                self.taskLine.addStretch()
                self.taskLine.addWidget(self.deleteButtonTasks)
                self.taskLine.addStretch()
                self.tasksWidgetBox.setLayout(self.taskLine)
                self.tasksWidgetBox.setFixedHeight(40)
                self.tasksBox.addWidget(self.tasksWidgetBox)
        else:
            self.tasksWidgetBox = QWidget()
            self.taskLine = QHBoxLayout()
            self.tasksLabelNone = QLabel("Add tasks to get started.")
            self.tasksLabelNone.setStyleSheet(
                "color: #ffffff;"
                "font-size: 15px;"
                "border-bottom: 2px solid #fc9803;"
                "border-radius: 0px;"
                "padding: 5px;"
            )
            self.tasksLabelNone.setAlignment(Qt.AlignCenter)
            self.taskLine.addStretch()
            self.taskLine.addWidget(self.tasksLabelNone)
            self.taskLine.addStretch()
            self.tasksWidgetBox.setLayout(self.taskLine)
            self.tasksWidgetBox.setFixedHeight(50)
            self.tasksBox.addWidget(self.tasksWidgetBox)

        self.tasksWidget.setLayout(self.tasksBox)
        self.tasksScrollView.setWidget(self.tasksWidget)
        self.selectAllTasksButton.clicked.connect(self.checkAllTasks)
        self.deleteTasksButton.clicked.connect(self.deleteTasks)

        widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for widget in widgets:
            try:
                editButtons = widget.findChildren(QPushButton, 'editButtonTasks')
                for e in range(0, len(editButtons)):
                    editButtons[e].clicked.connect(lambda: self.editTask(edit_objects_list_tasks))
            except:
                pass

        widgets2 = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for widget2 in widgets2:
            try:
                deleteButtons = widget2.findChildren(QPushButton, 'deleteButtonTasks')
                for e in range(0, len(deleteButtons)):
                    deleteButtons[e].clicked.connect(lambda: self.deleteTask(delete_objects_list_tasks))
            except:
                pass

        tasksWidgetStarts = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for taskWidgetStart in tasksWidgetStarts:
            try:
                startButtons = taskWidgetStart.findChildren(QPushButton, 'startButtonTasks')
                for e in range(0, len(startButtons)):
                    startButtons[e].clicked.connect(lambda: self.startTask(self.start_objects_list_tasks))
            except:
                pass

        all_tasks = task_handler.get_all_tasks()
        if len(all_tasks) > 0:
            if all_tasks[0][5] == 'False':
                try:
                    if self.timer_thread_pool:
                        self.timer_worker.reset_timer()
                except:
                    pass
                self.check_start_time(self.start_objects_list_tasks)

    def get_start_times(self):
        all_tasks = task_handler.get_all_tasks()
        num_tasks = task_handler.get_num_tasks()
        time_list = []
        if num_tasks > 0:
            for task in all_tasks:
                if task[5] == "False":
                    time = task[6]
                    time = time.split(" ")
                    start_time = time[0]
                    if time[1] == 'PM':
                        start_times = start_time.split(":")
                        hour = int(start_times[0])
                        hour += 12
                        hour = str(hour)
                        time = f"{hour}:{start_times[1]}"
                        time_list.append(time)
                    else:
                        time_list.append(start_time)
                else:
                    time_list.append(False)
        return time_list

    def check_start_time(self, objects):
        time_list = self.get_start_times()

        self.timer_thread_pool = QThreadPool()

        self.timer_worker = TimeCheckWorker(time_list) # import worker class as...

        self.timer_worker.setAutoDelete(True)
        self.timer_worker.signals.timematch.connect(lambda: self.startTasks(True, 0, objects)) # signal should be if time is equal

        self.timer_thread_pool.start(self.timer_worker)

    def task_run_started(self):
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            try:
                all_status = task_widget.findChildren(QLabel, "status")
                for e in range(0, len(all_status)):
                    all_status[e].setText("Running now...")
                    all_status[e].setStyleSheet(
                        "color: #fc9803;"
                        "font-weight: bold;"
                    )
            except:
                pass

    def task_run_started_ind(self, e):
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            try:
                all_status = task_widget.findChildren(QLabel, "status")
                all_status[e].setText("Running now...")
                all_status[e].setStyleSheet(
                    "color: #fc9803;"
                    "font-weight: bold;"
                )
            except:
                pass

    def task_run_searching(self, i):
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            try:
                all_status = task_widget.findChildren(QLabel, "status")
                all_status[i].setText("Searching for product")
                all_status[i].setStyleSheet(
                    "color: #FFFF00;"
                    "font-weight: bold;"
                )
            except:
                pass

    def task_run_found(self, i):
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            try:
                all_status = task_widget.findChildren(QLabel, "status")
                all_status[i].setText("Found product")
                all_status[i].setStyleSheet(
                    "color: #03c6fc;"
                    "font-weight: bold;"
                )
            except:
                pass

    def task_run_cart(self, i):
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            try:
                all_status = task_widget.findChildren(QLabel, "status")
                all_status[i].setText("At cart")
                all_status[i].setStyleSheet(
                    "color: #FF00FF;"
                    "font-weight: bold;"
                )
            except:
                pass

    def task_run_checkout(self, i):
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            try:
                all_status = task_widget.findChildren(QLabel, "status")
                all_status[i].setText("Checking out")
                all_status[i].setStyleSheet(
                    "color: #0000FF;"
                    "font-weight: bold;"
                )
            except:
                pass

    def task_run_success(self, i, success):
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            try:
                all_status = task_widget.findChildren(QLabel, "status")
                if success:
                    all_status[i].setText("Product copped")
                    all_status[i].setStyleSheet(
                        "color: #00FF00;"
                        "font-weight: bold;"
                    )
                else:
                    all_status[i].setText("Error obtaining product")
                    all_status[i].setStyleSheet(
                        "color: red;"
                        "font-weight: bold;"
                    )
            except:
                pass

    def task_run_cart_error(self, i):
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            try:
                all_status = task_widget.findChildren(QLabel, "status")
                all_status[i].setText("Cart Error")
                all_status[i].setStyleSheet(
                    "color: red;"
                    "font-weight: bold;"
                )
            except:
                pass

    def task_run_captcha_error(self, i):
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            try:
                all_status = task_widget.findChildren(QLabel, "status")
                all_status[i].setText("Captcha Error")
                all_status[i].setStyleSheet(
                    "color: red;"
                    "font-weight: bold;"
                )
            except:
                pass

    def task_run_card_declined(self, i):
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            try:
                all_status = task_widget.findChildren(QLabel, "status")
                all_status[i].setText("Card Declined")
                all_status[i].setStyleSheet(
                    "color: red;"
                    "font-weight: bold;"
                )
            except:
                pass

    def task_run_sold_out(self, i):
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            try:
                all_status = task_widget.findChildren(QLabel, "status")
                all_status[i].setText("Sold Out")
                all_status[i].setStyleSheet(
                    "color: red;"
                    "font-weight: bold;"
                )
            except:
                pass

    def task_run_restock(self, i):
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            try:
                all_status = task_widget.findChildren(QLabel, "status")
                all_status[i].setText("Trying Restock")
                all_status[i].setStyleSheet(
                    "color: #fc9803;"
                    "font-weight: bold;"
                )
            except:
                pass

    def startTasks(self, is_all, i, objects):
        all_tasks = task_handler.get_all_tasks()
        all_accounts = account_handler.get_all_accounts()
        all_proxies = proxy_handler.get_all_proxies()

        num_tasks = task_handler.get_num_tasks()
        num_accounts = account_handler.get_num_accounts()
        num_proxies = proxy_handler.get_num_proxies()

        default_settings = settings_handler.get_all_settings()
        default_account = default_settings["default account"]

        if num_accounts < num_tasks:
            diff = num_tasks - num_accounts
            for _ in range(diff):
                all_accounts.append(default_account)

        if num_proxies < num_tasks:
            diff = num_tasks - num_proxies
            for _ in range(diff):
                all_proxies.append(False)

        self.tasks_thread_pool = QThreadPool()

        if is_all:
            try:
                for object in objects:
                    img_path = os.path.join(self.application_path, 'images/stoptaskIcon.icns')
                    object.setIcon(QIcon(img_path))
            except:
                pass
            self.worker = TaskWorker(True, i, all_tasks, all_accounts, all_proxies)  # this worker is used to seperate functions away from interface and it runs however many tasks in the class
        else:
            img_path = os.path.join(self.application_path, 'images/stopTaskIcon.icns')
            objects[i].setIcon(QIcon(img_path))
            self.worker = TaskWorker(False, i, all_tasks, all_accounts, all_proxies)

        self.worker.signals.started.connect(self.task_run_started)
        self.worker.signals.started_ind.connect(self.task_run_started_ind)
        self.worker.signals.searching.connect(self.task_run_searching)
        self.worker.signals.found.connect(self.task_run_found)
        self.worker.signals.cart.connect(self.task_run_cart)
        self.worker.signals.checkout.connect(self.task_run_checkout)
        self.worker.signals.success.connect(self.task_run_success)
        self.worker.signals.stopped.connect(self.task_run_stopped)
        self.worker.signals.stopped_ind.connect(self.task_run_stopped_ind)
        self.worker.signals.cart_error.connect(self.task_run_cart_error)
        self.worker.signals.captcha_error.connect(self.task_run_captcha_error)
        self.worker.signals.card_declined.connect(self.task_run_card_declined)
        self.worker.signals.sold_out.connect(self.task_run_sold_out)
        self.worker.signals.restock.connect(self.task_run_restock)

        self.tasks_thread_pool.start(self.worker)


    def startTask(self, objects):
        stop_task = False
        try:
            sender = self.sender()
            index = 0
            i = 0
            for object in objects:
                if sender == object:
                    i = index
                    break
                index += 1
            if self.tasks_thread_pool:
                stop_task = True
            if stop_task:
                img_path = os.path.join(self.application_path, 'images/iconstart.icns')
                objects[i].setIcon(QIcon(img_path))
                self.stopTasks(False, i)
            else:
                img_path = os.path.join(self.application_path, 'images/stopTaskIcon.icns')
                objects[i].setIcon(QIcon(img_path))
                self.startTasks(False, i, objects)
        except:
            sender = self.sender()
            index = 0
            i = 0
            for object in objects:
                if sender == object:
                    i = index
                    break
                index += 1
            img_path = os.path.join(self.application_path, 'images/stopTaskIcon.icns')
            objects[i].setIcon(QIcon(img_path))
            self.startTasks(False, i, objects)

    def stopTasks(self, is_all, index):
        num_tasks = task_handler.get_num_tasks()
        if num_tasks > 0:
            if is_all:
                try:
                    if self.tasks_thread_pool:
                        self.worker.stop_task(True, index)
                except:
                    pass
            else:
                try:
                    if self.tasks_thread_pool:
                        self.worker.stop_task(False, index)
                except:
                    pass

    def task_run_stopped_ind(self, i):
        all_tasks = task_handler.get_tasks_as_string()
        all_tasks_widgets = self.tasksScrollView.findChildren(QWidget, "tasksWidget")
        for task_widget in all_tasks_widgets:
            all_status = task_widget.findChildren(QLabel, "status")
            if all_tasks[i][5] == 'Manual       ':
                all_status[i].setText("Ready to start...")
            else:
                all_status[i].setText(f"Starting at {all_tasks[i][5]}")
            all_status[i].setStyleSheet(
                "color: #ffffff;"
                "font-weight: bold;"
            )

    def task_run_stopped(self):
        self.resetDashboardUI()

    def checkAllTasks(self):
        num_tasks = task_handler.get_num_tasks()
        checkboxes = self.tasksWidget.findChildren(QCheckBox)
        for i in range(0, num_tasks):
            self.checkbox = checkboxes[i]
            if self.checkbox.isChecked():
                self.checkbox.setChecked(False)
            else:
                self.checkbox.setChecked(True)
                
    def deleteTasks(self):
        index = 0
        indexes = []
        checkboxes = self.tasksWidget.findChildren(QCheckBox)
        for checkbox in checkboxes:
            if checkbox.isChecked():
                indexes.append(index)
            index += 1
        all_tasks = task_handler.get_all_tasks()
        count = 0
        try:
            for indice in indexes:
                all_tasks.pop(indice - count)
                count += 1
        except:
            pass
        task_handler.insert_tasks(all_tasks)
        self.resetDashboardUI()

    def addTasksWindow(self):
        self.addTasksWindow = AddTasksWindow()
        self.addTasksWindow.show()

    def quickTasksWindow(self):
        self.quickTasksWindow = QuickTasksWindow()
        self.quickTasksWindow.show()

    def editTasksWindow(self):
        checks = 0
        index = 0
        indexes = []
        tasks = []
        checkboxes = self.tasksWidget.findChildren(QCheckBox)
        for checkbox in checkboxes:
            if checkbox.isChecked():
                indexes.append(index)
                checks += 1
            index += 1
        all_tasks = task_handler.get_all_tasks()
        count = 0
        try:
            for indice in indexes:
                tasks.append(all_tasks[indice - count])
                count += 1
            product = tasks[0][1]
            size = tasks[0][2]
            delay = tasks[0][3]
            delay = delay[:-2]
        except:
            pass

        if checks > 0:
            self.editTasksWindow = EditTasksWindow(indexes, product, size, delay)
            self.editTasksWindow.show()

    def editTask(self, objects):
        sender = self.sender()
        index = 0
        for object in objects:
            if sender == object:
                tasks = task_handler.get_task_at_index(index)
                break
            else:
                index += 1
        product = tasks[1]
        size = tasks[2]
        delay = tasks[3]
        delay = delay[:-2]
        self.editTaskWindow = EditTaskWindow(index, product, size, delay)
        self.editTaskWindow.show()

    def deleteTask(self, objects):
        sender = self.sender()
        index = 0
        i = 0
        for object in objects:
            if sender == object:
                i = index
                break
            index += 1
        all_tasks = task_handler.get_all_tasks()
        del_task = task_handler.get_task_at_index(i)
        all_tasks.remove(del_task)
        task_handler.insert_tasks(all_tasks)
        self.resetDashboardUI()

    # ACCOUNTS

    def accountsUI(self):
        num_accounts = account_handler.get_num_accounts()
        self.accountsLabel = QLabel(f"Accounts   [{num_accounts}]")
        self.accountsLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 20px;"
            "font-weight: bold;"
        )
        self.importAccountsButton = QPushButton("Import")
        img_path = os.path.join(self.application_path, 'images/importicon.icns')
        self.importAccountsButton.setIcon(QIcon(img_path))
        self.importAccountsButton.setStyleSheet(
            """
            QPushButton {
                background-color: #000000;
                color: #03c6fc;
                border: 2px solid #03c6fc;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #101010;
                border: 3px solid #03c6fc;
            }
            QPushButton:pressed {
                background-color: #000000;
            }
            """
        )
        self.exportAccountsButton = QPushButton("Export")
        img_path = os.path.join(self.application_path, 'images/exporticon.icns')
        self.exportAccountsButton.setIcon(QIcon(img_path))
        self.exportAccountsButton.setStyleSheet(
            """
            QPushButton {
                background-color: #000000;
                color: #03c6fc;
                border: 2px solid #03c6fc;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #101010;
                border: 3px solid #03c6fc;
            }
            QPushButton:pressed {
                background-color: #000000;
            }
            """
        )
        self.selectAllAccountsButton = QPushButton("Select All")
        img_path = os.path.join(self.application_path, 'images/checkIcon.icns')
        self.selectAllAccountsButton.setIcon(QIcon(img_path))
        self.selectAllAccountsButton.setStyleSheet(
            """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #ffffff;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #dcdcdc;
                border: 2px solid #dcdcdc;
            }
            QPushButton:pressed {
                background-color: #ffffff;
            }
            """
        )
        self.selectAllAccountsButton.hide()
        self.deleteAccountsButton = QPushButton("Delete Accounts")
        img_path = os.path.join(self.application_path, 'images/trashIcon.icns')
        self.deleteAccountsButton.setIcon(QIcon(img_path))
        self.deleteAccountsButton.setStyleSheet(
            """
            QPushButton {
                background-color: #fc9803;
                color: #000000;
                border: 2px solid #fc9803;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #e38902;
                border: 2px solid #e38902;
            }
            QPushButton:pressed {
                background-color: #fc9803;
            }
            """
        )
        self.deleteAccountsButton.hide()
        num_accounts = account_handler.get_num_accounts()
        if num_accounts != 0:
            self.selectAllAccountsButton.show()
            self.deleteAccountsButton.show()
        self.refreshAccountsButton = QPushButton("Refresh Feed")
        img_path = os.path.join(self.application_path, 'images/refreshIcon.icns')
        self.refreshAccountsButton.setIcon(QIcon(img_path))
        self.refreshAccountsButton.setStyleSheet(
            """
            QPushButton {
                background-color: #000000;
                color: #03c6fc;
                border: 2px solid #03c6fc;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #101010;
                border: 3px solid #03c6fc;
            }
            QPushButton:pressed {
                background-color: #000000;
            }
            """
        )
        self.accountsHeaderBox = QVBoxLayout()
        self.accountsHeaderBoxTop = QHBoxLayout()
        self.accountsHeaderBoxTop.addWidget(self.accountsLabel)
        self.accountsHeaderBoxTop.addStretch()
        self.accountsHeaderBoxTop.addWidget(self.importAccountsButton)
        self.accountsHeaderBoxTop.addWidget(self.exportAccountsButton)
        self.accountsHeaderBoxTop.addWidget(self.selectAllAccountsButton)
        self.accountsHeaderBoxTop.addWidget(self.deleteAccountsButton)
        self.accountsHeaderBoxTop.addWidget(self.refreshAccountsButton)
        self.nameLabel = QLabel('              Name')
        self.nameLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
            "padding-left: 1px;"
        )
        self.nameLabel.setFixedWidth(200)
        self.nameLabel.setAlignment(Qt.AlignLeft)
        self.emailLabel = QLabel('                Email')
        self.emailLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
        )
        self.emailLabel.setFixedWidth(200)
        self.emailLabel.setAlignment(Qt.AlignLeft)
        self.addressLabel = QLabel('                 Address')
        self.addressLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
            "margin-left: -5px;"
        )
        self.addressLabel.setFixedWidth(200)
        self.addressLabel.setAlignment(Qt.AlignLeft)
        self.billingLabel = QLabel('                  Billing')
        self.billingLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
        )
        self.billingLabel.setFixedWidth(200)
        self.billingLabel.setAlignment(Qt.AlignLeft)
        self.controlsLabel2 = QLabel('                         Controls')
        self.controlsLabel2.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
        )
        self.controlsLabel2.setFixedWidth(200)
        self.controlsLabel2.setAlignment(Qt.AlignLeft)
        self.accountsHeaderBoxBottom = QHBoxLayout()
        self.accountsHeaderBoxBottom.setContentsMargins(0, 30, 0, 0)
        self.accountsHeaderBoxBottom.addStretch()
        self.accountsHeaderBoxBottom.addWidget(self.nameLabel)
        self.accountsHeaderBoxBottom.addStretch()
        self.accountsHeaderBoxBottom.addWidget(self.emailLabel)
        self.accountsHeaderBoxBottom.addStretch()
        self.accountsHeaderBoxBottom.addWidget(self.addressLabel)
        self.accountsHeaderBoxBottom.addStretch()
        self.accountsHeaderBoxBottom.addWidget(self.billingLabel)
        self.accountsHeaderBoxBottom.addStretch()
        self.accountsHeaderBoxBottom.addWidget(self.controlsLabel2)
        self.accountsHeaderBoxBottom.addStretch()
        self.accountsHeaderBox.addLayout(self.accountsHeaderBoxTop)
        self.accountsHeaderBox.addLayout(self.accountsHeaderBoxBottom)
        # sub-header
        self.accountsScrollView = QScrollArea()
        self.accountsWidget = QWidget()
        self.accountsBox = QVBoxLayout()
        self.accountsBox.setSpacing(5)
        self.showAccounts()
        self.accountsScrollView.setWidget(self.accountsWidget)
        self.accountsScrollView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.accountsScrollView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.accountsScrollView.setWidgetResizable(True)
        self.accountsButtonsBox = QHBoxLayout()
        self.addAccountsButton = QPushButton("＋    Add Account")
        self.addAccountsButton.setStyleSheet(
            """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border-radius: 5px;
                padding: 10px 110px 7px 110px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton::hover {
                background-color: #dcdcdc;
            }
            QPushButton:pressed {
                background-color: #ffffff;
            }
            """
        )
        self.accountsButtonsBox.addStretch()
        self.accountsButtonsBox.addWidget(self.addAccountsButton)
        self.accountsButtonsBox.addStretch()
        self.accountsBodyBox = QVBoxLayout()
        self.accountsBodyBox.addWidget(self.accountsScrollView)
        self.accountsBodyBox.addLayout(self.accountsButtonsBox)
        self.accounts = QVBoxLayout()
        self.accounts.addLayout(self.accountsHeaderBox)
        self.accounts.addLayout(self.accountsBodyBox)
        self.accounts.setStretch(1, 2)
        self.accountsTab.setLayout(self.accounts)
        self.refreshAccountsButton.clicked.connect(self.resetAccountsUI)
        self.addAccountsButton.clicked.connect(self.addAccountsWindow)

    def resetAccountsUI(self):
        while self.accountsBox.count():
            child2 = self.accountsBox.takeAt(0)
            if child2.widget():
                child2.widget().deleteLater()
        num_accounts = account_handler.get_num_accounts()
        if num_accounts != 0:
            self.showAccounts()
            self.selectAllAccountsButton.show()
            self.deleteAccountsButton.show()
        else:
            self.showAccounts()
            self.selectAllAccountsButton.hide()
            self.deleteAccountsButton.hide()

        self.accountsLabel.setText(f"Accounts   [{num_accounts}]")
        self.accountsLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 20px;"
            "font-weight: bold;"
        )

    def showAccounts(self):
        edit_objects_list = []
        delete_objects_list = []
        num_accounts = account_handler.get_num_accounts()
        if num_accounts > 0:
            all_accounts = account_handler.get_accounts_as_string()
            for i in range(0, num_accounts):
                account = all_accounts[i]
                self.accountsWidgetBox = QWidget()
                self.accountsWidgetBox.setStyleSheet(
                    "background-color: #000000;"
                    "border-radius: 5px;"
                )
                self.accountLine = QHBoxLayout()
                self.name = QLabel(str(i + 1) + '   ' + account[0])
                self.name.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.name.setAlignment(Qt.AlignLeft)
                self.name.setFixedWidth(200)
                self.email = QLabel(account[1])
                self.email.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.email.setAlignment(Qt.AlignLeft)
                self.email.setFixedWidth(200)
                self.address = QLabel(account[2])
                self.address.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.address.setAlignment(Qt.AlignLeft)
                self.address.setFixedWidth(200)
                self.billing = QLabel(account[3])
                self.billing.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.billing.setAlignment(Qt.AlignLeft)
                self.billing.setFixedWidth(200)

                self.editButtonAccounts = QPushButton()
                img_path = os.path.join(self.application_path, 'images/iconedit.icns')
                self.editButtonAccounts.setIcon(QIcon(img_path))
                self.editButtonAccounts.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #000000;
                        color: #000000;
                        border-radius: 5px;
                        padding: 0px;
                        font-weight: bold;
                    }
                    QPushButton::hover {
                        background-color: #FF00FF;
                    }
                    QPushButton:pressed {
                        background-color: #000000;
                    }
                    """
                )
                edit_objects_list.append(self.editButtonAccounts)
                self.editButtonAccounts.setObjectName("editButtonAccounts")
                self.deleteButtonAccounts = QPushButton()
                img_path = os.path.join(self.application_path, 'images/icontrash.icns')
                self.deleteButtonAccounts.setIcon(QIcon(img_path))
                self.deleteButtonAccounts.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #000000;
                        color: #000000;
                        border-radius: 5px;
                        padding: 0px;
                        font-weight: bold;
                    }
                    QPushButton::hover {
                        background-color: #FF00FF;
                    }
                    QPushButton:pressed {
                        background-color: #000000;
                    }
                    """
                )
                delete_objects_list.append(self.deleteButtonAccounts)
                self.deleteButtonAccounts.setObjectName("deleteButtonAccounts")
                self.checkboxAccounts = QCheckBox()
                self.accountLine.addWidget(self.checkboxAccounts)
                self.accountLine.addStretch()
                self.accountLine.addWidget(self.name)
                self.accountLine.addStretch()
                self.accountLine.addWidget(self.email)
                self.accountLine.addStretch()
                self.accountLine.addWidget(self.address)
                self.accountLine.addStretch()
                self.accountLine.addWidget(self.billing)
                self.accountLine.addStretch()
                self.accountLine.addStretch()
                self.accountLine.addWidget(self.editButtonAccounts)
                self.accountLine.addStretch()
                self.accountLine.addWidget(self.deleteButtonAccounts)
                self.accountLine.addStretch()
                self.accountsWidgetBox.setLayout(self.accountLine)
                self.accountsWidgetBox.setFixedHeight(40)
                self.accountsBox.addWidget(self.accountsWidgetBox)

        else:
            self.accountsWidgetBox = QWidget()
            self.accountLine = QHBoxLayout()
            self.accountsLabelNone = QLabel("Add accounts to get started.")
            self.accountsLabelNone.setStyleSheet(
                "color: #ffffff;"
                "font-size: 15px;"
                "border-bottom: 2px solid #fc9803;"
                "border-radius: 0px;"
                "padding: 5px;"
            )
            self.accountsLabelNone.setAlignment(Qt.AlignCenter)
            self.accountLine.addStretch()
            self.accountLine.addWidget(self.accountsLabelNone)
            self.accountLine.addStretch()
            self.accountsWidgetBox.setLayout(self.accountLine)
            self.accountsWidgetBox.setFixedHeight(50)
            self.accountsBox.addWidget(self.accountsWidgetBox)

        self.accountsWidget.setLayout(self.accountsBox)
        self.accountsWidget.setObjectName("accountsWidget")
        self.accountsScrollView.setWidget(self.accountsWidget)
        self.selectAllAccountsButton.clicked.connect(self.checkAllAccounts)
        self.deleteAccountsButton.clicked.connect(self.deleteAccounts)
        self.importAccountsButton.clicked.connect(self.importAccounts)
        self.exportAccountsButton.clicked.connect(self.exportAccounts)

        widgets = self.accountsScrollView.findChildren(QWidget, "accountsWidget")
        for widget in widgets:
            try:
                editButtons = widget.findChildren(QPushButton, 'editButtonAccounts')
                for e in range(0, len(editButtons)):
                    editButtons[e].clicked.connect(lambda: self.editAccount(edit_objects_list))
            except:
                pass

        widgets2 = self.accountsScrollView.findChildren(QWidget, "accountsWidget")
        for widget2 in widgets2:
            try:
                deleteButtons = widget2.findChildren(QPushButton, 'deleteButtonAccounts')
                for e in range(0, len(deleteButtons)):
                    deleteButtons[e].clicked.connect(lambda: self.deleteAccount(delete_objects_list))
            except:
                pass

    def checkAllAccounts(self):
        num_accounts = account_handler.get_num_accounts()
        checkboxes = self.accountsWidget.findChildren(QCheckBox)
        for i in range(0, num_accounts):
            self.checkbox = checkboxes[i]
            if self.checkbox.isChecked():
                self.checkbox.setChecked(False)
            else:
                self.checkbox.setChecked(True)

    def deleteAccounts(self):
        index = 0
        indexes = []
        checkboxes = self.accountsWidget.findChildren(QCheckBox)
        for checkbox in checkboxes:
            if checkbox.isChecked():
                indexes.append(index)
            index += 1
        all_accounts = account_handler.get_all_accounts()
        count = 0
        try:
            for indice in indexes:
                all_accounts.pop(indice - count)
                count += 1
        except:
            pass
        account_handler.insert_accounts(all_accounts)
        self.resetAccountsUI()

    def importAccounts(self):
        for i in range(1):
            filename, _ = QFileDialog.getOpenFileName(self, "Select a csv file to open...", QDir.homePath(), 'CSV Files (*.csv)', 'CSV Files (*.csv)')
            import_handler.import_file(filename)

    def exportAccounts(self):
        for i in range(1):
            filename, _ = QFileDialog.getSaveFileName(self, "Create a csv file to save to...", QDir.homePath(), 'CSV Files (*.csv)', 'CSV Files (*.csv)')
            export_handler.export_file(filename)

    def addAccountsWindow(self):
        self.addAccountsWindow = AddAccountsWindow()
        self.addAccountsWindow.show()

    def editAccount(self, objects):
        sender = self.sender()
        index = 0
        for object in objects:
            if sender == object:
                account = account_handler.get_account(index)
                break
            else:
                index += 1
        first = account[0]
        last = account[1]
        email = account[2]
        phone = account[3]
        street = account[4]
        city = account[5]
        state = account[6]
        zip = account[7]
        number = account[8]
        exp = account[9]
        cvv = account[10]
        name = account[11]
        billingStreet = account[12]
        billingCity = account[13]
        billingState = account[14]
        billingZip = account[15]
        self.editAccountWindow = EditAccountsWindow(index, first, last, email, phone, street, city, state, zip, number, exp, cvv, name, billingStreet, billingCity, billingState, billingZip)
        self.editAccountWindow.show()

    def deleteAccount(self, objects):
        sender = self.sender()
        index = 0
        i = 0
        for object in objects:
            if sender == object:
                i = index
                break
            index += 1
        all_accounts = account_handler.get_all_accounts()
        del_account = account_handler.get_account(i)
        all_accounts.remove(del_account)
        account_handler.insert_accounts(all_accounts)
        self.resetAccountsUI()

    # PROXIES

    def proxiesUI(self):
        num_proxies = proxy_handler.get_num_proxies()
        self.proxiesLabel = QLabel(f"Proxies   [{num_proxies}]")
        self.proxiesLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 20px;"
            "font-weight: bold;"
        )
        self.selectAllProxiesButton = QPushButton("Select All")
        img_path = os.path.join(self.application_path, 'images/checkIcon.icns')
        self.selectAllProxiesButton.setIcon(QIcon(img_path))
        self.selectAllProxiesButton.setStyleSheet(
            """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #ffffff;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #dcdcdc;
                border: 2px solid #dcdcdc;
            }
            QPushButton:pressed {
                background-color: #ffffff;
            }
            """
        )
        self.selectAllProxiesButton.hide()
        self.deleteProxiesButton = QPushButton("Delete Proxies")
        img_path = os.path.join(self.application_path, 'images/trashIcon.icns')
        self.deleteProxiesButton.setIcon(QIcon(img_path))
        self.deleteProxiesButton.setStyleSheet(
            """
            QPushButton {
                background-color: #fc9803;
                color: #000000;
                border: 2px solid #fc9803;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #e38902;
                border: 2px solid #e38902;
            }
            QPushButton:pressed {
                background-color: #fc9803;
            }
            """
        )
        self.deleteProxiesButton.hide()
        num_proxies = proxy_handler.get_num_proxies()
        if num_proxies != 0:
            self.selectAllProxiesButton.show()
            self.deleteProxiesButton.show()
        self.refreshProxiesButton = QPushButton("Refresh Feed")
        img_path = os.path.join(self.application_path, 'images/refreshIcon.icns')
        self.refreshProxiesButton.setIcon(QIcon(img_path))
        self.refreshProxiesButton.setStyleSheet(
            """
            QPushButton {
                background-color: #000000;
                color: #03c6fc;
                border: 2px solid #03c6fc;
                border-radius: 5px;
                padding: 5px 20px 5px 20px;
                font-weight: bold;
            }
            QPushButton::hover {
                background-color: #101010;
                border: 3px solid #03c6fc;
            }
            QPushButton:pressed {
                background-color: #000000;
            }
            """
        )
        self.proxiesHeaderBox = QVBoxLayout()
        self.proxiesHeaderBoxTop = QHBoxLayout()
        self.proxiesHeaderBoxTop.addWidget(self.proxiesLabel)
        self.proxiesHeaderBoxTop.addStretch()
        # self.proxiesHeaderBoxTop.addWidget(self.importProxiesButton)
        # self.proxiesHeaderBoxTop.addWidget(self.exportProxiesButton)
        self.proxiesHeaderBoxTop.addWidget(self.selectAllProxiesButton)
        self.proxiesHeaderBoxTop.addWidget(self.deleteProxiesButton)
        self.proxiesHeaderBoxTop.addWidget(self.refreshProxiesButton)
        self.portLabel = QLabel('            Port')
        self.portLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
            "padding-left: 1px;"
        )
        self.portLabel.setFixedWidth(200)
        self.portLabel.setAlignment(Qt.AlignLeft)
        self.ipLabel = QLabel('            IP')
        self.ipLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
            "margin-left: -5px;"
        )
        self.ipLabel.setFixedWidth(200)
        self.ipLabel.setAlignment(Qt.AlignLeft)
        self.statusLabel = QLabel('          Status')
        self.statusLabel.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
        )
        self.statusLabel.setFixedWidth(200)
        self.statusLabel.setAlignment(Qt.AlignLeft)
        self.controlsLabel3 = QLabel('                         Controls')
        self.controlsLabel3.setStyleSheet(
            "font-size: 15px;"
            "color: #03c6fc;"
            "font-weight: bold;"
        )
        self.controlsLabel3.setFixedWidth(200)
        self.controlsLabel3.setAlignment(Qt.AlignLeft)
        self.proxiesHeaderBoxBottom = QHBoxLayout()
        self.proxiesHeaderBoxBottom.setContentsMargins(0, 30, 0, 0)
        self.proxiesHeaderBoxBottom.addStretch()
        self.proxiesHeaderBoxBottom.addWidget(self.portLabel)
        self.proxiesHeaderBoxBottom.addStretch()
        self.proxiesHeaderBoxBottom.addWidget(self.ipLabel)
        self.proxiesHeaderBoxBottom.addStretch()
        self.proxiesHeaderBoxBottom.addWidget(self.statusLabel)
        self.proxiesHeaderBoxBottom.addStretch()
        self.proxiesHeaderBoxBottom.addWidget(self.controlsLabel3)
        self.proxiesHeaderBoxBottom.addStretch()
        self.proxiesHeaderBox.addLayout(self.proxiesHeaderBoxTop)
        self.proxiesHeaderBox.addLayout(self.proxiesHeaderBoxBottom)
        # sub-header
        self.proxiesScrollView = QScrollArea()
        self.proxiesWidget = QWidget()
        self.proxiesBox = QVBoxLayout()
        self.proxiesBox.setSpacing(5)
        self.showProxies()
        self.proxiesScrollView.setWidget(self.proxiesWidget)
        self.proxiesScrollView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.proxiesScrollView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.proxiesScrollView.setWidgetResizable(True)
        self.proxiesButtonsBox = QHBoxLayout()
        self.addProxiesButton = QPushButton("＋    Add Proxies")
        self.addProxiesButton.setStyleSheet(
            """
            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border-radius: 5px;
                padding: 10px 110px 7px 110px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton::hover {
                background-color: #dcdcdc;
            }
            QPushButton:pressed {
                background-color: #ffffff;
            }
            """
        )
        self.testProxiesButton = QPushButton("    Test Proxies")
        img_path = os.path.join(self.application_path, 'images/testicon.icns')
        self.testProxiesButton.setIcon(QIcon(img_path))
        self.testProxiesButton.setStyleSheet(
            """
            QPushButton {
                background-color: #03c6fc;
                color: #000000;
                border-radius: 5px;
                padding: 12px 110px 10px 110px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton::hover {
                background-color: #03b2e3;
            }
            QPushButton:pressed {
                background-color: #03c6fc;
            }
            """
        )
        self.captchaHarvesterButton = QPushButton("    Captcha Harvester")
        self.captchaHarvesterButton.setIcon(QIcon('images/harvesticon.icns'))
        self.captchaHarvesterButton.setStyleSheet(
            "color: #000000;"
            "background-color: #fc9803;"
            "font-size: 15px;"
            "padding: 12px 50px 10px 50px;"
            "border-radius: 5px;"
            "font-weight: bold;"
        )
        self.proxiesButtonsBox.addStretch()
        self.proxiesButtonsBox.addWidget(self.addProxiesButton)
        self.proxiesButtonsBox.addWidget(self.testProxiesButton)
        self.proxiesButtonsBox.addStretch()
        #self.proxiesButtonsBox.addWidget(self.captchaHarvesterButton)
        self.proxiesBodyBox = QVBoxLayout()
        self.proxiesBodyBox.addWidget(self.proxiesScrollView)
        self.proxiesBodyBox.addLayout(self.proxiesButtonsBox)
        self.proxies = QVBoxLayout()
        self.proxies.addLayout(self.proxiesHeaderBox)
        self.proxies.addLayout(self.proxiesBodyBox)
        self.proxies.setStretch(1, 2)
        self.proxiesTab.setLayout(self.proxies)
        self.refreshProxiesButton.clicked.connect(self.resetProxiesUI)
        self.addProxiesButton.clicked.connect(self.addProxyWindow)
        self.testProxiesButton.clicked.connect(self.proxies_tester)

    def resetProxiesUI(self):
        while self.proxiesBox.count():
            child3 = self.proxiesBox.takeAt(0)
            if child3.widget():
                child3.widget().deleteLater()
        num_proxies = proxy_handler.get_num_proxies()
        if num_proxies != 0:
            self.showProxies()
            self.selectAllProxiesButton.show()
            self.deleteProxiesButton.show()
        else:
            self.showProxies()
            self.selectAllProxiesButton.hide()
            self.deleteProxiesButton.hide()

        self.proxiesLabel.setText(f"Proxies   [{num_proxies}]")
        self.proxiesLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 20px;"
            "font-weight: bold;"
        )

    def showProxies(self):
        edit_objects_list_proxies = []
        test_objects_list_proxies = []
        delete_objects_list_proxies = []
        num_proxies = proxy_handler.get_num_proxies()
        if num_proxies > 0:
            all_proxies = proxy_handler.get_all_proxies()
            for i in range(0, num_proxies):
                proxy = all_proxies[i]
                self.proxiesWidgetBox = QWidget()
                self.proxiesWidgetBox.setStyleSheet(
                    "background-color: #000000;"
                    "border-radius: 5px;"
                )
                self.proxyLine = QHBoxLayout()
                self.port = QLabel(str(i + 1) + '    ' + proxy[0])
                self.port.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.port.setAlignment(Qt.AlignLeft)
                self.port.setFixedWidth(200)
                self.ip = QLabel(proxy[1])
                self.ip.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.ip.setAlignment(Qt.AlignLeft)
                self.ip.setFixedWidth(200)
                self.status2 = QLabel("Untested")
                self.status2.setStyleSheet(
                    "color: #ffffff;"
                    "font-weight: bold;"
                )
                self.status2.setAlignment(Qt.AlignLeft)
                self.status2.setFixedWidth(200)
                self.status2.setObjectName("proxyStatus")

                self.editButtonProxies = QPushButton()
                img_path = os.path.join(self.application_path, 'images/iconedit.icns')
                self.editButtonProxies.setIcon(QIcon(img_path))
                self.editButtonProxies.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #000000;
                        color: #000000;
                        border-radius: 5px;
                        padding: 0px;
                        font-weight: bold;
                    }
                    QPushButton::hover {
                        background-color: #FF00FF;
                    }
                    QPushButton:pressed {
                        background-color: #000000;
                    }
                    """
                )
                edit_objects_list_proxies.append(self.editButtonProxies)
                self.editButtonProxies.setObjectName("editButtonProxies")
                self.testButtonProxies = QPushButton()
                img_path = os.path.join(self.application_path, 'images/icontest.icns')
                self.testButtonProxies.setIcon(QIcon(img_path))
                self.testButtonProxies.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #000000;
                        color: #000000;
                        border-radius: 5px;
                        padding: 0px;
                        font-weight: bold;
                    }
                    QPushButton::hover {
                        background-color: #FF00FF;
                    }
                    QPushButton:pressed {
                        background-color: #000000;
                    }
                    """
                )
                test_objects_list_proxies.append(self.testButtonProxies)
                self.testButtonProxies.setObjectName("testButtonProxies")
                self.deleteButtonProxies = QPushButton()
                img_path = os.path.join(self.application_path, 'images/icontrash.icns')
                self.deleteButtonProxies.setIcon(QIcon(img_path))
                self.deleteButtonProxies.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #000000;
                        color: #000000;
                        border-radius: 5px;
                        padding: 0px;
                        font-weight: bold;
                    }
                    QPushButton::hover {
                        background-color: #FF00FF;
                    }
                    QPushButton:pressed {
                        background-color: #000000;
                    }
                    """
                )
                self.deleteButtonProxies.setObjectName("deleteButtonProxies")
                delete_objects_list_proxies.append(self.deleteButtonProxies)
                self.checkboxProxies = QCheckBox()
                self.proxyLine.addWidget(self.checkboxProxies)
                self.proxyLine.addStretch()
                self.proxyLine.addWidget(self.port)
                self.proxyLine.addStretch()
                self.proxyLine.addWidget(self.ip)
                self.proxyLine.addStretch()
                self.proxyLine.addWidget(self.status2)
                self.proxyLine.addStretch()
                self.proxyLine.addStretch()
                self.proxyLine.addWidget(self.editButtonProxies)
                #self.proxyLine.addStretch()
                self.proxyLine.addWidget(self.testButtonProxies)
                #self.proxyLine.addStretch()
                self.proxyLine.addWidget(self.deleteButtonProxies)
                self.proxyLine.addStretch()
                self.proxiesWidgetBox.setLayout(self.proxyLine)
                self.proxiesWidgetBox.setFixedHeight(40)
                self.proxiesBox.addWidget(self.proxiesWidgetBox)

        else:
            self.proxiesWidgetBox = QWidget()
            self.proxyLine = QHBoxLayout()
            self.proxiesLabelNone = QLabel("Add proxies to get started.")
            self.proxiesLabelNone.setStyleSheet(
                "color: #ffffff;"
                "font-size: 15px;"
                "border-bottom: 2px solid #fc9803;"
                "border-radius: 0px;"
                "padding: 5px;"
            )
            self.proxiesLabelNone.setAlignment(Qt.AlignCenter)
            self.proxyLine.addStretch()
            self.proxyLine.addWidget(self.proxiesLabelNone)
            self.proxyLine.addStretch()
            self.proxiesWidgetBox.setLayout(self.proxyLine)
            self.proxiesWidgetBox.setFixedHeight(50)
            self.proxiesBox.addWidget(self.proxiesWidgetBox)

        self.proxiesWidget.setLayout(self.proxiesBox)
        self.proxiesWidget.setObjectName("proxiesWidget")
        self.proxiesScrollView.setWidget(self.proxiesWidget)
        self.selectAllProxiesButton.clicked.connect(self.checkAllProxies)
        self.deleteProxiesButton.clicked.connect(self.deleteProxies)

        widgets3 = self.proxiesScrollView.findChildren(QWidget, "proxiesWidget")
        for widget3 in widgets3:
            try:
                editButtons = widget3.findChildren(QPushButton, 'editButtonProxies')
                for e in range(0, len(editButtons)):
                    editButtons[e].clicked.connect(lambda: self.editProxy(edit_objects_list_proxies))
            except:
                pass

        widgets4 = self.proxiesScrollView.findChildren(QWidget, "proxiesWidget")
        for widget4 in widgets4:
            try:
                editButtons = widget4.findChildren(QPushButton, 'deleteButtonProxies')
                for e in range(0, len(editButtons)):
                    editButtons[e].clicked.connect(lambda: self.deleteProxy(delete_objects_list_proxies))
            except:
                pass

        widgets5 = self.proxiesScrollView.findChildren(QWidget, "proxiesWidget")
        for widget5 in widgets5:
            try:
                testButtons = widget5.findChildren(QPushButton, 'testButtonProxies')
                for e in range(0, len(testButtons)):
                    testButtons[e].clicked.connect(lambda: self.testProxy(test_objects_list_proxies))
            except:
                pass

    def checkAllProxies(self):
        num_proxies = proxy_handler.get_num_proxies()
        checkboxes = self.proxiesWidget.findChildren(QCheckBox)
        for i in range(0, num_proxies):
            self.checkbox = checkboxes[i]
            if self.checkbox.isChecked():
                self.checkbox.setChecked(False)
            else:
                self.checkbox.setChecked(True)

    def deleteProxies(self):
        index = 0
        indexes = []
        checkboxes = self.proxiesWidget.findChildren(QCheckBox)
        for checkbox in checkboxes:
            if checkbox.isChecked():
                indexes.append(index)
            index += 1
        all_proxies = proxy_handler.get_all_proxies()
        count = 0
        try:
            for indice in indexes:
                all_proxies.pop(indice - count)
                count += 1
        except:
            pass
        proxy_handler.insert_proxies(all_proxies)
        self.resetProxiesUI()

    def addProxyWindow(self):
        self.addProxyWindow = AddProxyWindow()
        self.addProxyWindow.show()

    # executes when progress is made (does nothing rn)
    def execute_proxy_tests_fn(self, progress_callback):
        pass

    # executes when process starts
    def show_proxy_tests_output(self):
        num_proxies = proxy_handler.get_num_proxies()
        if num_proxies > 0:

            all_proxies_widgets = self.proxiesScrollView.findChildren(QWidget, "proxiesWidget")
            for proxy_widget in all_proxies_widgets:
                try:
                    all_proxy_status = proxy_widget.findChildren(QLabel, "proxyStatus")
                    for e in range(0, len(all_proxy_status)):
                        all_proxy_status[e].setText("Running now...                 ")
                        all_proxy_status[e].setStyleSheet(
                            "color: #fc9803;"
                            "font-weight: bold;"
                        )
                except:
                    pass

    # executes when process finishes
    def proxy_testing_thread_complete(self, result, i):
        widgets7 = self.proxiesScrollView.findChildren(QWidget, "proxiesWidget")
        for widget7 in widgets7:
            statusLabels = widget7.findChildren(QLabel, "proxyStatus")
            if result[0] == True:
                result[1] = round(result[1], 2)
                statusLabels[i].setText(f"Valid:    {result[1]} ms")
                statusLabels[i].setStyleSheet(
                    "font-weight: bold;"
                    "color: #00FF00;"
                )
            else:
                statusLabels[i].setText(f"Invalid")
                statusLabels[i].setStyleSheet(
                    "font-weight: bold;"
                    "color: red;"
                )
        # set values as the status

    # actual method that starts threads
    def proxies_tester(self):
        num_proxies = proxy_handler.get_num_proxies()
        if num_proxies > 0:
            self.proxies_thread_pool = QThreadPool()

            worker = ProxiesWorker(self.execute_proxy_tests_fn)
            worker.signals.result.connect(self.show_proxy_tests_output)
            worker.signals.finished.connect(self.proxy_testing_thread_complete)

            self.proxies_thread_pool.start(worker)

    def editProxy(self, objects):
        sender = self.sender()
        index = 0
        for object in objects:
            if sender == object:
                proxy = proxy_handler.get_proxy(index)
                break
            else:
                index += 1
        port = proxy[0]
        ip = proxy[1]
        self.editProxyWindow = EditProxyWindow(index, port, ip)
        self.editProxyWindow.show()

    def deleteProxy(self, objects):
        sender = self.sender()
        index = 0
        i = 0
        for object in objects:
            if sender == object:
                i = index
                break
            index += 1
        all_proxies = proxy_handler.get_all_proxies()
        del_proxy = proxy_handler.get_proxy(i)
        all_proxies.remove(del_proxy)
        proxy_handler.insert_proxies(all_proxies)
        self.resetProxiesUI()

    def execute_proxy_test_fn(self, progress_callback):
        pass

    def show_proxy_test_output(self, i):
        num_proxies = proxy_handler.get_num_proxies()
        if num_proxies > 0:

            all_proxies_widgets = self.proxiesScrollView.findChildren(QWidget, "proxiesWidget")
            for proxy_widget in all_proxies_widgets:
                try:
                    all_proxy_status = proxy_widget.findChildren(QLabel, "proxyStatus")
                    all_proxy_status[i].setText("Running now...                 ")
                    all_proxy_status[i].setStyleSheet(
                        "color: #fc9803;"
                        "font-weight: bold;"
                    )
                except:
                    pass

    def proxy_test_thread_complete(self, result):
        widgets6 = self.proxiesScrollView.findChildren(QWidget, "proxiesWidget")
        for widget6 in widgets6:
            try:
                statusLabels = widget6.findChildren(QLabel, 'proxyStatus')
                if result[0] == True:
                    result[1] = round(result[1], 2)
                    statusLabels[result[2]].setText(f"Valid:    {result[1]} ms")
                    statusLabels[result[2]].setStyleSheet(
                        "font-weight: bold;"
                        "color: #00FF00;"
                    )
                else:
                    statusLabels[result[1]].setText("Invalid")
                    statusLabels[result[1]].setStyleSheet(
                        "font-weight: bold;"
                        "color: red;"
                    )
            except:
                pass

    def testProxy(self, objects):
        sender = self.sender()
        index = 0
        i = 0
        for object in objects:
            if sender == object:
                i = index
                break
            index += 1

        self.proxy_thread_pool = QThreadPool()

        worker = ProxyWorker(self.execute_proxy_test_fn, i)
        worker.signals.result.connect(lambda: self.show_proxy_test_output(i))
        worker.signals.finished.connect(self.proxy_test_thread_complete)

        self.proxy_thread_pool.start(worker)


    # SETTINGS

    def settingsUI(self):
        settings = settings_handler.get_all_settings()

        self.mainSettingslayout = QVBoxLayout()
        self.mainSettingslayout.setStretch(1, 2)
        self.settingsBodyBox = QHBoxLayout()
        self.dashboardSettingsBox = QGridLayout()
        self.dashboardSettingsLabel = QLabel("Dashboard Settings")
        self.dashboardSettingsLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 20px;"
            "font-weight: bold;"
        )
        self.dashboardSettingsLabel.setAlignment(Qt.AlignHCenter)
        self.safeModeLabel = QLabel("safe Mode")
        self.safeModeLabel.setStyleSheet(
            "color: #ffffff;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.safeModeCheckbox = QCheckBox()
        self.fastModeLabel = QLabel("fast Mode")
        self.fastModeLabel.setStyleSheet(
            "color: #ffffff;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.fastModeCheckbox = QCheckBox()
        if settings["safe mode"] == True:
            self.safeModeCheckbox.setChecked(True)
            self.fastModeCheckbox.setChecked(False)
        else:
            self.fastModeCheckbox.setChecked(True)
            self.safeModeCheckbox.setChecked(False)
        self.monitorDelayLabel = QLabel("monitor delay")
        self.monitorDelayLabel.setStyleSheet(
            "color: #ffffff;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.monitorDelayInput = QLineEdit()
        self.monitorDelayInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.monitorDelayInput.setText(str(settings["monitor delay"]))
        self.retryDelayLabel = QLabel("retry delay")
        self.retryDelayLabel.setStyleSheet(
            "color: #ffffff;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.retryDelayInput = QLineEdit()
        self.retryDelayInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.retryDelayInput.setText(str(settings["retry delay"]))
        self.defaultTaskLabel = QLabel("Default Settings For Quick Tasks")
        self.defaultTaskLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.defaultSizeLabel = QLabel("default size")
        self.defaultSizeLabel.setStyleSheet(
            "color: #ffffff;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.defaultSizeInput = QComboBox()
        self.defaultSizeInput.addItems(
            ['Select Size', 'Random', '6.0', '6.5', '7.0', '7.5', '8.0', '8.5', '9.0', '9.5', '10.0', '10.5', '11.0',
             '11.5', '12.0',
             '12.5', '13.0', 'S', 'M', 'L', 'XL'])
        self.defaultSizeInput.setStyleSheet(
            """        
            QComboBox QAbstractItemView {
                border: 1px solid white;
                background: white;
                selection-background-color: blue;
            }
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
        self.defaultDelayLabel = QLabel("default delay")
        self.defaultDelayLabel.setStyleSheet(
            "color: #ffffff;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.defaultDelayInput = QLineEdit()
        self.defaultDelayInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        if len(settings["quick task default"]) > 0:
            self.defaultSizeInput.setCurrentText(settings["quick task default"][0])
            self.defaultDelayInput.setText(str(settings["quick task default"][1]))
        self.emptyDashSettingsWidget1 = QLabel()
        self.emptyDashSettingsWidget2 = QLabel()
        self.emptyDashSettingsWidget3 = QLabel()
        self.emptyDashSettingsWidget4 = QLabel()
        self.emptyDashSettingsWidget5 = QLabel()
        self.emptyDashSettingsWidget6 = QLabel()
        self.emptyDashSettingsWidget7 = QLabel()
        self.defaultQuickTaskButton = QPushButton("Save")
        self.defaultQuickTaskButton.setStyleSheet(
            """
            QPushButton {
                color: #000000;
                background-color: #fc9803;
                font-size: 15px;
                padding: 5px 25px 5px 25px;
                border-radius: 5px;
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
        self.dashboardSettingsBox.addWidget(self.dashboardSettingsLabel, 0, 0, 0, 0)
        self.dashboardSettingsBox.addWidget(self.emptyDashSettingsWidget6, 1, 0, 1, 1)
        self.dashboardSettingsBox.addWidget(self.safeModeLabel, 2, 0, 1, 1)
        self.dashboardSettingsBox.addWidget(self.safeModeCheckbox, 2, 1, 1, 1)
        self.dashboardSettingsBox.addWidget(self.fastModeLabel, 3, 0, 1, 1)
        self.dashboardSettingsBox.addWidget(self.fastModeCheckbox, 3, 1, 1, 1)
        self.dashboardSettingsBox.addWidget(self.monitorDelayLabel, 4, 0, 1, 1)
        self.dashboardSettingsBox.addWidget(self.monitorDelayInput, 4, 1, 1, 1)
        self.dashboardSettingsBox.addWidget(self.retryDelayLabel, 5, 0, 1, 1)
        self.dashboardSettingsBox.addWidget(self.retryDelayInput, 5, 1, 1, 1)
        self.dashboardSettingsBox.addWidget(self.defaultTaskLabel, 6, 0, 1, 2)
        self.dashboardSettingsBox.addWidget(self.defaultSizeLabel, 7, 0, 1, 1)
        self.dashboardSettingsBox.addWidget(self.defaultSizeInput, 7, 1, 1, 1)
        self.dashboardSettingsBox.addWidget(self.defaultDelayLabel, 8, 0, 1, 1)
        self.dashboardSettingsBox.addWidget(self.defaultDelayInput, 8, 1, 1, 1)
        self.dashboardSettingsBox.addWidget(self.emptyDashSettingsWidget1, 9, 0, 1, 1)
        self.dashboardSettingsBox.addWidget(self.emptyDashSettingsWidget2, 10, 0, 1, 1)
        self.dashboardSettingsBox.addWidget(self.emptyDashSettingsWidget3, 11, 0, 1, 1)
        self.dashboardSettingsBox.addWidget(self.emptyDashSettingsWidget4, 12, 0, 1, 1)
        self.dashboardSettingsBox.addWidget(self.emptyDashSettingsWidget5, 13, 0, 1, 1)
        self.dashboardSettingsBox.addWidget(self.defaultQuickTaskButton, 14, 0, 1, 2)
        # account settings
        self.accountSettingsBox = QGridLayout()
        self.accountSettingsLabel = QLabel("Account Settings")
        self.accountSettingsLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 20px;"
            "font-weight: bold;"
        )
        self.accountSettingsLabel.setAlignment(Qt.AlignHCenter)
        self.defaultAccountLabel = QLabel("default account settings")
        self.defaultAccountLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.defaultFirstNameInput = QLineEdit()
        self.defaultFirstNameInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultFirstNameInput.setText("")
        self.defaultFirstNameInput.setPlaceholderText("First")
        self.defaultLastNameInput = QLineEdit()
        self.defaultLastNameInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultLastNameInput.setText("")
        self.defaultLastNameInput.setPlaceholderText("last")
        self.defaultEmailInput = QLineEdit()
        self.defaultEmailInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultEmailInput.setText("")
        self.defaultEmailInput.setPlaceholderText("email")
        self.defaultPhoneInput = QLineEdit()
        self.defaultPhoneInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultPhoneInput.setText("")
        self.defaultPhoneInput.setPlaceholderText("phone")
        self.defaultAddressInput = QLineEdit()
        self.defaultAddressInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultAddressInput.setText("")
        self.defaultAddressInput.setPlaceholderText("address")
        self.defaultCityInput = QLineEdit()
        self.defaultCityInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultCityInput.setText("")
        self.defaultCityInput.setPlaceholderText("city")
        self.defaultStateInput = QComboBox()
        self.defaultStateInput.addItems(
            ['Select State', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
             'KS', 'KY', 'LA',
             'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
             'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
        )
        self.defaultStateInput.setStyleSheet(
            """
            QComboBox QAbstractItemView {
                border: 1px solid white;
                background: white;
                selection-background-color: blue;
            }
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
        self.defaultZipInput = QLineEdit()
        self.defaultZipInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultZipInput.setText("")
        self.defaultZipInput.setPlaceholderText("zip")
        self.defaultCardInput = QLineEdit()
        self.defaultCardInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultCardInput.setText("")
        self.defaultCardInput.setPlaceholderText("card number")
        self.defaultExpInput = QLineEdit()
        self.defaultExpInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultExpInput.setText("")
        self.defaultExpInput.setPlaceholderText("exp")
        self.defaultCVVInput = QLineEdit()
        self.defaultCVVInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultCVVInput.setText("")
        self.defaultCVVInput.setPlaceholderText("cvv")
        self.defaultCardNameInput = QLineEdit()
        self.defaultCardNameInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultCardNameInput.setText("")
        self.defaultCardNameInput.setPlaceholderText("name")
        self.defaultBillingAddressInput = QLineEdit()
        self.defaultBillingAddressInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultBillingAddressInput.setText("")
        self.defaultBillingAddressInput.setPlaceholderText("billing address")
        self.defaultBillingCityInput = QLineEdit()
        self.defaultBillingCityInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultBillingCityInput.setText("")
        self.defaultBillingCityInput.setPlaceholderText("billing city")
        self.defaultBillingStateInput = QComboBox()
        self.defaultBillingStateInput.addItems(
            ['Select State', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
             'KS', 'KY', 'LA',
             'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
             'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
        )
        self.defaultBillingStateInput.setStyleSheet(
            """
            QComboBox QAbstractItemView {
                border: 1px solid white;
                background: white;
                selection-background-color: blue;
            }
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
        self.defaultBillingZipInput = QLineEdit()
        self.defaultBillingZipInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultBillingZipInput.setText("")
        self.defaultBillingZipInput.setPlaceholderText("billing zip")
        self.defaultAccountButton = QPushButton("Save")
        self.defaultAccountButton.setStyleSheet(
            """
            QPushButton {
                color: #000000;
                background-color: #fc9803;
                font-size: 15px;
                padding: 5px 25px 5px 25px;
                border-radius: 5px;
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
        self.emptyWidget = QLabel()
        if len(settings["default account"]) > 0:
            self.defaultFirstNameInput.setText(settings["default account"][0])
            self.defaultLastNameInput.setText(settings["default account"][1])
            self.defaultEmailInput.setText(settings["default account"][2])
            self.defaultPhoneInput.setText(settings["default account"][3])
            self.defaultAddressInput.setText(settings["default account"][4])
            self.defaultCityInput.setText(settings["default account"][5])
            self.defaultStateInput.setCurrentText(settings["default account"][6])
            self.defaultZipInput.setText(settings["default account"][7])
            self.defaultCardInput.setText(settings["default account"][8])
            self.defaultExpInput.setText(settings["default account"][9])
            self.defaultCVVInput.setText(settings["default account"][10])
            self.defaultCardNameInput.setText(settings["default account"][11])
            self.defaultBillingAddressInput.setText(settings["default account"][12])
            self.defaultBillingCityInput.setText(settings["default account"][13])
            self.defaultBillingStateInput.setCurrentText(settings["default account"][14])
            self.defaultBillingZipInput.setText(settings["default account"][15])
        self.accountSettingsBox.addWidget(self.accountSettingsLabel, 1, 0, 1, 2)
        self.accountSettingsBox.addWidget(self.defaultAccountLabel, 2, 0, 1, 2)
        self.accountSettingsBox.addWidget(self.defaultFirstNameInput, 3, 0, 1, 1)
        self.accountSettingsBox.addWidget(self.defaultLastNameInput, 3, 1, 1, 1)
        self.accountSettingsBox.addWidget(self.defaultEmailInput, 4, 0, 1, 2)
        self.accountSettingsBox.addWidget(self.defaultPhoneInput, 5, 0, 1, 2)
        self.accountSettingsBox.addWidget(self.defaultAddressInput, 6, 0, 1, 2)
        self.accountSettingsBox.addWidget(self.defaultCityInput, 7, 0, 1, 2)
        self.accountSettingsBox.addWidget(self.defaultStateInput, 8, 0, 1, 1)
        self.accountSettingsBox.addWidget(self.defaultZipInput, 8, 1, 1, 1)
        self.accountSettingsBox.addWidget(self.defaultCardInput, 9, 0, 1, 2)
        self.accountSettingsBox.addWidget(self.defaultExpInput, 10, 0, 1, 1)
        self.accountSettingsBox.addWidget(self.defaultCVVInput, 10, 1, 1, 1)
        self.accountSettingsBox.addWidget(self.defaultCardNameInput, 11, 0, 1, 2)
        self.accountSettingsBox.addWidget(self.defaultBillingAddressInput, 12, 0, 1, 2)
        self.accountSettingsBox.addWidget(self.defaultBillingCityInput, 13, 0, 1, 2)
        self.accountSettingsBox.addWidget(self.defaultBillingStateInput, 14, 0, 1, 1)
        self.accountSettingsBox.addWidget(self.defaultBillingZipInput, 14, 1, 1, 1)
        self.accountSettingsBox.addWidget(self.defaultAccountButton, 15, 0, 1, 2)
        # # proxy settings
        self.proxySettingsBox = QGridLayout()
        self.proxySettingsLabel = QLabel("Proxy Settings")
        self.proxySettingsLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 20px;"
            "font-weight: bold;"
        )
        self.proxySettingsLabel.setAlignment(Qt.AlignHCenter)
        self.runProxiesLabel = QLabel("run proxies untested")
        self.runProxiesLabel.setStyleSheet(
            "color: #ffffff;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.runProxiesCheckbox = QCheckBox()
        if settings["run proxies untested"] == False:
            self.runProxiesCheckbox.setChecked(False)
        else:
            self.runProxiesCheckbox.setChecked(True)
        self.manualCaptchaLabel = QLabel("manual captcha")
        self.manualCaptchaLabel.setStyleSheet(
            "color: #ffffff;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.manualCaptchaCheckbox = QCheckBox()
        self.defaultHarvesterLabel = QLabel("Default captcha harvester website")
        self.defaultHarvesterLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.defaultHarvesterInput = QLineEdit()
        self.defaultHarvesterInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.defaultHarvesterInput.setText(settings["harvester website"])
        self.defaultHarvesterInput.setPlaceholderText("website")
        self.automatedCaptchaLabel = QLabel("automated captcha")
        self.automatedCaptchaLabel.setStyleSheet(
            "color: #ffffff;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.automatedCaptchaCheckbox = QCheckBox()
        if settings["manual captcha"] == False:
            self.manualCaptchaCheckbox.setChecked(False)
            self.automatedCaptchaCheckbox.setChecked(True)
        else:
            self.manualCaptchaCheckbox.setChecked(True)
            self.automatedCaptchaCheckbox.setChecked(False)
        self.defaultAutomatedLabel = QLabel("captcha serrvice api key")
        self.defaultAutomatedLabel.setStyleSheet(
            "color: #fc9803;"
            "font-size: 15px;"
            "font-weight: bold;"
        )
        self.apiKeyInput = QLineEdit()
        self.apiKeyInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #000000;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.apiKeyInput.setPlaceholderText("Api key")
        self.apiKeyInput.setText(settings["api key"])
        self.emptyDashSettingsWidget5 = QLabel()
        self.emptyDashSettingsWidget6 = QLabel()
        self.emptyDashSettingsWidget7 = QLabel()
        self.emptyDashSettingsWidget8 = QLabel()
        self.emptyDashSettingsWidget9 = QLabel()
        self.emptyDashSettingsWidget10 = QLabel()
        self.emptyDashSettingsWidget11 = QLabel()
        self.proxySettingsButton = QPushButton("Save")
        self.proxySettingsButton.setStyleSheet(
            "color: #000000;"
            "background-color: #fc9803;"
            "font-size: 15px;"
            "padding: 5px 25px 5px 25px;"
            "border-radius: 5px;"
            "font-weight: bold;"
        )
        self.proxySettingsBox.addWidget(self.proxySettingsLabel, 0, 0, 0, 0)
        self.proxySettingsBox.addWidget(self.emptyDashSettingsWidget11, 1, 0, 1, 1)
        self.proxySettingsBox.addWidget(self.runProxiesLabel, 2, 0, 1, 1)
        self.proxySettingsBox.addWidget(self.runProxiesCheckbox, 2, 1, 1, 1)
        self.proxySettingsBox.addWidget(self.manualCaptchaLabel, 3, 0, 1, 1)
        self.proxySettingsBox.addWidget(self.manualCaptchaCheckbox, 3, 1, 1, 1)
        self.proxySettingsBox.addWidget(self.defaultHarvesterLabel, 4, 0, 1, 2)
        self.proxySettingsBox.addWidget(self.defaultHarvesterInput, 5, 0, 1, 2)
        self.proxySettingsBox.addWidget(self.automatedCaptchaLabel, 6, 0, 1, 1)
        self.proxySettingsBox.addWidget(self.automatedCaptchaCheckbox, 6, 1, 1, 1)
        self.proxySettingsBox.addWidget(self.defaultAutomatedLabel, 7, 0, 1, 2)
        self.proxySettingsBox.addWidget(self.apiKeyInput, 8, 0, 1, 2)
        self.proxySettingsBox.addWidget(self.emptyDashSettingsWidget5, 9, 0, 1, 1)
        self.proxySettingsBox.addWidget(self.emptyDashSettingsWidget6, 10, 0, 1, 1)
        self.proxySettingsBox.addWidget(self.emptyDashSettingsWidget7, 11, 0, 1, 1)
        self.proxySettingsBox.addWidget(self.emptyDashSettingsWidget8, 12, 0, 1, 1)
        self.proxySettingsBox.addWidget(self.emptyDashSettingsWidget9, 13, 0, 1, 1)
        self.proxySettingsBox.addWidget(self.proxySettingsButton, 14, 0, 1, 2)

        self.settingsBodyBox.addLayout(self.dashboardSettingsBox)
        self.settingsBodyBox.addLayout(self.accountSettingsBox)
        #self.settingsBodyBox.addLayout(self.proxySettingsBox)

        self.settingsFooterBox = QVBoxLayout()
        self.validLabelSettings = QLabel("Status: valid")
        self.validLabelSettings.setStyleSheet(
            "color: #00FF00;"
            "font-weight: bold;"
            "font-size: 15px;"
        )
        self.validLabelSettings.setContentsMargins(0, 0, 0, 0)
        self.settingsResetWebhook = QHBoxLayout()
        self.resetSettingsButton = QPushButton("Reset Settings")
        self.resetSettingsButton.setStyleSheet(
            """
            QPushButton {
                background-color: #303030;
                color: #03c6fc;
                border: 2px solid #03c6fc;
                border-radius: 5px;
                padding: 5px 25px 5px 25px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton::hover {
                background-color: #202020;
                border: 3px solid #03c6fc;
            }
            QPushButton:pressed {
                background-color: #000000;
            }
            """
        )
        self.webhookHBox = QHBoxLayout()
        self.webhookLabel = QLabel("Webhook")
        self.webhookLabel.setStyleSheet(
            "color: #03c6fc;"
            "font-weight: bold;"
            "font-size: 15px;"
        )
        self.webhookInput = QLineEdit()
        self.webhookInput.setStyleSheet(
            "color: #03c6fc;"
            "background-color: #303030;"
            "border: 1px solid #03c6fc;"
            "border-radius: 0px;"
        )
        self.webhookInput.setPlaceholderText("discord")
        self.webhookInput.setText(settings["webhook"])
        self.saveWebhookButton = QPushButton("save")
        self.saveWebhookButton.setStyleSheet(
            """
            QPushButton {
                color: #303030;
                background-color: #03c6fc;
                font-size: 15px;
                padding: 1px 5px 1px 5px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #03b2e3;
            }
            QPushButton:pressed {
                background-color: #03c6fc;
            }
            """
        )
        self.webhookHBox.addWidget(self.webhookLabel)
        self.webhookHBox.addWidget(self.webhookInput)
        self.webhookHBox.addWidget(self.saveWebhookButton)
        self.settingsResetWebhook.addWidget(self.resetSettingsButton)
        self.settingsResetWebhook.addStretch()
        self.settingsResetWebhook.addLayout(self.webhookHBox)
        self.settingsDownloadUpdates = QHBoxLayout()
        self.downloadUserManualButton = QPushButton("Download user manual")
        self.downloadUserManualButton.setStyleSheet(
            """
            QPushButton {
                background-color: #303030;
                color: #03c6fc;
                border: 2px solid #03c6fc;
                border-radius: 5px;
                padding: 5px 25px 5px 25px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton::hover {
                background-color: #202020;
                border: 3px solid #03c6fc;
            }
            QPushButton:pressed {
                background-color: #000000;
            }
            """
        )
        self.updatesHBox = QHBoxLayout()
        self.autoUpdatesLabel = QLabel("Automatic Updates")
        self.autoUpdatesLabel.setStyleSheet(
            "color: #03c6fc;"
            "font-weight: bold;"
            "font-size: 15px;"
        )
        self.autoUpdatesInput = QCheckBox()
        self.autoUpdatesInput.setChecked(True)
        self.updatesHBox.addWidget(self.autoUpdatesLabel)
        self.updatesHBox.addWidget(self.autoUpdatesInput)
        self.settingsDownloadUpdates.addWidget(self.downloadUserManualButton)
        self.settingsDownloadUpdates.addStretch()
        self.settingsDownloadUpdates.addWidget(self.validLabelSettings)
        self.settingsDownloadUpdates.addStretch()
        self.settingsDownloadUpdates.addLayout(self.updatesHBox)

        self.settingsFooterBox.addLayout(self.settingsResetWebhook)
        self.settingsFooterBox.addLayout(self.settingsDownloadUpdates)

        self.settingsFooterWidget = QWidget()
        self.settingsFooterWidget.setStyleSheet(
            "background-color: #303030;"
            "border-radius: 5px;"
        )
        self.settingsFooterWidget.setContentsMargins(0, 0, 0, 0)
        self.settingsFooterWidget.setLayout(self.settingsFooterBox)

        self.mainSettingslayout.addLayout(self.settingsBodyBox)
        self.mainSettingslayout.addWidget(self.settingsFooterWidget)
        self.settingsTab.setLayout(self.mainSettingslayout)

        self.safeModeCheckbox.toggled.connect(self.toggleSafeMode)
        self.fastModeCheckbox.toggled.connect(self.toggleFastMode)

        self.manualCaptchaCheckbox.toggled.connect(self.toggleCaptchaManual)
        self.automatedCaptchaCheckbox.toggled.connect(self.toggleCaptchaAutomated)

        self.defaultQuickTaskButton.clicked.connect(self.saveDashboardSettings)
        self.defaultAccountButton.clicked.connect(self.saveAccountSettings)
        self.proxySettingsButton.clicked.connect(self.saveProxySettings)

        self.saveWebhookButton.clicked.connect(self.saveWebhook)
        self.resetSettingsButton.clicked.connect(self.resetSettings)

    def resetSettings(self):
        settings_handler.set_setting("safe mode", True)
        settings_handler.set_setting("monitor delay", 0)
        settings_handler.set_setting("retry delay", 0)
        settings_handler.set_setting("quick task default", ["Select Size", 0])
        settings_handler.set_setting("default account", ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        settings_handler.set_setting("webhook", "")
        self.safeModeCheckbox.setChecked(True)
        self.fastModeCheckbox.setChecked(False)
        self.monitorDelayInput.setText('0')
        self.retryDelayInput.setText('0')
        self.defaultSizeInput.setCurrentText("Select Size")
        self.defaultDelayInput.setText('0')
        self.defaultFirstNameInput.setText('')
        self.defaultLastNameInput.setText('')
        self.defaultEmailInput.setText('')
        self.defaultPhoneInput.setText('')
        self.defaultAddressInput.setText('')
        self.defaultCityInput.setText('')
        self.defaultStateInput.setCurrentText('Select State')
        self.defaultZipInput.setText('')
        self.defaultCardInput.setText('')
        self.defaultExpInput.setText('')
        self.defaultCVVInput.setText('')
        self.defaultCardNameInput.setText('')
        self.defaultBillingAddressInput.setText('')
        self.defaultBillingCityInput.setText('')
        self.defaultBillingStateInput.setCurrentText('Select State')
        self.defaultBillingZipInput.setText('')

    def toggleSafeMode(self):
        if self.safeModeCheckbox.isChecked():
            self.fastModeCheckbox.setChecked(False)
            self.safeModeCheckbox.setChecked(True)
        else:
            self.fastModeCheckbox.setChecked(True)
            self.safeModeCheckbox.setChecked(False)

    def toggleFastMode(self):
        if self.fastModeCheckbox.isChecked():
            self.fastModeCheckbox.setChecked(True)
            self.safeModeCheckbox.setChecked(False)
        else:
            self.fastModeCheckbox.setChecked(False)
            self.safeModeCheckbox.setChecked(True)

    def saveWebhook(self):
        webhook = self.webhookInput.text()
        settings_handler.set_setting("webhook", webhook)

    def toggleCaptchaManual(self):
        if self.manualCaptchaCheckbox.isChecked():
            self.automatedCaptchaCheckbox.setChecked(False)
            self.manualCaptchaCheckbox.setChecked(True)
        else:
            self.automatedCaptchaCheckbox.setChecked(True)
            self.manualCaptchaCheckbox.setChecked(False)

    def toggleCaptchaAutomated(self):
        if self.automatedCaptchaCheckbox.isChecked():
            self.automatedCaptchaCheckbox.setChecked(True)
            self.manualCaptchaCheckbox.setChecked(False)
        else:
            self.automatedCaptchaCheckbox.setChecked(False)
            self.manualCaptchaCheckbox.setChecked(True)

    def saveDashboardSettings(self):
        if self.safeModeCheckbox.isChecked():
            safe_mode = True
        else:
            safe_mode = False
        monitor_delay = int(self.monitorDelayInput.text())
        retry_delay = int(self.retryDelayInput.text())
        default_size = self.defaultSizeInput.currentText()
        default_delay = int(self.defaultDelayInput.text())
        settings_handler.set_setting("safe mode", safe_mode)
        settings_handler.set_setting("monitor delay", monitor_delay)
        settings_handler.set_setting("retry delay", retry_delay)
        settings_handler.set_setting("quick task default", [default_size, default_delay])

    def saveAccountSettings(self):
        first = self.defaultFirstNameInput.text()
        last = self.defaultLastNameInput.text()
        email = self.defaultEmailInput.text()
        phone = self.defaultPhoneInput.text()
        address = self.defaultAddressInput.text()
        city = self.defaultCityInput.text()
        state = self.defaultStateInput.currentText()
        zip = self.defaultZipInput.text()
        number = self.defaultCardInput.text()
        exp = self.defaultExpInput.text()
        cvv = self.defaultCVVInput.text()
        name = self.defaultCardNameInput.text()
        bill_add = self.defaultBillingAddressInput.text()
        bill_city = self.defaultBillingCityInput.text()
        bill_state = self.defaultBillingStateInput.currentText()
        bill_zip = self.defaultBillingZipInput.text()
        settings_handler.set_setting("default account", [first, last, email, phone, address, city, state, zip, number, exp, cvv, name, bill_add, bill_city, bill_state, bill_zip])

    def saveProxySettings(self):
        if self.runProxiesCheckbox.isChecked():
            run_proxies_untested = True
        else:
            run_proxies_untested = False
        if self.manualCaptchaCheckbox.isChecked():
            manual_captcha = True
        else:
            manual_captcha = False
        harvester_website = self.defaultHarvesterInput.text()
        api_key = self.apiKeyInput.text()
        settings_handler.set_setting("run proxies untested", run_proxies_untested)
        settings_handler.set_setting("manual captcha", manual_captcha)
        settings_handler.set_setting("harvester website", harvester_website)
        settings_handler.set_setting("api key", api_key)


def isValid():
    settings = settings_handler.get_all_settings()

    if "valid" in settings.keys():
        if settings["valid"] == True:
            return True
        else:
            return False
    else:
        return False

def checkStatus():
    valid = isValid()
    if valid:
        main()
    else:
        onStartup()

def onStartup():
    App = QApplication(sys.argv)
    keyVerificationWindow = KeyVerificationWindow()
    sys.exit(App.exec_())

def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())


if __name__ == '__main__':
    checkStatus()
