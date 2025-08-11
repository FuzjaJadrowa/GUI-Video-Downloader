from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QIcon
from launcher import Launcher

app = QApplication([])

QFontDatabase.addApplicationFont("fonts/Montserrat-Bold.ttf")
QFontDatabase.addApplicationFont("fonts/Montserrat-ExtraBold.ttf")

app.setWindowIcon(QIcon("icon.ico"))

app.setStyleSheet("""
    QLabel, QPushButton {
        font-family: 'Montserrat';
        font-weight: bold;
        color: white;
    }
    QLabel.title {
        font-weight: 800;
        font-size: 24px;
    }
    QLabel.subtitle {
        font-weight: bold;
        font-size: 16px;
    }
    QPushButton {
        background-color: #333;
        border: none;
        padding: 6px 14px;
        border-radius: 6px;
    }
    QPushButton:hover {
        background-color: #555;
    }
    QProgressBar {
        border: 1px solid #444;
        border-radius: 6px;
        background-color: #222;
        text-align: center;
        color: white;
    }
    QProgressBar::chunk {
        background-color: #00bfff;
        border-radius: 6px;
    }
""")

window = Launcher()
window.show()

app.exec()
