DEFAULT_CONFIG = {
    "name": "Gunther",
    "palette": "gunther",
    "scale": 1.0,  # 1.0 = ~108px, 0.75 = ~81px, 1.25 = ~135px, 1.5 = ~162px
    "always_on_top": True,
    "enable_thoughts": True,
    "thought_interval_sec": 180,
    "sound_enabled": True,
    "gravity_enabled": True,
    "roam_enabled": True
}

_current_config = DEFAULT_CONFIG.copy()

def load_config() -> dict:
    """Returns current in-memory configuration without creating any files on disk."""
    return _current_config.copy()

def save_config(cfg: dict):
    """Updates in-memory configuration purely within the running process."""
    global _current_config
    _current_config.update(cfg)
