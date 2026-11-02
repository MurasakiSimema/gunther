"""
Unified Build System for Desktop Companions.
Compiles standalone single-file executables with PyInstaller.

Targets built-in:
    --target gunther     : Solo Gunther (manto originale criceto -> Gunther_Solo.exe)
    --target criceti     : Tutti i criceti (5 manti -> Gunther_Criceti.exe)
    --target paperelle   : Tutte le paperelle (6 varianti -> Paperella.exe)
    --target all         : Tutti gli animali registrati in SPECIES_REGISTRY

Per aggiungere un nuovo animale, vedi ADDING_SPECIES.md.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

# Ensure UTF-8 output on Windows consoles
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

# ---------------------------------------------------------------------------
# BUILD CONFIG REGISTRY
# Ogni entry descrive come fare la build di una specie (o un sottoinsieme).
# Per aggiungere un nuovo animale, aggiungi una entry qui e in SPECIES_REGISTRY
# in gunther/species.py. Nessun altro file va modificato.
# ---------------------------------------------------------------------------

BUILD_CONFIGS: dict[str, dict] = {
    # target_id -> configurazione di build
    "gunther": {
        "label": "🐹 SOLO GUNTHER (Manto Originale Esclusivo)",
        "exe_name": "Gunther_Solo",
        # Lista di (species_folder, palette_subfolder | None) da copiare.
        # None = copia tutta la cartella della specie.
        "copy_sprites": [("criceto", "gunther")],
        "icons": {
            "src_png": "icon.png",
            "src_ico": "icon.ico",
            "dst_png": "icon.png",
            "dst_ico": "icon.ico",
        },
        "icon_rel": os.path.join("assets", "icon.ico"),
        "metadata": {
            "target": "gunther",
            "species": "criceto",
            "default_palette": "gunther",
            "default_name": "Gunther",
            "exclusive_palette": "gunther",
        },
        "sprite_builder": None,   # gestito da ensure_sprites() per compatibilità
        "menu_label": "Solo Gunther (Gunther_Solo.exe)",
    },
    "criceti": {
        "label": "🐹 TUTTI I CRICETI (5 Manti Disponibili)",
        "exe_name": "Gunther_Criceti",
        "copy_sprites": [("criceto", None)],
        "icons": {
            "src_png": "icon.png",
            "src_ico": "icon.ico",
            "dst_png": "icon.png",
            "dst_ico": "icon.ico",
        },
        "icon_rel": os.path.join("assets", "icon.ico"),
        "metadata": {
            "target": "criceti",
            "species": "criceto",
            "default_palette": "gunther",
            "default_name": "Gunther",
        },
        "sprite_builder": None,
        "menu_label": "Tutti i Criceti (Gunther_Criceti.exe)",
    },
    "paperelle": {
        "label": "🦆 TUTTE LE PAPERELLE (6 Varianti + Menu a tema)",
        "exe_name": "Paperella",
        "copy_sprites": [("paperella", None)],
        "icons": {
            "src_png": "duck_icon.png",
            "src_ico": "duck_icon.ico",
            "dst_png": "duck_icon.png",
            "dst_ico": "duck_icon.ico",
            # Anche come icona generica "icon.*" per il tema paperella
            "also_as_icon": True,
        },
        "icon_rel": os.path.join("assets", "duck_icon.ico"),
        "icon_rel_fallback": os.path.join("assets", "icon.ico"),
        "metadata": {
            "target": "paperelle",
            "species": "paperella",
            "default_palette": "papera_bianca",
            "default_name": "Paperella",
        },
        "sprite_builder": None,
        "menu_label": "Tutte le Paperelle (Paperella.exe)",
    },
    # -----------------------------------------------------------------------
    # TEMPLATE: aggiungi qui la build config del tuo nuovo animale.
    # Esempio per un gatto:
    #
    # "gatti": {
    #     "label": "🐱 TUTTI I GATTI",
    #     "exe_name": "Gatto",
    #     "copy_sprites": [("gatto", None)],
    #     "icons": {
    #         "src_png": "gatto_icon.png",
    #         "src_ico": "gatto_icon.ico",
    #         "dst_png": "gatto_icon.png",
    #         "dst_ico": "gatto_icon.ico",
    #         "also_as_icon": True,
    #     },
    #     "icon_rel": os.path.join("assets", "gatto_icon.ico"),
    #     "icon_rel_fallback": os.path.join("assets", "icon.ico"),
    #     "metadata": {
    #         "target": "gatti",
    #         "species": "gatto",
    #         "default_palette": "gatto_tigrato",
    #         "default_name": "Micio",
    #     },
    #     "sprite_builder": "gunther.gatto_sprite_builder",   # modulo Python
    #     "menu_label": "Tutti i Gatti (Gatto.exe)",
    # },
    # -----------------------------------------------------------------------
}

# Target virtuale "all": include tutti i target tranne se stesso
ALL_TARGETS = [k for k in BUILD_CONFIGS]


def _resolve_icon(cfg: dict, base_dir: str) -> str:
    """Returns the absolute path of the icon to use for this build target."""
    icon_rel = cfg.get("icon_rel", os.path.join("assets", "icon.ico"))
    fallback = cfg.get("icon_rel_fallback", os.path.join("assets", "icon.ico"))
    full = os.path.join(base_dir, icon_rel)
    if not os.path.exists(full):
        full = os.path.join(base_dir, fallback)
    return full


def ensure_sprites(target: str, base_dir: str, force: bool = False):
    """
    Ensures sprites and icons are generated for the chosen target.
    Built-in species (criceto, paperella) are handled explicitly for backwards
    compatibility; additional species declare their sprite_builder module in
    BUILD_CONFIGS and this function calls it automatically.
    """
    targets_to_process = ALL_TARGETS if target == "all" else [target]

    for t in targets_to_process:
        cfg = BUILD_CONFIGS.get(t)
        if not cfg:
            continue

        # ---- built-in: criceto ----
        if t in ("gunther", "criceti"):
            criceto_dir = os.path.join(base_dir, "assets", "sprites", "criceto")
            if force or not os.path.exists(criceto_dir) or not os.listdir(criceto_dir):
                print("[SETUP] Generazione sprite criceto...")
                from gunther.sprite_builder import generate_all_sprites as gen_criceti
                gen_criceti(output_dir=criceto_dir)

        # ---- built-in: paperella ----
        elif t == "paperelle":
            paperella_dir = os.path.join(base_dir, "assets", "sprites", "paperella")
            from gunther.duck_sprite_builder import generate_all_sprites as gen_ducks, generate_icons
            if force or not os.path.exists(paperella_dir) or not os.listdir(paperella_dir):
                print("[SETUP] Generazione sprite paperella...")
                gen_ducks(output_dir=paperella_dir)
            duck_png = os.path.join(base_dir, "assets", "duck_icon.png")
            duck_ico = os.path.join(base_dir, "assets", "duck_icon.ico")
            if force or not os.path.exists(duck_png) or not os.path.exists(duck_ico):
                print("[SETUP] Generazione icone paperella...")
                generate_icons(output_png=duck_png, output_ico=duck_ico)

        # ---- nuovo animale: usa sprite_builder dichiarato in BUILD_CONFIGS ----
        elif cfg.get("sprite_builder"):
            import importlib
            mod = importlib.import_module(cfg["sprite_builder"])
            species_folder = cfg["copy_sprites"][0][0]
            species_dir = os.path.join(base_dir, "assets", "sprites", species_folder)
            if force or not os.path.exists(species_dir) or not os.listdir(species_dir):
                print(f"[SETUP] Generazione sprite {species_folder}...")
                mod.generate_all_sprites(output_dir=species_dir)
            # Genera icone se il modulo le supporta
            if hasattr(mod, "generate_icons"):
                icons_cfg = cfg.get("icons", {})
                dst_png = os.path.join(base_dir, "assets", icons_cfg.get("dst_png", "icon.png"))
                dst_ico = os.path.join(base_dir, "assets", icons_cfg.get("dst_ico", "icon.ico"))
                if force or not os.path.exists(dst_png) or not os.path.exists(dst_ico):
                    print(f"[SETUP] Generazione icone {species_folder}...")
                    mod.generate_icons(output_png=dst_png, output_ico=dst_ico)


def _copy_icons(cfg: dict, base_dir: str, staging_assets: str):
    """Copies icon files from assets/ into the staging directory."""
    icons = cfg.get("icons", {})
    src_png = os.path.join(base_dir, "assets", icons.get("src_png", "icon.png"))
    src_ico = os.path.join(base_dir, "assets", icons.get("src_ico", "icon.ico"))
    dst_png = os.path.join(staging_assets, icons.get("dst_png", "icon.png"))
    dst_ico = os.path.join(staging_assets, icons.get("dst_ico", "icon.ico"))

    if os.path.exists(src_png):
        shutil.copy2(src_png, dst_png)
    if os.path.exists(src_ico):
        shutil.copy2(src_ico, dst_ico)

    # Optionally copy also as generic icon.* for species-themed builds
    if icons.get("also_as_icon"):
        if os.path.exists(src_png):
            shutil.copy2(src_png, os.path.join(staging_assets, "icon.png"))
        if os.path.exists(src_ico):
            shutil.copy2(src_ico, os.path.join(staging_assets, "icon.ico"))


def prepare_staging(target: str, base_dir: str, staging_dir: str, custom_name: str = None) -> tuple[str, str, str]:
    """
    Prepares a clean staging directory with only the necessary assets and metadata for the target.
    Returns: (staging_assets_dir, exe_name, icon_absolute_path)

    For target == 'all', copies sprites from all registered BUILD_CONFIGS and
    uses a generic metadata (default: criceto).
    """
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir, ignore_errors=True)

    staging_assets = os.path.join(staging_dir, "assets")
    os.makedirs(staging_assets, exist_ok=True)
    staging_sprites = os.path.join(staging_assets, "sprites")
    os.makedirs(staging_sprites, exist_ok=True)

    if target == "all":
        exe_name = custom_name or "Gunther_Completo"

        # Copy all species sprites
        for t, cfg in BUILD_CONFIGS.items():
            for species_folder, palette_sub in cfg["copy_sprites"]:
                if palette_sub:
                    src = os.path.join(base_dir, "assets", "sprites", species_folder, palette_sub)
                    dst = os.path.join(staging_sprites, species_folder, palette_sub)
                else:
                    src = os.path.join(base_dir, "assets", "sprites", species_folder)
                    dst = os.path.join(staging_sprites, species_folder)
                if os.path.exists(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)

        # Copy all asset files (icons, etc.)
        for item in os.listdir(os.path.join(base_dir, "assets")):
            src = os.path.join(base_dir, "assets", item)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(staging_assets, item))

        metadata = {
            "target": "all",
            "species": "criceto",
            "default_palette": "gunther",
            "default_name": "Gunther",
        }
        icon_full = os.path.join(base_dir, "assets", "icon.ico")

    else:
        cfg = BUILD_CONFIGS[target]
        exe_name = custom_name or cfg["exe_name"]

        # Copy required sprite directories
        for species_folder, palette_sub in cfg["copy_sprites"]:
            if palette_sub:
                src = os.path.join(base_dir, "assets", "sprites", species_folder, palette_sub)
                dst = os.path.join(staging_sprites, species_folder, palette_sub)
            else:
                src = os.path.join(base_dir, "assets", "sprites", species_folder)
                dst = os.path.join(staging_sprites, species_folder)
            if os.path.exists(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)

        # Copy icons
        _copy_icons(cfg, base_dir, staging_assets)

        metadata = cfg["metadata"].copy()
        icon_full = _resolve_icon(cfg, base_dir)

    # Write metadata into staged assets
    with open(os.path.join(staging_assets, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return staging_assets, exe_name, icon_full


def run_pyinstaller(cmd: list[str]):
    """Attempts running PyInstaller through sys.executable or system PATH."""
    try:
        return subprocess.run(cmd)
    except FileNotFoundError:
        cmd_fallback = ["pyinstaller"] + cmd[3:]
        return subprocess.run(cmd_fallback)


def build(target: str = "gunther", custom_name: str = None, rebuild_sprites: bool = False):
    """Main build entry point."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    # Normalize target aliases
    target = target.lower().strip().replace("-", "_")
    target_aliases: dict[str, str] = {
        "solo_gunther": "gunther",
        "gunther_only": "gunther",
        "criceto": "criceti",
        "hamsters": "criceti",
        "hamster": "criceti",
        "paperella": "paperelle",
        "papere": "paperelle",
        "duck": "paperelle",
        "ducks": "paperelle",
        "tutti": "all",
        "completo": "all",
    }
    # Also auto-map <species_id> -> <build_target> for any registered target
    for t in BUILD_CONFIGS:
        target_aliases.setdefault(t, t)
    target = target_aliases.get(target, target)

    if target != "all" and target not in BUILD_CONFIGS:
        print(f"[ERRORE] Target sconosciuto: '{target}'")
        print(f"         Target disponibili: {', '.join(list(BUILD_CONFIGS.keys()) + ['all'])}")
        sys.exit(1)

    label = (
        "✨ TUTTI GLI ANIMALI (" + ", ".join(cfg["exe_name"] for cfg in BUILD_CONFIGS.values()) + ")"
        if target == "all"
        else BUILD_CONFIGS[target]["label"]
    )

    print("=" * 65)
    print(f"[BUILD] Avvio build: {label}")
    print("=" * 65)

    # 1. Ensure required sprites and icons exist (regenerate if forced or missing)
    ensure_sprites(target, base_dir, force=rebuild_sprites)

    # 2. Setup clean staging
    staging_dir = os.path.join(base_dir, "build_staging")
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir, ignore_errors=True)

    staging_assets, exe_name, icon_full = prepare_staging(
        target, base_dir, staging_dir, custom_name=custom_name
    )
    assets_add_data = f"{staging_assets};assets"

    # 3. Assemble PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name", exe_name,
        "--icon", icon_full,
        "--add-data", assets_add_data,
        "main.py"
    ]

    print("\nEsecuzione comando PyInstaller...")
    print(f"Eseguibile target: {exe_name}.exe")
    print(f"Icona usata:       {icon_full}")

    res = run_pyinstaller(cmd)

    # Clean up staging
    if os.path.exists(staging_dir):
        try:
            shutil.rmtree(staging_dir, ignore_errors=True)
        except Exception:
            pass

    if res.returncode != 0:
        print("\n[ERRORE] Errore durante la build!")
        sys.exit(res.returncode)

    dist_dir = os.path.join(base_dir, "dist")
    exe_path = os.path.join(dist_dir, f"{exe_name}.exe")

    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print("\n" + "=" * 65)
        print("[SUCCESSO] Build completata con successo!")
        print(f"File generato: {exe_path}")
        print(f"Dimensione:    {size_mb:.1f} MB")
        print(f"Modalità:      {label}")
        print("=" * 65)


def parse_args():
    # Build dynamic list of valid targets for --target choices and help text
    valid_targets = list(BUILD_CONFIGS.keys()) + ["all"]
    target_help = (
        "Target da compilare. Disponibili: "
        + ", ".join(f"'{t}'" for t in valid_targets)
        + ". 'all' compila tutti gli animali."
    )

    parser = argparse.ArgumentParser(
        description="Script di compilazione unificato per Desktop Companion"
    )
    parser.add_argument(
        "--target", "-t",
        choices=valid_targets,
        default=None,
        help=target_help,
    )
    parser.add_argument(
        "--name", "-n",
        default=None,
        help="Nome personalizzato per l'eseguibile (senza estensione .exe)",
    )
    parser.add_argument(
        "--rebuild-sprites",
        action="store_true",
        help="Forza la rigenerazione degli sprite e delle icone prima della compilazione",
    )
    parser.add_argument("--gunther-only", "-g", action="store_true", help="Scorciatoia per --target gunther")

    args = parser.parse_args()

    # Determine target from flags
    target = None
    if args.gunther_only:
        target = "gunther"
    elif args.target:
        target = args.target

    if target:
        return target, args.name, args.rebuild_sprites

    # Interactive menu if executed without arguments in a terminal
    if sys.stdin and hasattr(sys.stdin, "isatty") and sys.stdin.isatty():
        menu_entries = {str(i + 1): t for i, t in enumerate(BUILD_CONFIGS.keys())}
        all_idx = str(len(BUILD_CONFIGS) + 1)
        menu_entries[all_idx] = "all"

        print("=" * 60)
        print("     DESKTOP COMPANION - MENU DI COMPILAZIONE")
        print("=" * 60)
        print(" Scegli cosa compilare:")
        for idx, t in menu_entries.items():
            if t == "all":
                print(f"   [{idx}] Tutti gli Animali")
            else:
                label = BUILD_CONFIGS[t].get("menu_label", t)
                print(f"   [{idx}] {label}")
        print("=" * 60)
        choice = input(f"Digita 1-{all_idx} [default: 1]: ").strip()
        target = menu_entries.get(choice, list(BUILD_CONFIGS.keys())[0])
        return target, args.name, args.rebuild_sprites

    return list(BUILD_CONFIGS.keys())[0], args.name, args.rebuild_sprites


if __name__ == "__main__":
    chosen_target, custom_name, rebuild_sprites = parse_args()
    build(target=chosen_target, custom_name=custom_name, rebuild_sprites=rebuild_sprites)
