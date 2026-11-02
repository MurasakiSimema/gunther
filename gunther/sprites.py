import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from gunther.utils import get_resource_path

class SpriteManager:
    """Manages sprite loading, caching, scaling and palette swapping."""

    def __init__(self, palette="gunther", scale=1.0):
        self.palette = palette
        self.scale = scale
        self.cache = {}
        self.load_sprites()

    def set_palette(self, palette: str):
        if self.palette != palette:
            self.palette = palette
            self.cache.clear()
            self.load_sprites()

    def set_scale(self, scale: float):
        if abs(self.scale - scale) > 0.01:
            self.scale = scale
            self.cache.clear()
            self.load_sprites()

    def find_palette_path(self, palette: str) -> str:
        """Finds the directory for a palette, checking both direct path and category subfolders."""
        # 1. Direct path check (e.g. 'criceto/gunther' or 'gunther')
        direct = get_resource_path(os.path.join("assets", "sprites", palette))
        if os.path.isdir(direct):
            return direct

        # 2. Check within all category subfolders (e.g. assets/sprites/criceto/gunther)
        base_dir = get_resource_path(os.path.join("assets", "sprites"))
        if os.path.exists(base_dir):
            for sub in sorted(os.listdir(base_dir)):
                sub_path = os.path.join(base_dir, sub)
                if os.path.isdir(sub_path):
                    candidate = os.path.join(sub_path, palette)
                    if os.path.isdir(candidate):
                        return candidate

        return direct

    def load_sprites(self):
        pal_path = self.find_palette_path(self.palette)
        if not os.path.exists(pal_path):
            print(f"Warning: palette folder {pal_path} not found!")
            return

        animations = ["idle", "walk_left", "walk_right", "eat", "sleep", "drag", "pet"]
        for anim in animations:
            self.cache[anim] = []
            for i in range(4):
                file_name = f"{anim}_{i}.png"
                file_path = os.path.join(pal_path, file_name)
                if os.path.exists(file_path):
                    pixmap = QPixmap(file_path)
                    if abs(self.scale - 1.0) > 0.01:
                        target_w = int(pixmap.width() * self.scale)
                        target_h = int(pixmap.height() * self.scale)
                        pixmap = pixmap.scaled(
                            target_w, target_h,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.FastTransformation
                        )
                    self.cache[anim].append(pixmap)
                else:
                    print(f"Sprite not found: {file_path}")

    def get_categorized_palettes(self) -> dict[str, list[str]]:
        """Returns all available palettes grouped by their category subfolder."""
        base_dir = get_resource_path(os.path.join("assets", "sprites"))
        if not os.path.exists(base_dir):
            return {"default": [self.palette]}

        categories = {}
        for entry in sorted(os.listdir(base_dir)):
            entry_path = os.path.join(base_dir, entry)
            if not os.path.isdir(entry_path):
                continue

            has_pngs = any(f.endswith(".png") for f in os.listdir(entry_path) if os.path.isfile(os.path.join(entry_path, f)))
            if has_pngs:
                categories.setdefault("default", []).append(entry)
            else:
                sub_pals = [
                    d for d in sorted(os.listdir(entry_path))
                    if os.path.isdir(os.path.join(entry_path, d))
                ]
                if sub_pals:
                    categories[entry] = sub_pals

        return categories if categories else {"default": [self.palette]}

    def get_available_palettes(self) -> list[str]:
        categorized = self.get_categorized_palettes()
        all_pals = []
        for cat, pals in categorized.items():
            all_pals.extend(pals)
        return all_pals if all_pals else [self.palette]

    def get_frame(self, anim: str, index: int) -> QPixmap:
        frames = self.cache.get(anim, [])
        if not frames:
            return QPixmap()
        return frames[index % len(frames)]

    def frame_count(self, anim: str) -> int:
        return len(self.cache.get(anim, []))

    def get_size(self) -> tuple[int, int]:
        idle_frames = self.cache.get("idle", [])
        if idle_frames and not idle_frames[0].isNull():
            return (idle_frames[0].width(), idle_frames[0].height())
        return (int(108 * self.scale), int(108 * self.scale))
