import random
import math
from PyQt6.QtGui import QPainter, QColor, QPainterPath
from PyQt6.QtCore import Qt

class HeartParticle:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.base_x = x
        self.vy = random.uniform(1.2, 2.2)
        self.sway_speed = random.uniform(2.0, 4.0)
        self.sway_amp = random.uniform(3.0, 7.0)
        self.time = random.uniform(0, 3.14)
        self.size = random.uniform(10.0, 16.0)
        self.alpha = 255
        self.fade_speed = random.uniform(3.5, 5.5)
        self.alive = True
        colors = [
            QColor(255, 90, 130),
            QColor(255, 120, 160),
            QColor(255, 150, 185),
            QColor(255, 70, 110)
        ]
        self.color = random.choice(colors)

    def update(self):
        self.y -= self.vy
        self.time += 0.05
        self.x = self.base_x + math.sin(self.time * self.sway_speed) * self.sway_amp
        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            self.alive = False

    def draw(self, painter: QPainter):
        if not self.alive or self.alpha <= 0:
            return

        c = QColor(self.color)
        c.setAlpha(int(max(0, min(255, self.alpha))))
        painter.setBrush(c)
        painter.setPen(Qt.PenStyle.NoPen)

        # Draw cute heart shape with QPainterPath
        s = self.size
        hx = self.x - s / 2
        hy = self.y - s / 2

        path = QPainterPath()
        path.moveTo(hx + s * 0.5, hy + s * 0.8)
        # Left curve
        path.cubicTo(
            hx, hy + s * 0.45,
            hx, hy,
            hx + s * 0.3, hy
        )
        path.cubicTo(
            hx + s * 0.5, hy,
            hx + s * 0.5, hy + s * 0.2,
            hx + s * 0.5, hy + s * 0.2
        )
        # Right curve
        path.cubicTo(
            hx + s * 0.5, hy + s * 0.2,
            hx + s * 0.5, hy,
            hx + s * 0.7, hy
        )
        path.cubicTo(
            hx + s, hy,
            hx + s, hy + s * 0.45,
            hx + s * 0.5, hy + s * 0.8
        )

        painter.drawPath(path)


class ParticleManager:
    def __init__(self):
        self.particles: list[HeartParticle] = []

    def spawn_hearts(self, x: float, y: float, count: int = 4):
        for _ in range(count):
            ox = x + random.uniform(-15, 15)
            oy = y + random.uniform(-5, 5)
            self.particles.append(HeartParticle(ox, oy))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, painter: QPainter):
        for p in self.particles:
            p.draw(painter)
