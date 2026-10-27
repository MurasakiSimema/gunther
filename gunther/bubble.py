from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath

class ThoughtBubble(QWidget):
    """
    A charming thought/speech bubble for Gunther that floats gently
    above his head and displays sweet messages.
    """
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(400)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.dismiss_timer = QTimer(self)
        self.dismiss_timer.setSingleShot(True)
        self.dismiss_timer.timeout.connect(self.fade_out)

        self.message = ""
        self.setFixedWidth(220)
        self.setMinimumHeight(60)

    def show_thought(self, text: str, hamster_center_x: int, hamster_top_y: int, duration_ms: int = 7000):
        self.message = text
        self.adjust_size_and_position(hamster_center_x, hamster_top_y)

        self.show()
        self.anim.stop()
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()

        self.dismiss_timer.stop()
        self.dismiss_timer.start(duration_ms)

    def adjust_size_and_position(self, hamster_center_x: int, hamster_top_y: int):
        # Calculate needed height based on text length
        # Approximate 25 characters per line
        lines = max(1, len(self.message) // 22 + 1)
        bubble_h = max(64, lines * 20 + 34)
        self.setFixedHeight(bubble_h)

        # Center above hamster
        w = self.width()
        pos_x = hamster_center_x - (w // 2)
        pos_y = hamster_top_y - bubble_h - 10

        # Keep on screen bounds if possible
        if pos_y < 10:
            pos_y = hamster_top_y + 100  # Flip below if at top edge

        self.move(pos_x, pos_y)
        self.update()

    def update_position(self, hamster_center_x: int, hamster_top_y: int):
        if self.isVisible():
            w = self.width()
            pos_x = hamster_center_x - (w // 2)
            pos_y = hamster_top_y - self.height() - 10
            self.move(pos_x, pos_y)

    def fade_out(self):
        self.anim.stop()
        self.anim.setStartValue(self.opacity_effect.opacity())
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self._on_fade_finished)
        self.anim.start()

    def _on_fade_finished(self):
        try:
            self.anim.finished.disconnect(self._on_fade_finished)
        except Exception:
            pass
        self.hide()
        self.closed.emit()

    def mousePressEvent(self, event):
        # Dismiss when clicked
        self.fade_out()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        tail_h = 10

        # Draw thought bubble background
        path = QPainterPath()
        rect_h = h - tail_h
        path.addRoundedRect(4, 4, w - 8, rect_h - 4, 14, 14)

        # Bubble fill & border
        painter.setBrush(QBrush(QColor(255, 253, 247, 245)))
        painter.setPen(QPen(QColor(215, 195, 175, 220), 1.5))
        painter.drawPath(path)

        # Little thought cloud bubbles pointing down
        cx = w // 2
        painter.setBrush(QBrush(QColor(255, 253, 247, 245)))
        painter.setPen(QPen(QColor(215, 195, 175, 220), 1.2))
        painter.drawEllipse(cx - 3, h - tail_h - 2, 7, 7)
        painter.drawEllipse(cx - 1, h - 5, 4, 4)

        # Text
        painter.setPen(QColor(60, 48, 42))
        font = QFont("Segoe UI", 9)
        font.setBold(True)
        painter.setFont(font)

        text_rect = self.rect().adjusted(14, 8, -14, -tail_h - 4)
        painter.drawText(
            text_rect,
            Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap,
            self.message
        )
