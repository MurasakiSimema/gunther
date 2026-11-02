"""
Animal species registry and theming architecture.
Allows adding new desktop companion species (e.g. criceti, paperelle, gatti, conigli)
with distinct identities, menu actions, messages, palettes, and build configurations.
"""

from dataclasses import dataclass, field
import os
import json
from gunther.messages import HAMSTER_MESSAGES, DUCK_MESSAGES, get_messages_for_species
from gunther.utils import get_resource_path


@dataclass
class SpeciesConfig:
    id: str                            # Unique identifier: 'criceto', 'paperella', etc.
    name: str                          # Name of species: 'Criceto', 'Paperella'
    emoji: str                         # '🐹', '🦆'
    default_pet_name: str              # 'Gunther', 'Paperella'
    default_palette: str               # 'gunther', 'papera_bianca'
    sprites_folder: str                # 'criceto', 'paperella'
    palette_menu_title: str            # '🎨 Manto del Criceto', '🎨 Piumaggio della Paperella'
    
    # Action and UI text templates (supports {name} placeholder)
    app_title: str = "{name} Desktop Companion"
    app_id: str = "companion.desktop.1.0"
    tray_tooltip: str = "{name} {emoji}❤️"
    initial_greeting: str = "Ciao! Sono {name}! {emoji}❤️"
    feed_action: str = "🌻 Dai un semino a {name}"
    pet_action: str = "🐾 Fai una coccola a {name}"
    sleep_action: str = "💤 Fai fare un pisolino"
    wake_action: str = "☀️ Sveglia {name}"
    thought_action: str = "💬 Cosa stai pensando?"
    bring_action: str = "{emoji} Riporta {name} qui"
    exit_action: str = "👋 Saluta {name} (Esci)"
    roam_action: str = "🚶 Cammina liberamente"
    show_thoughts_action: str = "💭 Mostra pensieri dolci"
    
    # Icons (relative to assets/)
    icon_png: str = "icon.png"
    icon_ico: str = "icon.ico"
    
    # Palette display names map
    palette_names: dict[str, str] = field(default_factory=dict)
    
    # Thought messages
    messages: list[str] = field(default_factory=list)


SPECIES_REGISTRY: dict[str, SpeciesConfig] = {
    "criceto": SpeciesConfig(
        id="criceto",
        name="Criceto",
        emoji="🐹",
        default_pet_name="Gunther",
        default_palette="gunther",
        sprites_folder="criceto",
        palette_menu_title="🎨 Manto del Criceto",
        app_title="Gunther Desktop Companion",
        app_id="gunther.desktop.companion.1.0",
        tray_tooltip="Gunther il Criceto 🐹❤️",
        initial_greeting="Ciao! Sono Gunther! 🐹❤️",
        feed_action="🌻 Dai un semino a {name}",
        pet_action="🐾 Fai una coccola a {name}",
        sleep_action="💤 Fai fare un pisolino",
        wake_action="☀️ Sveglia {name}",
        thought_action="💬 Cosa stai pensando?",
        bring_action="🐹 Riporta {name} qui",
        exit_action="👋 Saluta {name} (Esci)",
        icon_png="icon.png",
        icon_ico="icon.ico",
        palette_names={
            "gunther": "Gunther (Grigio Scuro Originale) 🐹",
            "dorato": "Dorato Classico (Siriano) 🌰",
            "invernale": "Bianco Invernale (Snow) ❄️",
            "zaffiro": "Grigio Zaffiro (Russo) 🪨",
            "panda": "Panda Pezzato 🐼",
        },
        messages=HAMSTER_MESSAGES
    ),
    "paperella": SpeciesConfig(
        id="paperella",
        name="Paperella",
        emoji="🦆",
        default_pet_name="Paperella",
        default_palette="papera_bianca",
        sprites_folder="paperella",
        palette_menu_title="🎨 Piumaggio della Paperella",
        app_title="Paperella Desktop Companion",
        app_id="duck.desktop.companion.1.0",
        tray_tooltip="Paperella da Scrivania 🦆❤️",
        initial_greeting="Quack! Ciao, sono la tua {name}! 🦆❤️",
        feed_action="🥬 Dai un pisellino a {name}",
        pet_action="🪶 Accarezza le piumette di {name}",
        sleep_action="💤 Fai fare un pisolino",
        wake_action="☀️ Sveglia {name}",
        thought_action="💬 A cosa stai quackando?",
        bring_action="🦆 Riporta {name} qui",
        exit_action="👋 Saluta {name} (Esci)",
        icon_png="duck_icon.png",
        icon_ico="duck_icon.ico",
        palette_names={
            "papera_bianca": "Paperella Bianca (Pekin) 🦆⚪",
            "papera_gialla": "Paperella Gialla Classica 🐥💛",
            "papera_germano": "Germano Reale 🦆🌿",
            "papera_rosa": "Paperella Rosa Pastello 🦆🌸",
            "papera_menta": "Paperella Verde Menta 🦆🍃",
            "papera_cioccolato": "Paperella Cioccolato 🦆🍫",
        },
        messages=DUCK_MESSAGES
    )
}


def register_species(config: SpeciesConfig):
    """Registers a new animal species into the system, making future extensions trivial."""
    SPECIES_REGISTRY[config.id] = config


def get_species(species_id: str) -> SpeciesConfig:
    """Returns the SpeciesConfig for a given ID, defaulting to 'criceto'."""
    return SPECIES_REGISTRY.get(species_id, SPECIES_REGISTRY["criceto"])


def get_species_for_palette(palette_key: str) -> SpeciesConfig:
    """Determines which species owns a given palette key."""
    if not palette_key:
        return SPECIES_REGISTRY["criceto"]

    # Check prefix or registered palette names
    for sp in SPECIES_REGISTRY.values():
        if palette_key in sp.palette_names or palette_key == sp.default_palette:
            return sp
        if palette_key.startswith(f"{sp.id}/") or palette_key.startswith(f"{sp.sprites_folder}/"):
            return sp
        if sp.id == "paperella" and palette_key.startswith("papera_"):
            return sp

    return SPECIES_REGISTRY["criceto"]


def load_build_metadata() -> dict:
    """Loads optional build metadata if packaged with the build."""
    meta_path = get_resource_path(os.path.join("assets", "metadata.json"))
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def detect_initial_species() -> tuple[SpeciesConfig, str, str]:
    """
    Detects the initial species, default pet name, and default palette.
    Considers build metadata, available sprite directories, and fallbacks.
    Returns: (SpeciesConfig, default_name, default_palette)
    """
    meta = load_build_metadata()
    if meta and "species" in meta:
        sp = get_species(meta["species"])
        name = meta.get("default_name", sp.default_pet_name)
        pal = meta.get("default_palette", sp.default_palette)
        return sp, name, pal

    # Check available sprite directories
    base_dir = get_resource_path(os.path.join("assets", "sprites"))
    if os.path.exists(base_dir):
        available_folders = [
            d for d in os.listdir(base_dir)
            if os.path.isdir(os.path.join(base_dir, d))
        ]
        # If ONLY paperella exists, start as paperella
        if "paperella" in available_folders and "criceto" not in available_folders:
            sp = SPECIES_REGISTRY["paperella"]
            return sp, sp.default_pet_name, sp.default_palette

    # Default to criceto
    sp = SPECIES_REGISTRY["criceto"]
    return sp, sp.default_pet_name, sp.default_palette
