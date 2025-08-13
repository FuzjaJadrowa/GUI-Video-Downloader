from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QRect, QTimer, QObject, Signal


class Popup(QWidget):
    def __init__(self, parent, text, color_hex):
        super().__init__(parent)
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.parent = parent
        self.text = text
        self.color = color_hex
        self.width_px = 420
        self.height_px = 56
        self.setup_ui()

    def setup_ui(self):
        self.label = QLabel(self.text, self)
        self.label.setStyleSheet(f"""
            background-color: {self.color};
            color: white;
            border-radius: 12px;
            padding-left: 16px;
            font-weight: 700;
        """)
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setFixedHeight(self.height_px)
        self.label.setFixedSize(self.width_px, self.height_px)

    def show_popup(self):
        parent_rect = self.parent.rect()
        x = (parent_rect.width() - self.width_px) // 2
        start = QRect(x, -self.height_px - 10, self.width_px, self.height_px)
        end = QRect(x, 12, self.width_px, self.height_px)
        self.setGeometry(start)
        self.label.setGeometry(0, 0, self.width_px, self.height_px)
        self.show()

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(380)
        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.start()

        QTimer.singleShot(5000, self.hide_popup)

    def hide_popup(self):
        parent_rect = self.parent.rect()
        x = (parent_rect.width() - self.width_px) // 2
        start = QRect(x, 12, self.width_px, self.height_px)
        end = QRect(x, -self.height_px - 10, self.width_px, self.height_px)
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(300)
        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.start()
        self.anim.finished.connect(self.deleteLater)


class PopupManager(QObject):
    _request_popup = Signal(str, str)  # message, color

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self._request_popup.connect(self._show_popup_main_thread)

    def _show_popup_main_thread(self, message, color):
        p = Popup(self.parent, message, color)
        p.show_popup()

    def show_error(self, message):
        self._request_popup.emit(f"✖ {message}", "#D32F2F")

    def show_success(self, message):
        self._request_popup.emit(f"✔ {message}", "#388E3C")

    def show_info(self, message):
        self._request_popup.emit(f"ℹ {message}", "#1976D2")