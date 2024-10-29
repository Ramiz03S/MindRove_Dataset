from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds, MindroveConfigMode
import sys
import time
import random
import threading
import os
import numpy as np
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtMultimedia import QSoundEffect

class trigger_communicator(QObject):
    update_image_signal = Signal(int)
    stop_signal = Signal()
    sound_signal = Signal()

class User_Interface(QWidget):
    def __init__(self, communicator):
        super().__init__()
        
        self.setWindowTitle('MindRove Dataset')
        self.setGeometry(400,400,1000,1000)
        self.setStyleSheet("background-color: white;")
        
        self.label = QLabel(parent=self)
        self.sound_effect = QSoundEffect()
        
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.label, alignment=Qt.AlignCenter)
        self.setLayout(hlayout)
        
        self.images = [QPixmap('tongue.png'),QPixmap('feet.png'),QPixmap('cross.png'),QPixmap('empty.png')]
        self.sound_effect.setSource("file:./ding.wav")
        
        communicator.sound_signal.connect(self.play_sound)
        communicator.update_image_signal.connect(self.update_image)
        communicator.stop_signal.connect(self.close_window)

    def update_image(self, trigger_class):
        self.label.setPixmap(self.images[trigger_class].scaled(400,400))

    def close_window(self):
        self.label.setText("RUN ENDED")
        self.close()

    def play_sound(self):
        self.sound_effect.play()

class arc_board:
    def __init__(self, board_shim, board_id):
        self.board_shim = board_shim
        self.eeg_channels = BoardShim.get_eeg_channels(board_id)
        self.eeg_channels.append(19)
        #self.trigger_channel = [19]
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
        
        return eeg_data
    
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

def trigger_signal_generator(communicator,subject_number,run_number):
    os.makedirs(f'subject_recordings//S_{subject_number:02d}//tongue_feet', exist_ok=True)
    arc = init_arc()
    
    trigger_list = [0] * 12 + [1] * 12
    random.shuffle(trigger_list)
    
    arc.prepare_session()
    initial_time = time.time()
    arc.start_streaming()
    
    for trigger in trigger_list:
        communicator.update_image_signal.emit(2) #cross
        communicator.sound_signal.emit()
        time.sleep(3)
        
        communicator.update_image_signal.emit(trigger)
        arc.BEEP_BOOP(trigger)
        time.sleep(5)
        
        communicator.update_image_signal.emit(3)
        time.sleep(2)
    
    run_time = time.time() - initial_time
    
    eeg_data = (arc.record_window(run_time+100)).T
    np.savetxt(f'subject_recordings//S_{subject_number:02d}//tongue_feet//run_{run_number}.csv',eeg_data,delimiter=',')
    
    communicator.stop_signal.emit()
    arc.stop_streaming()
    arc.release_session()
    
if __name__ == "__main__":
    
    
    subject_number = 
    run_number = 
    
    
    app = QApplication(sys.argv)
    communicator = trigger_communicator()
    user_window = User_Interface(communicator)
    
    user_window.showMaximized()
    trigger_thread = threading.Thread(target=trigger_signal_generator, args=(communicator,subject_number,run_number,))
    trigger_thread.start()
    
    sys.exit(app.exec())
    
    trigger_thread.join()
