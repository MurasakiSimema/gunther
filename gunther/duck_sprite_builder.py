"""
Sprite generator for adorable pixel art ducklings (Paperelle).
Generates crisp, high-quality sprites for all animations and multiple duck palettes,
including the white Pekin duck, classic rubber ducky, mallard duckling, and pastel variants.
"""

from PIL import Image, ImageDraw
import os
import sys
import argparse

# Ensure UTF-8 output on Windows consoles without charmap crash
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Resampling and transpose compatibility across Pillow versions
RESAMPLE_FILTER = getattr(getattr(Image, "Resampling", Image), "NEAREST", Image.NEAREST)
FLIP_HORIZONTAL = getattr(getattr(Image, "Transpose", Image), "FLIP_LEFT_RIGHT", Image.FLIP_LEFT_RIGHT)

PALETTES = {
    "papera_bianca": {
        "name": "Paperella Bianca (Pekin)",
        "feather_main": (255, 255, 255, 255),
        "feather_shadow": (212, 222, 238, 255),
        "feather_light": (255, 255, 255, 255),
        "belly": (248, 250, 255, 255),
        "belly_shadow": (205, 215, 232, 255),
        "bill": (255, 145, 20, 255),
        "bill_shadow": (215, 100, 10, 255),
        "bill_light": (255, 185, 75, 255),
        "feet": (255, 140, 25, 255),
        "feet_shadow": (210, 95, 15, 255),
        "blush": (255, 150, 170, 150),
        "eyes": (24, 28, 36, 255),
        "outline": (120, 132, 152, 220),
        "crest": True,
    },
    "papera_gialla": {
        "name": "Paperella Gialla Classica",
        "feather_main": (255, 218, 48, 255),
        "feather_shadow": (228, 172, 24, 255),
        "feather_light": (255, 242, 130, 255),
        "belly": (255, 236, 120, 255),
        "belly_shadow": (235, 185, 45, 255),
        "bill": (255, 125, 20, 255),
        "bill_shadow": (210, 85, 10, 255),
        "bill_light": (255, 175, 70, 255),
        "feet": (255, 130, 25, 255),
        "feet_shadow": (205, 88, 15, 255),
        "blush": (255, 130, 145, 160),
        "eyes": (25, 20, 20, 255),
        "outline": (145, 85, 20, 220),
        "crest": True,
    },
    "papera_germano": {
        "name": "Germano Reale (Mallard Duckling)",
        "feather_main": (248, 210, 95, 255),
        "feather_shadow": (80, 56, 40, 255),
        "feather_light": (255, 232, 140, 255),
        "cap_color": (60, 42, 30, 255),
        "belly": (245, 220, 135, 255),
        "belly_shadow": (205, 170, 80, 255),
        "bill": (160, 170, 50, 255),
        "bill_shadow": (120, 128, 35, 255),
        "bill_light": (195, 205, 95, 255),
        "feet": (225, 125, 40, 255),
        "feet_shadow": (180, 85, 25, 255),
        "blush": (245, 140, 120, 150),
        "eyes": (25, 18, 15, 255),
        "outline": (50, 36, 26, 220),
        "crest": False,
    },
    "papera_rosa": {
        "name": "Paperella Rosa Pastello",
        "feather_main": (255, 195, 215, 255),
        "feather_shadow": (228, 150, 178, 255),
        "feather_light": (255, 228, 238, 255),
        "belly": (255, 240, 246, 255),
        "belly_shadow": (235, 190, 210, 255),
        "bill": (255, 215, 60, 255),
        "bill_shadow": (220, 170, 30, 255),
        "bill_light": (255, 238, 140, 255),
        "feet": (255, 160, 90, 255),
        "feet_shadow": (218, 120, 55, 255),
        "blush": (255, 110, 150, 170),
        "eyes": (30, 20, 32, 255),
        "outline": (130, 75, 100, 220),
        "crest": True,
    },
    "papera_menta": {
        "name": "Paperella Verde Menta",
        "feather_main": (190, 238, 220, 255),
        "feather_shadow": (148, 202, 182, 255),
        "feather_light": (225, 252, 242, 255),
        "belly": (235, 252, 245, 255),
        "belly_shadow": (195, 232, 220, 255),
        "bill": (255, 215, 65, 255),
        "bill_shadow": (220, 175, 35, 255),
        "bill_light": (255, 238, 140, 255),
        "feet": (255, 175, 110, 255),
        "feet_shadow": (218, 135, 75, 255),
        "blush": (255, 140, 160, 150),
        "eyes": (20, 32, 28, 255),
        "outline": (75, 125, 110, 220),
        "crest": True,
    },
    "papera_cioccolato": {
        "name": "Paperella Cioccolato (Moka)",
        "feather_main": (125, 90, 68, 255),
        "feather_shadow": (85, 58, 42, 255),
        "feather_light": (165, 125, 98, 255),
        "belly": (235, 208, 180, 255),
        "belly_shadow": (195, 165, 135, 255),
        "bill": (245, 140, 35, 255),
        "bill_shadow": (195, 95, 20, 255),
        "bill_light": (255, 180, 85, 255),
        "feet": (220, 115, 35, 255),
        "feet_shadow": (170, 75, 20, 255),
        "blush": (255, 130, 140, 150),
        "eyes": (25, 18, 15, 255),
        "outline": (50, 35, 26, 220),
        "crest": True,
    }
}

PEA_COLOR = (115, 205, 55, 255)
PEA_LIGHT = (175, 242, 105, 255)
PEA_SHADOW = (65, 135, 25, 255)
SHADOW_COLOR = (0, 0, 0, 45)


def create_canvas(w=36, h=36):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def draw_drop_shadow(draw, cx, cy, rx, ry):
    """Draws a soft ground shadow underneath the duckling."""
    for y in range(cy - ry, cy + ry + 1):
        for x in range(cx - rx, cx + rx + 1):
            dx = (x - cx) / rx
            dy = (y - cy) / ry
            if dx*dx + dy*dy <= 1.0:
                draw.point((x, y), fill=SHADOW_COLOR)


def render_idle_frame(palette, step=0):
    """
    Renders an idle frame (breathing bob, happy waggle/quack, blinking).
    step: 0=normal, 1=breathe up, 2=happy head tilt & quack smile, 3=blink
    """
    img = create_canvas(36, 36)
    draw = ImageDraw.Draw(img)
    p = palette

    draw_drop_shadow(draw, 18, 33, 11, 2)

    dy = -1 if step == 1 else 0
    tilt = (step == 2)
    blink = (step == 3)

    # Webbed Feet flat on ground
    # Left foot
    draw.polygon([(11, 30), (8, 33), (14, 33)], fill=p["feet"])
    draw.line([(8, 33), (14, 33)], fill=p["feet_shadow"])
    # Right foot
    draw.polygon([(24, 30), (21, 33), (27, 33)], fill=p["feet"])
    draw.line([(21, 33), (27, 33)], fill=p["feet_shadow"])

    # Cute duck tail pointing up behind to the left
    tail_wag = -1 if tilt else 0
    draw.polygon([(9, 25 + dy), (3, 19 + dy + tail_wag), (10, 20 + dy)], fill=p["feather_main"], outline=p["outline"])
    draw.polygon([(8, 24 + dy), (4, 20 + dy + tail_wag), (10, 21 + dy)], fill=p["feather_light"])

    # Chubby body
    draw.ellipse([7, 15 + dy, 28, 32 + dy], fill=p["feather_main"], outline=p["outline"])
    draw.ellipse([9, 25 + dy, 26, 32 + dy], fill=p["feather_shadow"])
    draw.ellipse([11, 19 + dy, 24, 31 + dy], fill=p["belly"])

    # Folded wings on sides
    # Left wing
    draw.ellipse([6, 18 + dy, 12, 28 + dy], fill=p["feather_main"], outline=p["outline"])
    draw.arc([7, 20 + dy, 11, 26 + dy], 60, 240, fill=p["feather_light"])
    # Right wing
    draw.ellipse([23, 18 + dy, 29, 28 + dy], fill=p["feather_main"], outline=p["outline"])
    draw.arc([24, 20 + dy, 28, 26 + dy], 300, 120, fill=p["feather_light"])

    # Duck Head
    head_y = 8 + dy - (1 if tilt else 0)
    draw.ellipse([9, head_y, 26, head_y + 15], fill=p["feather_main"], outline=p["outline"])

    # Mallard Cap
    if "cap_color" in p:
        draw.ellipse([11, head_y, 24, head_y + 4], fill=p["cap_color"])
    else:
        draw.ellipse([15, head_y + 1, 20, head_y + 5], fill=p["feather_light"])

    # Tiny feather crest tuft on top of head
    if p.get("crest", True):
        draw.line([(17, head_y), (16, head_y - 3)], fill=p["feather_main"], width=2)
        draw.point((16, head_y - 3), fill=p["feather_light"])
        draw.point((17, head_y - 2), fill=p["outline"])

    # Eyes & Face
    eye_y = head_y + 6

    # Mallard eye stripe
    if "cap_color" in p:
        draw.line([(9, eye_y + 2), (12, eye_y + 2)], fill=p["cap_color"], width=1)
        draw.line([(23, eye_y + 2), (26, eye_y + 2)], fill=p["cap_color"], width=1)

    if blink:
        # Happy closed eyes (^ ^)
        draw.line([(11, eye_y + 1), (13, eye_y)], fill=p["eyes"], width=1)
        draw.line([(13, eye_y), (15, eye_y + 1)], fill=p["eyes"], width=1)
        draw.line([(20, eye_y + 1), (22, eye_y)], fill=p["eyes"], width=1)
        draw.line([(22, eye_y), (24, eye_y + 1)], fill=p["eyes"], width=1)
    else:
        # Shiny button eyes
        draw.ellipse([11, eye_y, 15, eye_y + 4], fill=p["eyes"])
        draw.point((12, eye_y + 1), fill=(255, 255, 255, 255))
        draw.ellipse([20, eye_y, 24, eye_y + 4], fill=p["eyes"])
        draw.point((21, eye_y + 1), fill=(255, 255, 255, 255))

    # Rosy cheeks
    draw.ellipse([8, eye_y + 3, 11, eye_y + 6], fill=p["blush"])
    draw.ellipse([24, eye_y + 3, 27, eye_y + 6], fill=p["blush"])

    # Duck Bill
    bill_y = eye_y + 3
    draw.rounded_rectangle([14, bill_y, 21, bill_y + 4], radius=2, fill=p["bill"], outline=p["bill_shadow"])
    draw.line([(15, bill_y), (20, bill_y)], fill=p["bill_light"])
    # Nostrils
    draw.point((16, bill_y + 1), fill=p["bill_shadow"])
    draw.point((19, bill_y + 1), fill=p["bill_shadow"])

    # Quack mouth if tilt
    if tilt:
        draw.line([(16, bill_y + 3), (19, bill_y + 3)], fill=(255, 110, 130, 255))

    return img


def render_walk_frame(palette, step=0):
    """
    Walking / waddling in profile-3/4 view (facing right).
    step 0 to 3: iconic duck waddle cycle.
    """
    img = create_canvas(36, 36)
    draw = ImageDraw.Draw(img)
    p = palette

    draw_drop_shadow(draw, 18, 33, 12, 2)

    bob = -1 if step in (1, 3) else 0

    # Waddle Feet
    if step == 0:
        draw.polygon([(10, 31), (7, 33), (13, 33)], fill=p["feet"])
        draw.polygon([(22, 30), (19, 32), (25, 32)], fill=p["feet"])
    elif step == 1:
        draw.polygon([(9, 30), (6, 32), (12, 32)], fill=p["feet"])
        draw.polygon([(24, 31), (21, 33), (27, 33)], fill=p["feet"])
    elif step == 2:
        draw.polygon([(13, 31), (10, 33), (16, 33)], fill=p["feet"])
        draw.polygon([(21, 30), (18, 32), (24, 32)], fill=p["feet"])
    else:
        draw.polygon([(8, 31), (5, 33), (11, 33)], fill=p["feet"])
        draw.polygon([(23, 31), (20, 33), (26, 33)], fill=p["feet"])

    # Tail pointing up back-left
    tail_tw = -1 if step in (0, 2) else 0
    draw.polygon([(7, 23 + bob), (2, 17 + bob + tail_tw), (8, 18 + bob)], fill=p["feather_main"], outline=p["outline"])
    draw.polygon([(6, 22 + bob), (3, 18 + bob + tail_tw), (8, 19 + bob)], fill=p["feather_light"])

    # Body forward tilted
    draw.ellipse([6, 14 + bob, 27, 31 + bob], fill=p["feather_main"], outline=p["outline"])
    draw.ellipse([16, 17 + bob, 28, 30 + bob], fill=p["feather_main"])
    draw.ellipse([13, 20 + bob, 25, 31 + bob], fill=p["belly"])

    # Wing on side (flutters slightly on up-step)
    wing_lift = -1 if step in (1, 3) else 0
    draw.ellipse([8, 17 + bob + wing_lift, 20, 26 + bob + wing_lift], fill=p["feather_main"], outline=p["outline"])
    draw.arc([10, 19 + bob + wing_lift, 18, 25 + bob + wing_lift], 80, 260, fill=p["feather_light"])

    # Head forward
    head_y = 8 + bob
    draw.ellipse([14, head_y, 29, head_y + 15], fill=p["feather_main"], outline=p["outline"])

    if "cap_color" in p:
        draw.ellipse([15, head_y, 25, head_y + 4], fill=p["cap_color"])
    else:
        draw.ellipse([17, head_y + 1, 23, head_y + 5], fill=p["feather_light"])

    # Crest
    if p.get("crest", True):
        draw.line([(19, head_y), (17, head_y - 3)], fill=p["feather_main"], width=2)
        draw.point((17, head_y - 3), fill=p["feather_light"])

    # Profile Eye
    eye_y = head_y + 5
    if "cap_color" in p:
        draw.line([(14, eye_y + 2), (21, eye_y + 2)], fill=p["cap_color"], width=1)
        draw.line([(25, eye_y + 2), (28, eye_y + 2)], fill=p["cap_color"], width=1)

    draw.ellipse([21, eye_y, 25, eye_y + 4], fill=p["eyes"])
    draw.point((22, eye_y + 1), fill=(255, 255, 255, 255))

    # Cheek blush
    draw.ellipse([20, eye_y + 4, 24, eye_y + 6], fill=p["blush"])

    # Profile Beak pointing right
    draw.rounded_rectangle([25, eye_y + 2, 33, eye_y + 7], radius=2, fill=p["bill"], outline=p["bill_shadow"])
    draw.line([(26, eye_y + 2), (32, eye_y + 2)], fill=p["bill_light"])
    draw.line([(26, eye_y + 5), (32, eye_y + 5)], fill=p["bill_shadow"])
    draw.point((27, eye_y + 3), fill=p["bill_shadow"])

    return img


def render_eat_frame(palette, step=0):
    """
    Eating yummy green pea treat!
    step 0: looking excitedly down at pea
    step 1: head dips down, bill nibbling pea, crumbs fly!
    step 2: head up, chewing happily with cheeks puffed
    step 3: swallowing happily with closed eyes (^ ^) and sweet sparkles
    """
    img = create_canvas(36, 36)
    draw = ImageDraw.Draw(img)
    p = palette

    draw_drop_shadow(draw, 18, 33, 11, 2)

    # Feet flat
    draw.polygon([(10, 31), (7, 33), (13, 33)], fill=p["feet"])
    draw.polygon([(23, 31), (20, 33), (26, 33)], fill=p["feet"])

    # Tail
    draw.polygon([(8, 24), (3, 18), (9, 19)], fill=p["feather_main"], outline=p["outline"])

    # Body
    draw.ellipse([7, 15, 28, 32], fill=p["feather_main"], outline=p["outline"])
    draw.ellipse([11, 19, 24, 31], fill=p["belly"])

    # Wings folded
    draw.ellipse([6, 18, 12, 28], fill=p["feather_main"], outline=p["outline"])
    draw.ellipse([23, 18, 29, 28], fill=p["feather_main"], outline=p["outline"])

    # Head and eating cycle
    dip = 2 if step == 1 else 0
    head_y = 8 + dip
    draw.ellipse([9, head_y, 26, head_y + 15], fill=p["feather_main"], outline=p["outline"])

    if "cap_color" in p:
        draw.ellipse([11, head_y, 24, head_y + 4], fill=p["cap_color"])

    if p.get("crest", True):
        draw.line([(17, head_y), (16, head_y - 3)], fill=p["feather_main"], width=2)
        draw.point((16, head_y - 3), fill=p["feather_light"])

    eye_y = head_y + 6
    if step in (1, 3):
        # Cheerful happy eyes (^ ^)
        draw.line([(11, eye_y + 1), (13, eye_y)], fill=p["eyes"], width=1)
        draw.line([(13, eye_y), (15, eye_y + 1)], fill=p["eyes"], width=1)
        draw.line([(20, eye_y + 1), (22, eye_y)], fill=p["eyes"], width=1)
        draw.line([(22, eye_y), (24, eye_y + 1)], fill=p["eyes"], width=1)
    else:
        # Looking down at treat
        draw.ellipse([11, eye_y, 15, eye_y + 4], fill=p["eyes"])
        draw.point((12, eye_y + 2), fill=(255, 255, 255, 255))
        draw.ellipse([20, eye_y, 24, eye_y + 4], fill=p["eyes"])
        draw.point((21, eye_y + 2), fill=(255, 255, 255, 255))

    # Cheeks
    draw.ellipse([8, eye_y + 3, 11, eye_y + 6], fill=p["blush"])
    draw.ellipse([24, eye_y + 3, 27, eye_y + 6], fill=p["blush"])

    # Beak
    bill_y = eye_y + 3
    draw.rounded_rectangle([14, bill_y, 21, bill_y + 4], radius=2, fill=p["bill"], outline=p["bill_shadow"])
    draw.line([(15, bill_y), (20, bill_y)], fill=p["bill_light"])

    # Pea treat
    if step == 0:
        # Pea on floor
        draw.ellipse([16, 27, 20, 31], fill=PEA_COLOR, outline=PEA_SHADOW)
        draw.point((17, 28), fill=PEA_LIGHT)
    elif step == 1:
        # Nibbling pea
        draw.ellipse([16, 25, 20, 29], fill=PEA_COLOR, outline=PEA_SHADOW)
        # Crumbs flying
        draw.point((14, 23), fill=PEA_LIGHT)
        draw.point((22, 24), fill=PEA_LIGHT)
    elif step == 2:
        # Chewing: pea half eaten in beak
        draw.ellipse([16, 22, 19, 25], fill=PEA_COLOR)
        draw.point((15, 25), fill=PEA_LIGHT)
        draw.point((21, 23), fill=PEA_LIGHT)
    elif step == 3:
        # Swallow! Happy sparkles
        draw.point((13, 22), fill=PEA_LIGHT)
        draw.point((23, 22), fill=PEA_LIGHT)

    return img


def render_sleep_frame(palette, step=0):
    """
    Duck loaf sleeping! Head tucked resting on back/wing.
    Animated Zzz floating up.
    """
    img = create_canvas(36, 36)
    draw = ImageDraw.Draw(img)
    p = palette

    draw_drop_shadow(draw, 18, 33, 12, 2)

    pulse = 1 if step in (1, 2) else 0

    # Loaf body resting on floor
    draw.ellipse([6, 17 - pulse, 29, 33], fill=p["feather_main"], outline=p["outline"])
    draw.ellipse([9, 26, 26, 33], fill=p["feather_shadow"])
    draw.ellipse([11, 21 - pulse, 25, 32], fill=p["belly"])

    # Tail curled up back left
    draw.polygon([(8, 23 - pulse), (3, 18 - pulse), (9, 19 - pulse)], fill=p["feather_main"], outline=p["outline"])

    # Wing along side
    draw.ellipse([9, 19 - pulse, 22, 28 - pulse], fill=p["feather_main"], outline=p["outline"])
    draw.arc([11, 21 - pulse, 20, 26 - pulse], 70, 250, fill=p["feather_light"])

    # Head tucked back resting on feathers
    head_y = 13 - pulse
    draw.ellipse([15, head_y, 28, head_y + 14], fill=p["feather_main"], outline=p["outline"])

    if "cap_color" in p:
        draw.ellipse([16, head_y, 27, head_y + 4], fill=p["cap_color"])

    # Sleeping closed eye: curved line
    draw.line([(18, head_y + 6), (22, head_y + 6)], fill=p["eyes"], width=1)
    draw.point((20, head_y + 7), fill=p["eyes"])

    # Blush
    draw.ellipse([17, head_y + 8, 20, head_y + 10], fill=p["blush"])

    # Tucked beak
    draw.rounded_rectangle([22, head_y + 6, 29, head_y + 10], radius=2, fill=p["bill"], outline=p["bill_shadow"])
    draw.line([(23, head_y + 6), (28, head_y + 6)], fill=p["bill_light"])

    # Animated floating "Zzz"
    z_color = (130, 165, 235, 220)
    def draw_tiny_z(dx, dy, size=3):
        draw.line([(dx, dy), (dx + size, dy)], fill=z_color)
        draw.line([(dx + size, dy), (dx, dy + size)], fill=z_color)
        draw.line([(dx, dy + size), (dx + size, dy + size)], fill=z_color)

    if step >= 0:
        draw_tiny_z(22, 11, 3)
    if step >= 1:
        draw_tiny_z(26, 6, 4)
    if step >= 2:
        draw_tiny_z(29, 2, 5)

    return img


def render_drag_frame(palette, step=0):
    """
    Picked up by cursor! Wings flapping, feet kicking, surprised quack!
    """
    img = create_canvas(36, 36)
    draw = ImageDraw.Draw(img)
    p = palette

    # Elongated body hanging
    draw.ellipse([9, 8, 27, 28], fill=p["feather_main"], outline=p["outline"])
    draw.ellipse([12, 12, 24, 26], fill=p["belly"])

    # Flapping wings
    wing_up = (step % 2 == 0)
    if wing_up:
        # Wings up!
        draw.polygon([(10, 14), (2, 8), (9, 20)], fill=p["feather_main"], outline=p["outline"])
        draw.polygon([(26, 14), (34, 8), (27, 20)], fill=p["feather_main"], outline=p["outline"])
    else:
        # Wings down!
        draw.polygon([(10, 15), (2, 22), (9, 23)], fill=p["feather_main"], outline=p["outline"])
        draw.polygon([(26, 15), (34, 22), (27, 23)], fill=p["feather_main"], outline=p["outline"])

    # Feet paddling/kicking
    kw = 2 if step % 2 == 0 else -2
    draw.polygon([(11, 28 + kw), (8, 33 + kw), (14, 33 + kw)], fill=p["feet"])
    draw.polygon([(22, 28 - kw), (19, 33 - kw), (25, 33 - kw)], fill=p["feet"])

    # Head
    draw.ellipse([10, 6, 26, 20], fill=p["feather_main"], outline=p["outline"])

    if "cap_color" in p:
        draw.ellipse([12, 6, 24, 10], fill=p["cap_color"])

    if p.get("crest", True):
        draw.line([(18, 6), (17, 3)], fill=p["feather_main"], width=2)
        draw.point((17, 3), fill=p["feather_light"])

    # Surprised wide eyes (O O)
    draw.ellipse([11, 10, 15, 15], fill=p["eyes"])
    draw.point((12, 11), fill=(255, 255, 255, 255))
    draw.ellipse([21, 10, 25, 15], fill=p["eyes"])
    draw.point((22, 11), fill=(255, 255, 255, 255))

    # Blushing in surprise
    draw.ellipse([8, 14, 11, 17], fill=p["blush"])
    draw.ellipse([25, 14, 28, 17], fill=p["blush"])

    # Open surprised "o" beak ("quack!")
    draw.rounded_rectangle([15, 15, 21, 19], radius=2, fill=p["bill"], outline=p["bill_shadow"])
    draw.ellipse([17, 16, 19, 18], fill=(185, 45, 60, 255))

    return img


def render_pet_frame(palette, step=0):
    """
    Being cuddled / petted!
    Squished down in ecstasy, closed happy eyes, bright rosy cheeks, floating heart!
    """
    img = create_canvas(36, 36)
    draw = ImageDraw.Draw(img)
    p = palette

    draw_drop_shadow(draw, 18, 33, 11, 2)

    # Squished body
    draw.ellipse([6, 17, 30, 33], fill=p["feather_main"], outline=p["outline"])
    draw.ellipse([10, 20, 26, 32], fill=p["belly"])

    # Cozy wings
    draw.ellipse([5, 19, 12, 29], fill=p["feather_main"], outline=p["outline"])
    draw.ellipse([24, 19, 31, 29], fill=p["feather_main"], outline=p["outline"])

    # Head relaxed and snug
    draw.ellipse([9, 11, 27, 24], fill=p["feather_main"], outline=p["outline"])

    if "cap_color" in p:
        draw.ellipse([11, 11, 25, 15], fill=p["cap_color"])

    # Ecstatic eyes (^ ^)
    eye_y = 15
    draw.line([(11, eye_y + 1), (13, eye_y)], fill=p["eyes"], width=1)
    draw.line([(13, eye_y), (15, eye_y + 1)], fill=p["eyes"], width=1)
    draw.line([(21, eye_y + 1), (23, eye_y)], fill=p["eyes"], width=1)
    draw.line([(23, eye_y), (25, eye_y + 1)], fill=p["eyes"], width=1)

    # Radiant rosy blush
    draw.ellipse([7, eye_y + 2, 12, eye_y + 6], fill=(255, 100, 130, 220))
    draw.ellipse([24, eye_y + 2, 29, eye_y + 6], fill=(255, 100, 130, 220))

    # Sweet smiling beak
    bill_y = eye_y + 3
    draw.rounded_rectangle([15, bill_y, 21, bill_y + 4], radius=2, fill=p["bill"], outline=p["bill_shadow"])
    draw.line([(16, bill_y), (20, bill_y)], fill=p["bill_light"])

    # Floating heart above head
    heart_y = 9 - (step * 2)
    heart_color = (255, 80, 120, 240)
    def draw_heart(hx, hy):
        draw.point((hx + 1, hy), fill=heart_color)
        draw.point((hx + 3, hy), fill=heart_color)
        draw.line([(hx, hy + 1), (hx + 4, hy + 1)], fill=heart_color)
        draw.line([(hx + 1, hy + 2), (hx + 3, hy + 2)], fill=heart_color)
        draw.point((hx + 2, hy + 3), fill=heart_color)

    draw_heart(16, max(1, heart_y))

    return img


def generate_all_sprites(output_dir="assets/sprites/paperella", scale=3, palettes=None):
    """
    Generates all sprite frames for duck palettes, scaled up with NEAREST filter.
    Includes: idle (4), walk_right (4), walk_left (4), eat (4), sleep (4), drag (4), pet (4).
    """
    os.makedirs(output_dir, exist_ok=True)
    target_palettes = palettes if palettes else PALETTES.keys()

    for pkey in target_palettes:
        if pkey not in PALETTES:
            print(f"[ATTENZIONE] Palette '{pkey}' non riconosciuta, saltata.")
            continue

        palette = PALETTES[pkey]
        pal_dir = os.path.join(output_dir, pkey)
        os.makedirs(pal_dir, exist_ok=True)

        # 1. Idle (4 frames)
        for i in range(4):
            f = render_idle_frame(palette, i)
            f_scaled = f.resize((f.width * scale, f.height * scale), RESAMPLE_FILTER)
            f_scaled.save(os.path.join(pal_dir, f"idle_{i}.png"))

        # 2. Walk (4 frames right + 4 frames left)
        for i in range(4):
            f_right = render_walk_frame(palette, i)
            f_right_scaled = f_right.resize((f_right.width * scale, f_right.height * scale), RESAMPLE_FILTER)
            f_right_scaled.save(os.path.join(pal_dir, f"walk_right_{i}.png"))

            # Flip for left walk
            f_left = f_right.transpose(FLIP_HORIZONTAL)
            f_left_scaled = f_left.resize((f_left.width * scale, f_left.height * scale), RESAMPLE_FILTER)
            f_left_scaled.save(os.path.join(pal_dir, f"walk_left_{i}.png"))

        # 3. Eat (4 frames)
        for i in range(4):
            f = render_eat_frame(palette, i)
            f_scaled = f.resize((f.width * scale, f.height * scale), RESAMPLE_FILTER)
            f_scaled.save(os.path.join(pal_dir, f"eat_{i}.png"))

        # 4. Sleep (4 frames)
        for i in range(4):
            f = render_sleep_frame(palette, i)
            f_scaled = f.resize((f.width * scale, f.height * scale), RESAMPLE_FILTER)
            f_scaled.save(os.path.join(pal_dir, f"sleep_{i}.png"))

        # 5. Dragged / Picked Up (4 frames)
        for i in range(4):
            f = render_drag_frame(palette, i)
            f_scaled = f.resize((f.width * scale, f.height * scale), RESAMPLE_FILTER)
            f_scaled.save(os.path.join(pal_dir, f"drag_{i}.png"))

        # 6. Pet / Love (4 frames)
        for i in range(4):
            f = render_pet_frame(palette, i)
            f_scaled = f.resize((f.width * scale, f.height * scale), RESAMPLE_FILTER)
            f_scaled.save(os.path.join(pal_dir, f"pet_{i}.png"))

        print(f"[OK] Sprite generati per palette duck: {pkey} ({palette['name']}) -> {pal_dir}")


def generate_preview(output_path="assets/ducks_preview.png", scale=3, palettes=None):
    """Generates a composite preview sheet showing all animations for all duck palettes."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    target_palettes = [k for k in (palettes if palettes else PALETTES.keys()) if k in PALETTES]

    anim_funcs = [
        ("idle", render_idle_frame),
        ("walk", render_walk_frame),
        ("eat", render_eat_frame),
        ("sleep", render_sleep_frame),
        ("drag", render_drag_frame),
        ("pet", render_pet_frame),
    ]

    total_rows = len(target_palettes) * len(anim_funcs)
    sheet_w = 36 * 4 * scale
    sheet_h = 36 * total_rows * scale

    preview = Image.new("RGBA", (sheet_w, sheet_h), (242, 245, 250, 255))

    for p_idx, pkey in enumerate(target_palettes):
        p = PALETTES[pkey]
        for row_idx, (anim_name, func) in enumerate(anim_funcs):
            for col_idx in range(4):
                f = func(p, col_idx)
                f_sc = f.resize((36 * scale, 36 * scale), RESAMPLE_FILTER)
                y_offset = (p_idx * len(anim_funcs) + row_idx) * 36 * scale
                x_offset = col_idx * 36 * scale
                preview.paste(f_sc, (x_offset, y_offset), f_sc)

    preview.save(output_path)
    print(f"[OK] Immagine preview generata con successo: {output_path}")


def generate_icons(output_png="assets/duck_icon.png", output_ico="assets/duck_icon.ico", palette="papera_bianca"):
    """Generates crisp duck icons for the application and Windows executables."""
    os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
    p = PALETTES.get(palette, PALETTES["papera_bianca"])
    frame = render_idle_frame(p, step=0)

    icon_img = frame.resize((256, 256), RESAMPLE_FILTER)
    icon_img.save(output_png)

    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    icon_img.save(output_ico, format="ICO", sizes=icon_sizes)
    print(f"[OK] Icone paperella generate: {output_png} e {output_ico}")


def main():
    parser = argparse.ArgumentParser(description="Sprite builder per deliziose paperelle animate (pixel art).")
    parser.add_argument(
        "--output-dir", "-o",
        default="assets/sprites/paperella",
        help="Cartella di destinazione degli sprite generati (default: assets/sprites/paperella)"
    )
    parser.add_argument(
        "--scale", "-s",
        type=int,
        default=3,
        help="Fattore di scala dei pixel con filtro nearest neighbor (default: 3, 36x36 -> 108x108)"
    )
    parser.add_argument(
        "--palettes", "-p",
        nargs="+",
        choices=list(PALETTES.keys()),
        help="Specifica solo determinate palette da generare (default: tutte)"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Genera anche l'immagine di anteprima complessiva 'assets/ducks_preview.png'"
    )

    args = parser.parse_args()

    print("=" * 65)
    print("🦆 DUCK SPRITE BUILDER - Generatore Sprite Paperelle Pixel Art")
    print("=" * 65)
    print(f"Destinazione: {args.output_dir}")
    print(f"Scala:        {args.scale}x ({36*args.scale}x{36*args.scale} px)")
    print(f"Palette:      {', '.join(args.palettes if args.palettes else PALETTES.keys())}")
    print("-" * 65)

    generate_all_sprites(output_dir=args.output_dir, scale=args.scale, palettes=args.palettes)

    # Ensure duck icons are generated in assets/
    if not os.path.exists("assets/duck_icon.png") or not os.path.exists("assets/duck_icon.ico"):
        generate_icons()

    if args.preview:
        preview_file = "assets/ducks_preview.png"
        generate_preview(output_path=preview_file, scale=args.scale, palettes=args.palettes)

    print("=" * 65)
    print("✨ Paperelle create con successo! Quack! 🦆💛⚪")
    print("=" * 65)


if __name__ == "__main__":
    main()
