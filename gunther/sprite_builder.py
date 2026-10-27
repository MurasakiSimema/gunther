"""
Sprite generator for Gunther the Hamster companion.
Generates adorable pixel art sprites for various animations and color palettes.
"""

from PIL import Image, ImageDraw
import os

PALETTES = {
    "gunther": {
        "name": "Gunther (Grigio Scuro)",
        "fur_main": (105, 105, 114, 255),
        "fur_shadow": (72, 72, 82, 255),
        "fur_light": (138, 138, 148, 255),
        "belly": (255, 255, 255, 255),
        "belly_shadow": (222, 226, 234, 255),
        "inner_ear": (255, 175, 190, 255),
        "nose": (245, 140, 160, 255),
        "paws": (255, 195, 205, 255),
        "blush": (255, 135, 160, 150),
        "eyes": (20, 18, 22, 255),
        "outline": (48, 48, 56, 220),
        "whiskers": False,
    },
    "dorato": {
        "name": "Dorato Classico (Siriano)",
        "fur_main": (230, 166, 93, 255),
        "fur_shadow": (185, 120, 55, 255),
        "fur_light": (248, 198, 138, 255),
        "belly": (255, 248, 238, 255),
        "belly_shadow": (232, 222, 205, 255),
        "inner_ear": (255, 175, 190, 255),
        "nose": (245, 140, 160, 255),
        "paws": (255, 195, 205, 255),
        "blush": (255, 140, 160, 160),
        "eyes": (30, 25, 30, 255),
        "outline": (90, 50, 25, 220),
        "whiskers": True,
    },
    "invernale": {
        "name": "Bianco Invernale (Winter White)",
        "fur_main": (245, 247, 250, 255),
        "fur_shadow": (205, 212, 224, 255),
        "fur_light": (255, 255, 255, 255),
        "belly": (255, 255, 255, 255),
        "belly_shadow": (225, 230, 238, 255),
        "inner_ear": (255, 185, 195, 255),
        "nose": (245, 150, 165, 255),
        "paws": (255, 200, 210, 255),
        "blush": (255, 150, 170, 150),
        "eyes": (35, 30, 40, 255),
        "outline": (130, 138, 155, 220),
        "whiskers": True,
    },
    "zaffiro": {
        "name": "Grigio Zaffiro (Russo)",
        "fur_main": (155, 164, 178, 255),
        "fur_shadow": (112, 122, 138, 255),
        "fur_light": (188, 196, 208, 255),
        "belly": (245, 248, 252, 255),
        "belly_shadow": (210, 216, 225, 255),
        "inner_ear": (245, 170, 185, 255),
        "nose": (240, 135, 155, 255),
        "paws": (250, 190, 200, 255),
        "blush": (255, 135, 160, 160),
        "eyes": (25, 28, 35, 255),
        "outline": (68, 75, 88, 220),
        "whiskers": True,
    },
    "panda": {
        "name": "Panda Pezzato",
        "fur_main": (65, 52, 45, 255),
        "fur_shadow": (40, 30, 25, 255),
        "fur_light": (95, 80, 70, 255),
        "belly": (252, 250, 245, 255),
        "belly_shadow": (220, 216, 210, 255),
        "inner_ear": (250, 170, 185, 255),
        "nose": (240, 135, 155, 255),
        "paws": (250, 190, 200, 255),
        "blush": (255, 140, 160, 160),
        "eyes": (20, 15, 15, 255),
        "outline": (30, 22, 18, 220),
        "whiskers": True,
    }
}

SEED_SHELL = (60, 50, 45, 255)
SEED_STRIPE = (210, 205, 195, 255)
SHADOW_COLOR = (0, 0, 0, 45)


def create_canvas(w=36, h=36):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def draw_pixel_rect(draw, x1, y1, x2, y2, color):
    draw.rectangle([x1, y1, x2, y2], fill=color)


def draw_drop_shadow(draw, cx, cy, rx, ry):
    """Draws a soft ground shadow underneath the hamster"""
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            if dx*dx + dy*dy <= 1.0:
                draw.point((x, y), fill=SHADOW_COLOR)


def render_idle_frame(palette, step=0):
    """
    Renders an idle frame (breathing, sniffing, blinking)
    step: 0=normal, 1=breathe up, 2=sniff/look up slightly, 3=blink
    """
    img = create_canvas(36, 36)
    draw = ImageDraw.Draw(img)
    p = palette

    # Shadow
    draw_drop_shadow(draw, 18, 33, 11, 2)

    # Bob offset
    dy = -1 if step == 1 else 0
    sniff = (step == 2)
    blink = (step == 3)

    # Feet
    draw.rectangle([10, 31, 14, 33], fill=p["paws"])
    draw.rectangle([21, 31, 25, 33], fill=p["paws"])

    # Body base (chubby round fluff)
    # Main body ellipse
    draw.ellipse([8, 14 + dy, 27, 32 + dy], fill=p["fur_main"], outline=p["outline"])
    # Chubby cheeks bulge
    draw.ellipse([6, 17 + dy, 18, 30 + dy], fill=p["fur_main"], outline=None)
    draw.ellipse([17, 17 + dy, 29, 30 + dy], fill=p["fur_main"], outline=None)
    # Outline touchups
    draw.line([(6, 21 + dy), (6, 27 + dy)], fill=p["outline"])
    draw.line([(29, 21 + dy), (29, 27 + dy)], fill=p["outline"])

    # White belly patch
    draw.ellipse([11, 19 + dy, 24, 31 + dy], fill=p["belly"])
    draw.ellipse([12, 28 + dy, 23, 31 + dy], fill=p["belly_shadow"])

    # Ears
    ear_y = 11 + dy - (1 if sniff else 0)
    # Left ear
    draw.ellipse([8, ear_y, 14, ear_y + 7], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([10, ear_y + 2, 13, ear_y + 5], fill=p["inner_ear"])
    # Right ear
    draw.ellipse([21, ear_y, 27, ear_y + 7], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([22, ear_y + 2, 25, ear_y + 5], fill=p["inner_ear"])

    # Forehead highlight
    draw.rectangle([16, 14 + dy, 19, 17 + dy], fill=p["fur_light"])

    # Face elements
    face_y = 19 + dy - (1 if sniff else 0)

    # Eyes
    if blink:
        # Happy sleepy eyes (^ ^)
        draw.line([(11, face_y + 1), (13, face_y)], fill=p["eyes"], width=1)
        draw.line([(13, face_y), (15, face_y + 1)], fill=p["eyes"], width=1)
        draw.line([(20, face_y + 1), (22, face_y)], fill=p["eyes"], width=1)
        draw.line([(22, face_y), (24, face_y + 1)], fill=p["eyes"], width=1)
    else:
        # Glossy black button eyes with white sparkles
        draw.ellipse([11, face_y, 15, face_y + 4], fill=p["eyes"])
        draw.point((12, face_y + 1), fill=(255, 255, 255, 255))
        draw.ellipse([20, face_y, 24, face_y + 4], fill=p["eyes"])
        draw.point((21, face_y + 1), fill=(255, 255, 255, 255))

    # Cheeks blush
    draw.ellipse([8, face_y + 3, 11, face_y + 6], fill=p["blush"])
    draw.ellipse([24, face_y + 3, 27, face_y + 6], fill=p["blush"])

    # Nose & Mouth
    nose_y = face_y + 3 + (0 if not sniff else -1)
    draw.point((17, nose_y), fill=p["nose"])
    draw.point((18, nose_y), fill=p["nose"])
    draw.point((17, nose_y + 1), fill=p["outline"])
    draw.point((18, nose_y + 1), fill=p["outline"])

    # Cute tiny paws in front
    paw_y = 26 + dy
    draw.ellipse([12, paw_y, 15, paw_y + 3], fill=p["paws"])
    draw.ellipse([20, paw_y, 23, paw_y + 3], fill=p["paws"])

    # Whiskers
    if p.get("whiskers", True):
        whisker_color = (255, 255, 255, 180)
        draw.line([(6, nose_y), (10, nose_y)], fill=whisker_color)
        draw.line([(6, nose_y + 2), (10, nose_y + 1)], fill=whisker_color)
        draw.line([(25, nose_y), (29, nose_y)], fill=whisker_color)
        draw.line([(25, nose_y + 1), (29, nose_y + 2)], fill=whisker_color)

    return img


def render_walk_frame(palette, step=0):
    """
    Walking sideways / profile-3/4 view (facing right).
    step 0 to 3
    """
    img = create_canvas(36, 36)
    draw = ImageDraw.Draw(img)
    p = palette

    # Shadow stretches
    draw_drop_shadow(draw, 18, 33, 12, 2)

    bob = -1 if step in (1, 3) else 0

    # Back paws (walking cycle)
    if step == 0:
        draw.rectangle([8, 31, 12, 33], fill=p["paws"])
        draw.rectangle([22, 31, 26, 33], fill=p["paws"])
    elif step == 1:
        draw.rectangle([10, 30, 14, 32], fill=p["paws"])
        draw.rectangle([24, 31, 27, 33], fill=p["paws"])
    elif step == 2:
        draw.rectangle([12, 31, 16, 33], fill=p["paws"])
        draw.rectangle([21, 30, 25, 32], fill=p["paws"])
    else:
        draw.rectangle([7, 31, 11, 33], fill=p["paws"])
        draw.rectangle([23, 31, 27, 33], fill=p["paws"])

    # Body (slightly oval tilted forward)
    draw.ellipse([7, 14 + bob, 27, 31 + bob], fill=p["fur_main"], outline=p["outline"])
    # Chubby forward cheek
    draw.ellipse([18, 16 + bob, 29, 29 + bob], fill=p["fur_main"])
    draw.ellipse([14, 20 + bob, 26, 31 + bob], fill=p["belly"])

    # Tiny tail bump on left
    draw.ellipse([5, 24 + bob, 8, 27 + bob], fill=p["paws"])

    # Ears
    ear_y = 11 + bob
    # Left ear (further away)
    draw.ellipse([12, ear_y, 17, ear_y + 6], fill=p["fur_shadow"], outline=p["outline"])
    # Right ear (nearer)
    draw.ellipse([18, ear_y - 1, 24, ear_y + 6], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([19, ear_y + 1, 22, ear_y + 4], fill=p["inner_ear"])

    # Eye (profile, one eye dominant, shiny)
    draw.ellipse([23, 18 + bob, 27, 22 + bob], fill=p["eyes"])
    draw.point((24, 19 + bob), fill=(255, 255, 255, 255))

    # Cheek blush
    draw.ellipse([24, 23 + bob, 27, 25 + bob], fill=p["blush"])

    # Nose
    draw.point((28, 21 + bob), fill=p["nose"])
    draw.point((28, 22 + bob), fill=p["outline"])

    # Front paw bobbing
    if step in (0, 2):
        draw.ellipse([19, 27 + bob, 23, 30 + bob], fill=p["paws"])
    else:
        draw.ellipse([21, 26 + bob, 25, 29 + bob], fill=p["paws"])

    # Whiskers
    if p.get("whiskers", True):
        draw.line([(28, 20 + bob), (32, 19 + bob)], fill=(255, 255, 255, 180))
        draw.line([(28, 22 + bob), (32, 23 + bob)], fill=(255, 255, 255, 180))

    return img


def render_eat_frame(palette, step=0):
    """
    Sitting upright, holding sunflower seed in paws and munching.
    step 0 to 3: nibble cycle
    """
    img = create_canvas(36, 36)
    draw = ImageDraw.Draw(img)
    p = palette

    draw_drop_shadow(draw, 18, 33, 10, 2)

    # Feet flat on floor
    draw.rectangle([9, 31, 14, 33], fill=p["paws"])
    draw.rectangle([21, 31, 26, 33], fill=p["paws"])

    # Body sitting tall
    draw.ellipse([8, 13, 27, 32], fill=p["fur_main"], outline=p["outline"])
    # Puffed cheeks
    cheek_puff = 1 if step in (1, 3) else 0
    draw.ellipse([6 - cheek_puff, 16, 17, 29], fill=p["fur_main"])
    draw.ellipse([18, 16, 29 + cheek_puff, 29], fill=p["fur_main"])

    # White belly
    draw.ellipse([12, 18, 23, 31], fill=p["belly"])

    # Ears perked up happily
    draw.ellipse([8, 10, 14, 17], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([10, 12, 13, 15], fill=p["inner_ear"])
    draw.ellipse([21, 10, 27, 17], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([22, 12, 25, 15], fill=p["inner_ear"])

    # Cheerful closed eyes (^ ^)
    draw.line([(11, 19), (13, 18)], fill=p["eyes"])
    draw.line([(13, 18), (15, 19)], fill=p["eyes"])
    draw.line([(20, 19), (22, 18)], fill=p["eyes"])
    draw.line([(22, 18), (24, 19)], fill=p["eyes"])

    # Intense happy blush
    draw.ellipse([7 - cheek_puff, 21, 11, 24], fill=p["blush"])
    draw.ellipse([24, 21, 28 + cheek_puff, 24], fill=p["blush"])

    # Nose
    draw.point((17, 21), fill=p["nose"])
    draw.point((18, 21), fill=p["nose"])

    # The Sunflower Seed! Held in front paws
    seed_y = 22 + (1 if step in (1, 3) else 0)
    # Seed body
    draw.polygon([(17, seed_y - 2), (15, seed_y + 3), (20, seed_y + 3)], fill=SEED_SHELL)
    draw.line([(17, seed_y - 1), (17, seed_y + 2)], fill=SEED_STRIPE)

    # Little paws gripping seed
    draw.ellipse([13, seed_y + 1, 16, seed_y + 4], fill=p["paws"])
    draw.ellipse([19, seed_y + 1, 22, seed_y + 4], fill=p["paws"])

    # Munch crumbs!
    if step in (1, 3):
        crumb_color = (230, 210, 140, 220)
        draw.point((14, seed_y - 1), fill=crumb_color)
        draw.point((21, seed_y), fill=crumb_color)

    return img


def render_sleep_frame(palette, step=0):
    """
    Curled into a peaceful ball, breathing slowly.
    step 0 to 3: breathing + animated "Zzz"
    """
    img = create_canvas(36, 36)
    draw = ImageDraw.Draw(img)
    p = palette

    draw_drop_shadow(draw, 18, 33, 12, 2)

    # Breathing pulse
    pulse = 1 if step in (1, 2) else 0

    # Curled ball body
    draw.ellipse([7, 18 - pulse, 28, 33], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([12, 23 - pulse, 26, 32], fill=p["belly"])

    # Small curled ear
    draw.ellipse([10, 17 - pulse, 15, 23 - pulse], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([11, 19 - pulse, 13, 21 - pulse], fill=p["inner_ear"])

    # Sleeping closed eye: line curved down
    draw.line([(18, 23 - pulse), (22, 23 - pulse)], fill=p["eyes"])
    draw.point((20, 24 - pulse), fill=p["eyes"])

    # Cute nose tucked
    draw.point((24, 25 - pulse), fill=p["nose"])

    # Little paw tucked under cheek
    draw.ellipse([21, 27 - pulse, 25, 30 - pulse], fill=p["paws"])

    # Little tail
    draw.ellipse([7, 27, 9, 29], fill=p["paws"])

    # Floating "Zzz"
    z_color = (130, 160, 230, 220)
    z_y = 12 - (step * 2)
    z_x = 22 + (step * 2)

    def draw_tiny_z(dx, dy, size=3):
        draw.line([(dx, dy), (dx + size, dy)], fill=z_color)
        draw.line([(dx + size, dy), (dx, dy + size)], fill=z_color)
        draw.line([(dx, dy + size), (dx + size, dy + size)], fill=z_color)

    if step >= 0:
        draw_tiny_z(22, 14, 3)
    if step >= 1:
        draw_tiny_z(26, 9, 4)
    if step >= 2:
        draw_tiny_z(29, 3, 5)

    return img


def render_drag_frame(palette, step=0):
    """
    Gunther picked up by cursor!
    Held by scruff, paws dangling & wiggling in air.
    """
    img = create_canvas(36, 36)
    draw = ImageDraw.Draw(img)
    p = palette

    # Scruff / pinch point at top
    pinch_x = 18

    # Elongated body hanging down
    draw.ellipse([9, 8, 26, 28], fill=p["fur_main"], outline=p["outline"])
    # Belly exposed
    draw.ellipse([12, 12, 23, 26], fill=p["belly"])

    # Ears folded back slightly
    draw.ellipse([8, 6, 13, 12], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([9, 8, 12, 11], fill=p["inner_ear"])
    draw.ellipse([22, 6, 27, 12], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([23, 8, 26, 11], fill=p["inner_ear"])

    # Surprised / cute wide eyes (O O)
    draw.ellipse([11, 12, 15, 16], fill=p["eyes"])
    draw.point((12, 13), fill=(255, 255, 255, 255))
    draw.ellipse([20, 12, 24, 16], fill=p["eyes"])
    draw.point((21, 13), fill=(255, 255, 255, 255))

    # Little 'o' mouth
    draw.point((17, 18), fill=p["nose"])
    draw.point((18, 18), fill=p["nose"])
    draw.point((17, 19), fill=p["outline"])
    draw.point((18, 19), fill=p["outline"])

    # Front paws wiggling in air
    pw_off = 1 if step % 2 == 0 else -1
    draw.ellipse([10, 19 + pw_off, 13, 23 + pw_off], fill=p["paws"])
    draw.ellipse([22, 19 - pw_off, 25, 23 - pw_off], fill=p["paws"])

    # Back paws dangling below
    draw.ellipse([11, 28 - pw_off, 15, 32 - pw_off], fill=p["paws"])
    draw.ellipse([20, 28 + pw_off, 24, 32 + pw_off], fill=p["paws"])

    # Whiskers
    if p.get("whiskers", True):
        draw.line([(7, 17), (11, 17)], fill=(255, 255, 255, 180))
        draw.line([(24, 17), (28, 17)], fill=(255, 255, 255, 180))

    return img


def render_pet_frame(palette, step=0):
    """
    Being petted! Blissful expression, floating pink hearts.
    """
    img = create_canvas(36, 36)
    draw = ImageDraw.Draw(img)
    p = palette

    draw_drop_shadow(draw, 18, 33, 11, 2)

    # Squished slightly down in bliss
    draw.ellipse([8, 16, 27, 33], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([5, 18, 17, 31], fill=p["fur_main"])
    draw.ellipse([18, 18, 30, 31], fill=p["fur_main"])
    draw.ellipse([11, 20, 24, 32], fill=p["belly"])

    # Flat, relaxed ears
    draw.ellipse([6, 16, 12, 21], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([8, 17, 11, 20], fill=p["inner_ear"])
    draw.ellipse([23, 16, 29, 21], fill=p["fur_main"], outline=p["outline"])
    draw.ellipse([24, 17, 27, 20], fill=p["inner_ear"])

    # Ecstatic eyes: ^ ^
    draw.line([(11, 20), (13, 18)], fill=p["eyes"], width=1)
    draw.line([(13, 18), (15, 20)], fill=p["eyes"], width=1)
    draw.line([(20, 20), (22, 18)], fill=p["eyes"], width=1)
    draw.line([(22, 18), (24, 20)], fill=p["eyes"], width=1)

    # Deep rosy blush
    draw.ellipse([7, 22, 12, 26], fill=(255, 100, 130, 200))
    draw.ellipse([23, 22, 28, 26], fill=(255, 100, 130, 200))

    # Paws clasped happily
    draw.ellipse([14, 26, 17, 29], fill=p["paws"])
    draw.ellipse([18, 26, 21, 29], fill=p["paws"])

    # Floating heart above
    heart_y = 10 - step * 2
    heart_color = (255, 80, 120, 240)

    def draw_heart(hx, hy):
        # 5x4 heart pixel shape
        draw.point((hx + 1, hy), fill=heart_color)
        draw.point((hx + 3, hy), fill=heart_color)
        draw.line([(hx, hy + 1), (hx + 4, hy + 1)], fill=heart_color)
        draw.line([(hx + 1, hy + 2), (hx + 3, hy + 2)], fill=heart_color)
        draw.point((hx + 2, hy + 3), fill=heart_color)

    draw_heart(16, max(1, heart_y))

    return img


def generate_all_sprites(output_dir="assets/sprites", scale=3):
    """
    Generates all sprite frames for each palette, scaled up with NEAREST filter
    so pixels remain crisp and vibrant!
    """
    os.makedirs(output_dir, exist_ok=True)

    for pkey, palette in PALETTES.items():
        pal_dir = os.path.join(output_dir, pkey)
        os.makedirs(pal_dir, exist_ok=True)

        # 1. Idle (4 frames)
        for i in range(4):
            f = render_idle_frame(palette, i)
            f_scaled = f.resize((f.width * scale, f.height * scale), Image.Resampling.NEAREST)
            f_scaled.save(os.path.join(pal_dir, f"idle_{i}.png"))

        # 2. Walk (4 frames)
        for i in range(4):
            f_right = render_walk_frame(palette, i)
            f_right_scaled = f_right.resize((f_right.width * scale, f_right.height * scale), Image.Resampling.NEAREST)
            f_right_scaled.save(os.path.join(pal_dir, f"walk_right_{i}.png"))

            # Flip for left walk
            f_left = f_right.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            f_left_scaled = f_left.resize((f_left.width * scale, f_left.height * scale), Image.Resampling.NEAREST)
            f_left_scaled.save(os.path.join(pal_dir, f"walk_left_{i}.png"))

        # 3. Eat (4 frames)
        for i in range(4):
            f = render_eat_frame(palette, i)
            f_scaled = f.resize((f.width * scale, f.height * scale), Image.Resampling.NEAREST)
            f_scaled.save(os.path.join(pal_dir, f"eat_{i}.png"))

        # 4. Sleep (4 frames)
        for i in range(4):
            f = render_sleep_frame(palette, i)
            f_scaled = f.resize((f.width * scale, f.height * scale), Image.Resampling.NEAREST)
            f_scaled.save(os.path.join(pal_dir, f"sleep_{i}.png"))

        # 5. Dragged / Picked Up (4 frames)
        for i in range(4):
            f = render_drag_frame(palette, i)
            f_scaled = f.resize((f.width * scale, f.height * scale), Image.Resampling.NEAREST)
            f_scaled.save(os.path.join(pal_dir, f"drag_{i}.png"))

        # 6. Pet / Love (4 frames)
        for i in range(4):
            f = render_pet_frame(palette, i)
            f_scaled = f.resize((f.width * scale, f.height * scale), Image.Resampling.NEAREST)
            f_scaled.save(os.path.join(pal_dir, f"pet_{i}.png"))

        print(f"Generated sprites for palette: {pkey}")


if __name__ == "__main__":
    generate_all_sprites()
