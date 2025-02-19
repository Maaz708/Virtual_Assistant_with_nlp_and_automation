import sys
import os
import logging
import threading
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer, QSize, pyqtSignal, QObject

# Initialize logging for debugging
logging.basicConfig(level=logging.INFO, filename="jarvis_ui_debug.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

class SizeAnimator(QObject):
    sizeChanged = pyqtSignal(QSize)

    def animate(self, size, delay=0):
        QTimer.singleShot(delay, lambda: self.sizeChanged.emit(size))

class JarvisUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.process = None
        self.is_listening = False

    def init_ui(self):
        self.setWindowTitle('Jarvis UI')
        self.setGeometry(80, 80, 400, 400)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Microphone image setup
        self.mic_label = QLabel(self)
        self.add_gif_to_label(self.mic_label, r"E:\J.A.R.V.I.S-main\J.A.R.V.I.S-main\Animation - 1739956129777.gif", size=(720, 220), alignment=Qt.AlignCenter)
        self.mic_label.setAlignment(Qt.AlignCenter)
        self.mic_label.mousePressEvent = self.start_listening

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.mic_label, alignment=Qt.AlignCenter)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)

        self.size_animator = SizeAnimator()
        self.size_animator.sizeChanged.connect(self.mic_label.setFixedSize)

    def add_gif_to_label(self, label, gif_path, size=None, alignment=None):
        try:
            if not os.path.exists(gif_path):
                logging.error(f"GIF path does not exist: {gif_path}")
                return
            movie = QMovie(gif_path)
            label.setMovie(movie)
            movie.start()

            if size:
                label.setFixedSize(*size)

            if alignment:
                label.setAlignment(alignment)

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            label.setGraphicsEffect(shadow)
        except Exception as e:
            logging.exception("Error loading GIF:")

    def start_listening(self, event):
        if not self.is_listening:
            self.is_listening = True
            logging.info("Starting subprocess for main function...")
            threading.Thread(target=self.run_main_file, daemon=True).start()

    def run_main_file(self):
        try:
            path_to_main_py = r"E:\J.A.R.V.I.S-main\J.A.R.V.I.S-main\jarvis.py"
            if not os.path.exists(path_to_main_py):
                logging.error(f"Path to main.py does not exist: {path_to_main_py}")
                self.is_listening = False
                return

            command = ["python", path_to_main_py]
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            for line in iter(self.process.stdout.readline, ''):
                logging.info(f"Output from jarvis.py: {line.strip()}")
                self.handle_output(line.strip())

            for line in iter(self.process.stderr.readline, ''):
                logging.error(f"Error from jarvis.py: {line.strip()}")

            self.process.stdout.close()
            self.process.stderr.close()
            self.process.wait()
        except Exception as e:
            logging.exception("Error running main file:")
        finally:
            self.is_listening = False
            logging.info("Subprocess finished")

    def handle_output(self, output):
        if output:
            self.size_animator.animate(QSize(900, 280))
            self.size_animator.animate(QSize(720, 220), delay=500)
        else:
            self.size_animator.animate(QSize(720, 220))

def start_ui():
    app = QApplication(sys.argv)
    jarvis_ui = JarvisUI()
    jarvis_ui.showFullScreen()
    return app, jarvis_ui

if __name__ == "__main__":
    app, _ = start_ui()
    sys.exit(app.exec_())
