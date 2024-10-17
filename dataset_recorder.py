from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds, MindroveConfigMode
import sys
import time
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
        self.setGeometry(100,100,400,400)
        
        self.label = QLabel(self)
        #self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.images = [QPixmap('right.png'),QPixmap('left.png')]
        self.trigger_count = 0
    
    def start(self):
        thread = threading.Thread(target=self.run_process)
        thread.start()
    
    def run_process(self):
        total_duration = 32
        trigger_interval = 4
        display_time = 4
        
        for i in range(int(total_duration/(trigger_interval+display_time))):
            time.sleep(trigger_interval)
            self.trigger_event()
            time.sleep(display_time)
            self.label.clear()
        
        self.close()
    
    def trigger_event(self):
        self.label.setPixmap(self.images[self.trigger_count])
        self.trigger_count +=1


class arc_board:
    def __init__(self, window_size, board_shim, board_id):
        self.window_size = window_size
        self.board_shim = board_shim
        self.eeg_channels = BoardShim.get_eeg_channels(board_id)
        self.trigger_channel = BoardShim.get_other_channels(19)
        self.sampling_rate = BoardShim.get_sampling_rate(board_id)
        self.num_points = window_size * self.sampling_rate
        
    def prepare_session(self):
        self.board_shim.prepare_session()
    def start_streaming(self):
        self.board_shim.start_stream()
    def stop_streaming(self):
        self.board_shim.stop_stream()
    def release_session(self):
        self.board_shim.release_session()
    
    def record_window(self):
        while True:
            if self.board_shim.get_board_data_count() >= self.num_points:
                data = self.board_shim.get_board_data(self.num_points)
                eeg_data = data[self.eeg_channels]
                triggers = data[19]
                break
        return [eeg_data,triggers]
    
    def BEEP(self):
        self.board_shim.config_board(MindroveConfigMode.BEEP)
    def BOOP(self):
        self.board_shim.config_board(MindroveConfigMode.BOOP)

def run_arc():
    BoardShim.enable_dev_board_logger() # enable logger when developing to catch relevant logs 

    params = MindRoveInputParams() 
    board_id = BoardIds.MINDROVE_WIFI_BOARD
    board_shim = BoardShim(board_id, params)
    window_size = 2 # seconds
    
    arc_board(window_size, board_shim, board_id)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = TriggeredImageApp()
    ex.show()
    ex.start()
    sys.exit(app.exec_())