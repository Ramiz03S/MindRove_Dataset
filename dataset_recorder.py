from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds, MindroveConfigMode
import sys
import time
import random
import threading
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap, QScreen
from PySide6.QtCore import QObject, Signal, Qt

class trigger_communicator(QObject):
    update_image_signal = Signal(int)
    toggle_image_signal = Signal()
    stop_signal = Signal()
    toggle_cross_signal = Signal()

class TriggeredImageApp(QWidget):
    def __init__(self, communicator):
        super().__init__()
        
        self.setWindowTitle('MindRove Dataset')
        self.setGeometry(400,400,1000,1000)
        self.setStyleSheet("background-color: white;")
        
        self.cross = QLabel(parent=self)
        self.label = QLabel(parent=self)
        
        # vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        # layout.addWidget(self.cross)
        hlayout.addWidget(self.cross, alignment=Qt.AlignCenter)
        hlayout.addWidget(self.label, alignment=Qt.AlignCenter)
        # vlayout.addLayout(hlayout)
        # vlayout.alignment(Qt.AlignCenter)
        self.setLayout(hlayout)
        
        self.images = [QPixmap('right.png'),QPixmap('left.png')]
        self.cross.setPixmap(QPixmap('cross.png').scaled(400,400))
        
        communicator.update_image_signal.connect(self.update_image)
        communicator.toggle_image_signal.connect(self.toggle_image)
        communicator.stop_signal.connect(self.close_window)
        communicator.toggle_cross_signal.connect(self.toggle_cross)

    def update_image(self, trigger_class):
        self.label.setPixmap(self.images[trigger_class].scaled(400,400))
    def toggle_image(self):
        if self.label.isVisible():
            self.label.hide()
        else:
            self.label.show()
    def toggle_cross(self):
        if self.cross.isVisible():
            self.cross.hide()
        else:
            self.cross.show()
        
    def close_window(self):
        self.label.setText("RUN ENDED")
        self.close()
    # def show_cross(self):
    #     self.cross.setPixmap(self.images[2])
    # def clear_cross(self):
    #     self.cross.clear()
    # def show_image(self, trigger_class):
    #     self.label.setPixmap(self.images[trigger_class])
    # def clear_image(self):
    #     self.label.clear()
    
    # def run(self,trigger_class): #arc_board,
        
    #     time.sleep(4)
    #     self.show_image(trigger_class)
    #     #arc_board.BEEP_BOOP(trigger_class)
    #     time.sleep(4)
    #     self.clear_image()
        

    # def multiple_runs(self):
    #     trigger_list = [0] * 12 + [1] * 12
    #     random.shuffle(trigger_list)

    #     #arc_board = init_arc()
        
        
    #     #arc_board.prepare_session()
    #     self.show()
    #     self.show_cross()
        
    #     #arc_board.start_streaming()
    #     start_time = time.time()
    #     j = 1
    #     for i in trigger_list:
    #         print(j)
    #         self.run(i) #arc_board,
    #         j += 1
    #     end_time = time.time()
    #     #arc_board.stop_streaming()
        
        
    #     run_time = end_time - start_time
    #     print(run_time)
    #     #data, triggers = arc_board.record_window(run_time)
    #     #arc_board.release_session()
    
    # def threaded_run(self):
    #     t1 = threading.Thread(target=self.multiple_runs)
    #     t1.start()
    #     t1.join()

# class arc_board:
#     def __init__(self, board_shim, board_id):
#         self.board_shim = board_shim
#         self.eeg_channels = BoardShim.get_eeg_channels(board_id)
#         self.trigger_channel = BoardShim.get_other_channels(19)
#         self.sampling_rate = BoardShim.get_sampling_rate(board_id)
        
#     def prepare_session(self):
#         self.board_shim.prepare_session()
#     def start_streaming(self):
#         self.board_shim.start_stream()
#     def stop_streaming(self):
#         self.board_shim.stop_stream()
#     def release_session(self):
#         self.board_shim.release_session()
    
#     def record_window(self, window_size):
#         num_points = int(window_size * self.sampling_rate)
#         data = self.board_shim.get_board_data(num_points)
#         eeg_data = data[self.eeg_channels]
#         triggers = data[19]
#         return [eeg_data,triggers]
    
#     def BEEP_BOOP(self, trigger_class):
#         if trigger_class == 0:
#             self.board_shim.config_board(MindroveConfigMode.BEEP)
#         if trigger_class == 1:
#             self.board_shim.config_board(MindroveConfigMode.BOOP)

# def init_arc():
#     BoardShim.enable_dev_board_logger() # enable logger when developing to catch relevant logs 
#     params = MindRoveInputParams() 
#     board_id = BoardIds.MINDROVE_WIFI_BOARD
#     board_shim = BoardShim(board_id, params)
#     return arc_board(board_shim, board_id)


# def run(display,  trigger_class): #arc_board,

#     time.sleep(4)
#     display.show_image(trigger_class)
#     #arc_board.BEEP_BOOP(trigger_class)
#     time.sleep(4)
#     display.clear_image()

# def multiple_runs():
#     trigger_list = [0] * 12 + [1] * 12
#     random.shuffle(trigger_list)

#     #arc_board = init_arc()
#     app = QApplication(sys.argv)
#     display = TriggeredImageApp()
#     #arc_board.prepare_session()
    
#     y = threading.Thread(target=display.show())
#     x = threading.Thread(target=display.show_cross())
    
#     x.start()
    
#     y.start()
#     time.sleep(4)
#     #arc_board.start_streaming()
#     # start_time = time.time()
    
#     # for i in trigger_list:
#     #     run(display,i) #arc_board,
#     # end_time = time.time()
#     # #arc_board.stop_streaming()
#     # sys.exit(app.exec_())
    
#     # run_time = end_time - start_time
#     #data, triggers = arc_board.record_window(run_time)
#     #arc_board.release_session()

def trigger_signal_generator(communicator):
    trigger_list = [0] * 2 + [1] * 2
    random.shuffle(trigger_list)
    start_time = time.time()
    for trigger in trigger_list:
        print(time.time()-start_time)
        communicator.toggle_cross_signal.emit()
        time.sleep(2)
        communicator.toggle_cross_signal.emit()
        communicator.update_image_signal.emit(trigger)
        time.sleep(4)
        communicator.toggle_image_signal.emit()
        time.sleep(2)
    
    communicator.stop_signal.emit()
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    communicator = trigger_communicator()

    user_window = TriggeredImageApp(communicator)
    user_window.show()
    trigger_thread = threading.Thread(target=trigger_signal_generator, args=(communicator,))
    trigger_thread.start()

    sys.exit(app.exec())