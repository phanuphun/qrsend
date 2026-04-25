import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config.json")
CONFIG_PATH = os.path.normpath(CONFIG_PATH)

DEFAULTS = {
    "camera_index": 0,
    "com0com_path": r"C:\Program Files (x86)\com0com\setupc.exe",
}


def loadConfig() -> dict:
    if not os.path.exists(CONFIG_PATH):
        return DEFAULTS.copy()
    try:
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
        return {**DEFAULTS, **data}
    except Exception:
        return DEFAULTS.copy()


def saveConfig(data: dict):
    current = loadConfig()
    current.update(data)
    with open(CONFIG_PATH, "w") as f:
        json.dump(current, f, indent=2)
    print(f"Config saved → {CONFIG_PATH}")


def getCameraIndex() -> int:
    return loadConfig().get("camera_index", 0)


def setCameraIndex(index: int):
    saveConfig({"camera_index": index})
    print(f"Camera index set to {index}")


def getCom0comPath() -> str:
    return loadConfig().get("com0com_path", r"C:\Program Files (x86)\com0com\setupc.exe")


def setCom0comPath(path: str):
    saveConfig({"com0com_path": path})
    print(f"com0com path set to {path}")
