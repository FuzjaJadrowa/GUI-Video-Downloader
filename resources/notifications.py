from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QRect

class Notification(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(40)
        self.setStyleSheet("border-radius: 6px; font-weight: bold;")
        self.hide()
        self.timer = QTimer()
        self.timer.timeout.connect(self.hide_notification)

    def show_message(self, text, type_):
        colors = {
            "error": "#ff4c4c",
            "success": "#28a745",
            "info": "#1e90ff"
        }
        self.setText(text)
        self.setStyleSheet(f"background-color: {colors[type_]}; color: white; border-radius: 6px; font-weight: bold;")

        self.setGeometry(QRect(0, -40, self.parent().width(), 40))
        self.show()

        anim = QPropertyAnimation(self, b"geometry")
        anim.setDuration(300)
        anim.setStartValue(QRect(0, -40, self.parent().width(), 40))
        anim.setEndValue(QRect(0, 0, self.parent().width(), 40))
        anim.start()
        self.anim = anim

        self.timer.start(5000)

    def hide_notification(self):
        anim = QPropertyAnimation(self, b"geometry")
        anim.setDuration(300)
        anim.setStartValue(QRect(0, 0, self.parent().width(), 40))
        anim.setEndValue(QRect(0, -40, self.parent().width(), 40))
        anim.start()
        self.anim = anim
        self.timer.stop()
