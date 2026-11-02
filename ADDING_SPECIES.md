# 🐾 Come aggiungere un nuovo animale

Questa guida spiega come aggiungere una nuova specie al progetto Desktop Companion (es. un gatto, un coniglio, un pinguino...).

Il sistema è progettato per essere esteso **senza toccare la logica principale**: ogni nuovo animale richiede modifiche solo in punti precisi e ben delimitati.

---

## Panoramica dei file coinvolti

```
gunther/
├── messages.py           ← 1. Aggiungi i messaggi/pensieri
├── species.py            ← 2. Registra la SpeciesConfig
├── gatto_sprite_builder.py  ← 3. Crea il generatore di sprite (nuovo file)
build.py                  ← 4. Aggiungi la BUILD_CONFIG
assets/
└── sprites/
    └── gatto/            ← 5. Cartella sprite generata automaticamente
        ├── gatto_tigrato/
        └── gatto_bianco/
```

---

## Step 1 — `gunther/messages.py`

Aggiungi la lista di pensieri/messaggi per il nuovo animale e registrala nel dizionario `MESSAGES_BY_SPECIES`:

```python
GATTO_MESSAGES = [
    "Miao... mi fai una coccola? 🐱",
    "Faccio le fusa solo per te! ✨",
    "Ho trovato un gomitolo... è mio ora. 🧶",
    # ... altri messaggi
]

MESSAGES_BY_SPECIES = {
    "criceto":   HAMSTER_MESSAGES,
    "paperella": DUCK_MESSAGES,
    "gatto":     GATTO_MESSAGES,   # ← aggiungi qui
}
```

---

## Step 2 — `gunther/species.py`

Importa i messaggi e aggiungi una nuova `SpeciesConfig` nel dizionario `SPECIES_REGISTRY`:

```python
from gunther.messages import HAMSTER_MESSAGES, DUCK_MESSAGES, GATTO_MESSAGES  # ← importa

SPECIES_REGISTRY: dict[str, SpeciesConfig] = {
    "criceto":   SpeciesConfig(...),
    "paperella": SpeciesConfig(...),

    # ↓ Aggiungi la nuova specie
    "gatto": SpeciesConfig(
        id="gatto",
        name="Gatto",
        emoji="🐱",
        default_pet_name="Micio",
        default_palette="gatto_tigrato",     # deve corrispondere a una chiave di palette_names
        sprites_folder="gatto",              # nome della cartella in assets/sprites/
        palette_menu_title="🎨 Pelo del Gatto",
        app_title="Gatto Desktop Companion",
        app_id="cat.desktop.companion.1.0",
        icon_png="gatto_icon.png",
        icon_ico="gatto_icon.ico",
        palette_names={
            "gatto_tigrato":  "Tigrato Classico 🐱🌿",
            "gatto_bianco":   "Bianco Neve ⬜",
            "gatto_nero":     "Nero Elegante 🖤",
        },
        messages=GATTO_MESSAGES,
    ),
}
```

> **Nota:** `detect_initial_species()` e `get_species_for_palette()` funzionano automaticamente con qualsiasi specie registrata qui — nessun'altra modifica richiesta al runtime.

---

## Step 3 — `gunther/gatto_sprite_builder.py` *(nuovo file)*

Crea un modulo che generi le sprite pixel-art e le icone per la nuova specie.
Il modulo **deve** esporre almeno:

```python
def generate_all_sprites(output_dir: str) -> None:
    """
    Genera tutte le sprite della specie in output_dir.
    Per ogni palette, crea una sottocartella: output_dir/<palette_key>/
    Ogni sottocartella deve contenere i file PNG delle animazioni:
        idle.png, walk_right.png, walk_left.png, sleep.png, ...
    """
    ...

def generate_icons(output_png: str, output_ico: str) -> None:
    """Genera le icone .png e .ico per l'eseguibile."""
    ...
```

Puoi prendere come riferimento [`gunther/duck_sprite_builder.py`](gunther/duck_sprite_builder.py) o [`gunther/sprite_builder.py`](gunther/sprite_builder.py).

---

## Step 4 — `build.py`

Aggiungi una entry nel dizionario `BUILD_CONFIGS` (all'interno del blocco template già presente nel file):

```python
BUILD_CONFIGS: dict[str, dict] = {
    "gunther":   {...},
    "criceti":   {...},
    "paperelle": {...},

    # ↓ Aggiungi qui
    "gatti": {
        "label":         "🐱 TUTTI I GATTI",
        "exe_name":      "Gatto",
        "copy_sprites":  [("gatto", None)],   # (cartella_specie, sottocartella|None)
        "icons": {
            "src_png":      "gatto_icon.png",
            "src_ico":      "gatto_icon.ico",
            "dst_png":      "gatto_icon.png",
            "dst_ico":      "gatto_icon.ico",
            "also_as_icon": True,              # copia anche come icon.* generico
        },
        "icon_rel":         os.path.join("assets", "gatto_icon.ico"),
        "icon_rel_fallback": os.path.join("assets", "icon.ico"),
        "metadata": {
            "target":          "gatti",
            "species":         "gatto",
            "default_palette": "gatto_tigrato",
            "default_name":    "Micio",
        },
        "sprite_builder": "gunther.gatto_sprite_builder",  # modulo Python da Step 3
        "menu_label":     "Tutti i Gatti (Gatto.exe)",
    },
}
```

> **Questo è tutto.** Il menu interattivo, l'help CLI e il target `all` si aggiornano automaticamente.

---

## Step 5 — Assets

Le sprite vengono generate automaticamente da `generate_all_sprites()` al primo avvio della build.

Se vuoi usare sprite **disegnate a mano** invece di generarle via codice:

1. Crea la cartella `assets/sprites/gatto/<palette_key>/` per ogni palette
2. Inserisci i PNG delle animazioni (stesso schema di `assets/sprites/criceto/gunther/`)
3. Imposta `"sprite_builder": None` in `BUILD_CONFIGS` — la build salterà la generazione

---

## Riepilogo checklist

| # | File | Cosa fare |
|---|------|-----------|
| 1 | `gunther/messages.py` | Aggiungi `GATTO_MESSAGES` e registralo in `MESSAGES_BY_SPECIES` |
| 2 | `gunther/species.py` | Aggiungi `SpeciesConfig` in `SPECIES_REGISTRY` |
| 3 | `gunther/gatto_sprite_builder.py` | Crea il generatore sprite con `generate_all_sprites()` e `generate_icons()` |
| 4 | `build.py` | Aggiungi la entry in `BUILD_CONFIGS` |
| 5 | `assets/sprites/gatto/` | Generata automaticamente dalla build, oppure popolata a mano |

### Comandi build

```bash
# Compila solo il nuovo animale
python build.py --target gatti

# Compila tutti gli animali (incluso il nuovo)
python build.py --target all

# Forza rigenerazione sprite
python build.py --target gatti --rebuild-sprites
```
