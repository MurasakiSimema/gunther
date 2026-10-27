import argparse
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

def build(gunther_only: bool = False):
    print("=" * 60)
    if gunther_only:
        print("[BUILD] Avvio build di Gunther (SOLO COLORE ORIGINALE GUNTHER)")
    else:
        print("[BUILD] Avvio build di Gunther (TUTTI I COLORI INCLUSI)")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    staging_dir = os.path.join(base_dir, "build_staging")
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)

    if gunther_only:
        # Create staging assets directory with ONLY the gunther palette
        staging_assets = os.path.join(staging_dir, "assets")
        staging_sprites = os.path.join(staging_assets, "sprites", "gunther")
        os.makedirs(staging_sprites, exist_ok=True)

        src_gunther = os.path.join(base_dir, "assets", "sprites", "gunther")
        for item in os.listdir(src_gunther):
            s = os.path.join(src_gunther, item)
            d = os.path.join(staging_sprites, item)
            shutil.copy2(s, d)

        # Copy icon assets
        for icon_file in ["icon.png", "icon.ico"]:
            src_icon = os.path.join(base_dir, "assets", icon_file)
            if os.path.exists(src_icon):
                shutil.copy2(src_icon, os.path.join(staging_assets, icon_file))

        assets_add_data = f"{staging_assets};assets"
    else:
        assets_add_data = "assets;assets"

    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name", "Gunther",
        "--icon", os.path.join("assets", "icon.ico"),
        "--add-data", assets_add_data,
        "main.py"
    ]

    print("\nEsecuzione comando PyInstaller...")
    res = subprocess.run(cmd)

    # Clean up staging
    if os.path.exists(staging_dir):
        try:
            shutil.rmtree(staging_dir)
        except Exception:
            pass

    if res.returncode != 0:
        print("\n[ERRORE] Errore durante la build!")
        sys.exit(res.returncode)

    dist_dir = os.path.join(base_dir, "dist")

    exe_path = os.path.join(dist_dir, "Gunther.exe")
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print("\n" + "=" * 60)
        print("[SUCCESSO] Build completata con successo!")
        print(f"File: {exe_path}")
        print(f"Dimensione: {size_mb:.1f} MB")
        if gunther_only:
            print("Versione: Esclusiva 'Gunther Only' (solo manto originale)")
        else:
            print("Versione: Completa con tutte le varianti di manto")
        print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script di compilazione per Gunther Desktop Companion")
    parser.add_argument(
        "--gunther-only", "-g",
        action="store_true",
        help="Includi solo il manto originale 'gunther' nell'eseguibile (esclude gli altri manti)"
    )
    args = parser.parse_args()
    build(gunther_only=args.gunther_only)
