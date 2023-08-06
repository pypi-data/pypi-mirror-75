import sys
sys.path.append("..") # When launching from source, include StudiOCR folder
import signal
from multiprocessing import Queue, Pipe

from PySide2 import QtCore as Qc
from PySide2 import QtWidgets as Qw
from PySide2 import QtGui as Qg
import qdarkstyle

import StudiOCR.wsl as wsl
from StudiOCR.db import create_tables, db
from StudiOCR.MainWindow import MainWindow
from StudiOCR.OcrWorker import StatusEmitter, OcrWorker

# References
# https://doc.qt.io/qtforpython/

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    # If the database has not been created, then create it
    create_tables()

    # Set DISPLAY env variable accordingly if running under WSL
    wsl.set_display_to_host()

    app = Qw.QApplication(sys.argv)  # Create application

    # Create a pipe and queue for inter-process communication
    main_pipe, child_pipe = Pipe()
    queue = Queue()

    ocr_process = OcrWorker(child_pipe, queue)
    status_emitter = StatusEmitter(main_pipe, app)
    status_emitter.daemon = True
    status_emitter.start()

    def quit_processes():
        # stop thread
        status_emitter.stop()
        # stop process
        queue.put(None)
        ocr_process.join()
        db.close()
        
    window = MainWindow(queue, status_emitter)  # Create main window

    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside2'))

    window.show()  # Show main window

    ocr_process.start()  # Start child process

    app.aboutToQuit.connect(quit_processes)
        
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
