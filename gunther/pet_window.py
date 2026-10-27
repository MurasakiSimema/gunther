import os
import random
from PyQt6.QtWidgets import QWidget, QMenu, QApplication
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPainter, QAction, QCursor

from gunther.config import load_config, save_config
from gunther.sprites import SpriteManager
from gunther.behavior import HamsterBehavior, State
from gunther.bubble import ThoughtBubble
from gunther.hearts import ParticleManager
from gunther.messages import MESSAGES

class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.config = load_config()
        self.sprite_manager = SpriteManager(
            palette=self.config.get("palette", "gunther"),
            scale=self.config.get("scale", 1.0)
        )
        self.behavior = HamsterBehavior()
        self.particles = ParticleManager()
        self.bubble = ThoughtBubble()

        # Window setup
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Drag tracking
        self.is_dragging = False
        self.drag_start_pos = QPoint()
        self.drag_offset = QPoint()

        # Animation frame counter
        self.anim_tick = 0
        self.current_frame_idx = 0

        # Load thoughts directly from embedded memory
        self.messages = list(MESSAGES)

        # Setup size
        self.update_window_size()

        # Initial position: bottom right above taskbar
        self.move_to_initial_floor()

        # Main 30 FPS update timer (~33ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_tick)
        self.timer.start(33)

        # Thought bubble timer (every 2-4 minutes)
        self.thought_timer = QTimer(self)
        self.thought_timer.timeout.connect(self.trigger_random_thought)
        interval = self.config.get("thought_interval_sec", 180)
        self.thought_timer.start(interval * 1000)

        # First greeting thought after 3 seconds!
        QTimer.singleShot(3000, lambda: self.show_thought("Ciao! Sono Gunther! 🐹❤️"))

    def update_window_size(self):
        sw, sh = self.sprite_manager.get_size()
        self.window_w = sw + 24
        self.window_h = sh + 40
        self.resize(self.window_w, self.window_h)

    def get_floor_y(self) -> int:
        screen = QApplication.primaryScreen().availableGeometry()
        return screen.bottom() - self.window_h + 10  # Hamster feet resting snugly on taskbar

    def get_screen_bounds(self) -> tuple[int, int]:
        screen = QApplication.primaryScreen().availableGeometry()
        return screen.left(), screen.right() - self.window_w

    def move_to_initial_floor(self):
        screen = QApplication.primaryScreen().availableGeometry()
        initial_x = screen.right() - self.window_w - 180
        initial_y = self.get_floor_y()
        self.move(initial_x, initial_y)

    def game_tick(self):
        self.anim_tick += 1

        # 1. Physics & Behavior
        min_x, max_x = self.get_screen_bounds()
        can_roam = self.config.get("roam_enabled", True)
        dx, dy, changed = self.behavior.update_tick(self.x(), min_x, max_x, can_roam=can_roam)

        if not self.is_dragging:
            cur_x = self.x() + dx
            cur_y = self.y() + dy

            # Gravity / Floor check
            floor_y = self.get_floor_y()
            if self.behavior.state == State.FALLING:
                if cur_y >= floor_y:
                    cur_y = floor_y
                    self.behavior.set_state(State.IDLE)
                    self.behavior.vy = 0
            elif self.behavior.state in (State.IDLE, State.WALK_LEFT, State.WALK_RIGHT, State.EAT, State.SLEEP, State.PETTED):
                if self.config.get("gravity_enabled", True) and cur_y < floor_y - 20:
                    self.behavior.set_state(State.FALLING)
                elif cur_y > floor_y:
                    cur_y = floor_y

            self.move(cur_x, cur_y)

        # 2. Advance Sprite Animation Frame
        anim_name = self.behavior.state.value
        if self.behavior.state == State.FALLING:
            anim_name = "drag"

        divider = 6
        if self.behavior.state == State.EAT:
            divider = 4
        elif self.behavior.state in (State.SLEEP, State.IDLE):
            divider = 12

        total_frames = self.sprite_manager.frame_count(anim_name)
        if total_frames > 0:
            self.current_frame_idx = (self.anim_tick // divider) % total_frames

        # 3. Update Particles
        self.particles.update()

        # 4. Update Thought Bubble Position
        if self.bubble.isVisible():
            hamster_center_x = self.x() + self.width() // 2
            hamster_top_y = self.y() + 35
            self.bubble.update_position(hamster_center_x, hamster_top_y)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw Hamster Sprite at bottom center
        anim_name = self.behavior.state.value
        if self.behavior.state == State.FALLING:
            anim_name = "drag"

        frame = self.sprite_manager.get_frame(anim_name, self.current_frame_idx)
        if not frame.isNull():
            sw, sh = frame.width(), frame.height()
            draw_x = (self.width() - sw) // 2
            draw_y = self.height() - sh
            painter.drawPixmap(draw_x, draw_y, frame)

        # Draw floating hearts over hamster
        self.particles.draw(painter)

    # ---------------- Mouse Events ----------------

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.globalPosition().toPoint()
            self.drag_offset = event.pos()
            self.is_dragging = False

        elif event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            diff = (event.globalPosition().toPoint() - self.drag_start_pos).manhattanLength()
            if diff > 6 or self.is_dragging:
                self.is_dragging = True
                self.behavior.set_state(State.DRAGGED)
                new_pos = event.globalPosition().toPoint() - self.drag_offset
                self.move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_dragging:
                self.is_dragging = False
                floor_y = self.get_floor_y()
                if self.config.get("gravity_enabled", True) and self.y() < floor_y - 20:
                    self.behavior.set_state(State.FALLING)
                    self.behavior.vy = 1.0
                else:
                    self.behavior.set_state(State.IDLE)
            else:
                self.pet_hamster()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.feed_hamster()

    def pet_hamster(self):
        self.behavior.set_state(State.PETTED, duration_ticks=80)
        cx = self.width() // 2
        cy = self.height() - self.sprite_manager.get_size()[1] + 10
        self.particles.spawn_hearts(cx, cy, count=5)

    def feed_hamster(self):
        self.behavior.set_state(State.EAT, duration_ticks=220)
        cx = self.width() // 2
        cy = self.height() - self.sprite_manager.get_size()[1] + 15
        self.particles.spawn_hearts(cx, cy, count=2)

    def toggle_sleep(self):
        if self.behavior.state == State.SLEEP:
            self.behavior.set_state(State.IDLE)
            self.pet_hamster()
        else:
            self.behavior.set_state(State.SLEEP, duration_ticks=3600)

    def trigger_random_thought(self):
        if not self.config.get("enable_thoughts", True):
            return
        if self.behavior.state in (State.SLEEP, State.DRAGGED):
            return
        if self.messages:
            msg = random.choice(self.messages)
            self.show_thought(msg)

    def show_thought(self, text: str):
        hamster_center_x = self.x() + self.width() // 2
        hamster_top_y = self.y() + 35
        self.bubble.show_thought(text, hamster_center_x, hamster_top_y)

    # ---------------- Context Menu ----------------

    def show_context_menu(self, global_pos: QPoint):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #FFFDF8;
                border: 1px solid #D6C7B8;
                border-radius: 8px;
                padding: 6px;
                font-family: 'Segoe UI';
                font-size: 10pt;
                color: #382C24;
            }
            QMenu::item {
                padding: 6px 24px 6px 12px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #F8E2CD;
                color: #261B14;
            }
            QMenu::separator {
                height: 1px;
                background-color: #EBDCCD;
                margin: 4px 6px;
            }
        """)

        feed_act = menu.addAction("🌻 Dai un semino a Gunther")
        feed_act.triggered.connect(self.feed_hamster)

        pet_act = menu.addAction("🐾 Fai una coccola")
        pet_act.triggered.connect(self.pet_hamster)

        is_sleeping = (self.behavior.state == State.SLEEP)
        sleep_text = "☀️ Sveglia Gunther" if is_sleeping else "💤 Fai fare un pisolino"
        sleep_act = menu.addAction(sleep_text)
        sleep_act.triggered.connect(self.toggle_sleep)

        thought_act = menu.addAction("💬 Cosa stai pensando?")
        thought_act.triggered.connect(self.trigger_random_thought)

        menu.addSeparator()

        available_pals = self.sprite_manager.get_available_palettes()
        if len(available_pals) > 1:
            pal_menu = menu.addMenu("🎨 Manto di Gunther")
            pal_names = {
                "gunther": "Gunther (Grigio Scuro Originale) 🐹",
                "dorato": "Dorato Classico (Siriano)",
                "invernale": "Bianco Invernale (Snow)",
                "zaffiro": "Grigio Zaffiro (Russo)",
                "panda": "Panda Pezzato"
            }
            cur_pal = self.config.get("palette", "gunther")
            for key in ["gunther", "dorato", "invernale", "zaffiro", "panda"]:
                if key in available_pals:
                    name = pal_names.get(key, key.capitalize())
                    act = pal_menu.addAction(name)
                    act.setCheckable(True)
                    act.setChecked(key == cur_pal)
                    act.triggered.connect(lambda chk, k=key: self.set_palette(k))

        size_menu = menu.addMenu("📏 Dimensione")
        sizes = [
            (0.75, "Piccolo (75%)"),
            (1.0, "Normale (100%)"),
            (1.25, "Grande (125%)"),
            (1.5, "Gigante (150%)")
        ]
        cur_scale = self.config.get("scale", 1.0)
        for scale_val, label in sizes:
            act = size_menu.addAction(label)
            act.setCheckable(True)
            act.setChecked(abs(cur_scale - scale_val) < 0.05)
            act.triggered.connect(lambda chk, s=scale_val: self.set_scale(s))

        roam_act = menu.addAction("🚶 Cammina liberamente")
        roam_act.setCheckable(True)
        roam_act.setChecked(self.config.get("roam_enabled", True))
        roam_act.triggered.connect(self.toggle_roam)

        thoughts_act = menu.addAction("💭 Mostra pensieri dolci")
        thoughts_act.setCheckable(True)
        thoughts_act.setChecked(self.config.get("enable_thoughts", True))
        thoughts_act.triggered.connect(self.toggle_thoughts)

        menu.addSeparator()

        exit_act = menu.addAction("👋 Saluta Gunther (Esci)")
        exit_act.triggered.connect(QApplication.instance().quit)

        menu.exec(global_pos)

    def set_palette(self, pal_key: str):
        self.config["palette"] = pal_key
        save_config(self.config)
        self.sprite_manager.set_palette(pal_key)
        self.update_window_size()

    def set_scale(self, scale_val: float):
        self.config["scale"] = scale_val
        save_config(self.config)
        self.sprite_manager.set_scale(scale_val)
        self.update_window_size()

    def toggle_roam(self, enabled: bool):
        self.config["roam_enabled"] = enabled
        save_config(self.config)
        if not enabled:
            self.behavior.set_state(State.IDLE)

    def toggle_thoughts(self, enabled: bool):
        self.config["enable_thoughts"] = enabled
        save_config(self.config)
        if not enabled and self.bubble.isVisible():
            self.bubble.fade_out()
