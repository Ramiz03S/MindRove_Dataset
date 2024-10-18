from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds, MindroveConfigMode
import sys
import time
import random
import threading
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap
#from PySide6 import QtCore

class TriggeredImageApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('MindRove Dataset')
        self.setGeometry(400,400,600,600)
        
        self.cross = QLabel(self)
        self.label = QLabel(self)
        #self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(self.cross)
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.images = [QPixmap('right.png'),QPixmap('left.png'),QPixmap('cross.png')]
    
    
    def show_cross(self):
        self.cross.setPixmap(self.images[2])
    def clear_cross(self):
        self.cross.clear()
    def show_image(self, trigger_class):
        self.label.setPixmap(self.images[trigger_class])
    def clear_image(self):
        self.label.clear()

class arc_board:
    def __init__(self, board_shim, board_id):
        self.board_shim = board_shim
        self.eeg_channels = BoardShim.get_eeg_channels(board_id)
        self.trigger_channel = BoardShim.get_other_channels(19)
        self.sampling_rate = BoardShim.get_sampling_rate(board_id)
        
    def prepare_session(self):
        self.board_shim.prepare_session()
    def start_streaming(self):
        self.board_shim.start_stream()
    def stop_streaming(self):
        self.board_shim.stop_stream()
    def release_session(self):
        self.board_shim.release_session()
    
    def record_window(self, window_size):
        num_points = int(window_size * self.sampling_rate)
        data = self.board_shim.get_board_data(num_points)
        eeg_data = data[self.eeg_channels]
        triggers = data[19]
        return [eeg_data,triggers]
    
    def BEEP_BOOP(self, trigger_class):
        if trigger_class == 0:
            self.board_shim.config_board(MindroveConfigMode.BEEP)
        if trigger_class == 1:
            self.board_shim.config_board(MindroveConfigMode.BOOP)

def init_arc():
    BoardShim.enable_dev_board_logger() # enable logger when developing to catch relevant logs 
    params = MindRoveInputParams() 
    board_id = BoardIds.MINDROVE_WIFI_BOARD
    board_shim = BoardShim(board_id, params)
    return arc_board(board_shim, board_id)


def run(display, arc_board, trigger_class):

    time.sleep(4)
    display.show_image(trigger_class)
    arc_board.BEEP_BOOP(trigger_class)
    time.sleep(4)
    display.clear_image()

def multiple_runs():
    trigger_list = [0] * 12 + [1] * 12
    random.shuffle(trigger_list)

    arc_board = init_arc()
    app = QApplication(sys.argv)
    display = TriggeredImageApp()
    arc_board.prepare_session()
    
    display.show()
    display.show_cross()
    
    arc_board.start_streaming()
    start_time = time.time()
    
    for i in trigger_list:
        run(display,arc_board,i)
    end_time = time.time()
    arc_board.stop_streaming()
    sys.exit(app.exec_())
    
    run_time = end_time - start_time
    data, triggers = arc_board.record_window(run_time)
    arc_board.release_session()
    
    
if __name__ == "__main__":
    multiple_runs()