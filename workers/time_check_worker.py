from PyQt5.QtCore import *
import time


class WorkerSignals(QObject):
    timematch = pyqtSignal() #index


class Worker(QRunnable):
    def __init__(self, time_list):
        super(Worker, self).__init__()
        self.time_list = time_list
        self.signals = WorkerSignals()
        self.started_times = [] # indexes, not times because times can repeat
        self.terminate = False

    @pyqtSlot()
    def run(self):
        times_list = []
        for val in self.time_list:
            if val:
                times_list.append(val)
        is_running = True
        while is_running:
            if not self.terminate:
                t = time.localtime()
                curr_time = str(time.strftime("%H:%M", t))  # hour, minute in 24 hr time
                index = 0
                if not self.terminate:
                    for ind_time in self.time_list:
                        if not self.terminate:
                            if ind_time: #means its not false, or it doesnt start manually
                                if index not in self.started_times:
                                    if ind_time == curr_time:
                                        self.started_times.append(index)
                            index += 1
                        else:
                            is_running = False
                    if not self.terminate:
                        if len(times_list) == len(self.started_times):
                            self.signals.timematch.emit() # when all times are equal, so start with only supporting running at one time
                            is_running = False # stop
                        time.sleep(10)
                    else:
                        is_running = False
                else:
                    is_running = False
            else:
                is_running = False
        return

    def reset_timer(self):
        self.signals.blockSignals(True)
        self.terminate = True