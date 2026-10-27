import sys
import os

def get_base_dir() -> str:
    """Returns the directory of the running script or .exe"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_bundle_dir() -> str:
    """Returns PyInstaller bundle dir (_MEIPASS) or source dir"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_resource_path(relative_path: str) -> str:
    """Gets absolute path to resource, works for dev and for PyInstaller bundle"""
    base = get_bundle_dir()
    return os.path.join(base, relative_path)

def get_user_data_path(file_name: str) -> str:
    """Gets path to user-editable file next to executable/project"""
    base = get_base_dir()
    return os.path.join(base, file_name)
