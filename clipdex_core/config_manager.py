import json
import os
from pathlib import Path
from typing import Any, Dict, Union

from .paths import get_user_data_dir

class ConfigManager:
    """Simple JSON-file based configuration manager."""

    DEFAULT_CONFIG: Dict[str, Any] = {
        "trigger_key": "space",  # "space" or "enter"
        "auto_start": False,
    }

    def __init__(self, filepath: Union[str, Path, None] = None) -> None:
        if filepath is None:
            filepath = get_user_data_dir() / "config.json"
        self.filepath: Union[Path, str] = filepath
        self._ensure_file()

    # ---------------------------------------------------------------------
    # Public helpers
    # ---------------------------------------------------------------------
    def get(self, key: str, default: Any = None) -> Any:
        return self._load().get(key, default)

    def set(self, key: str, value: Any) -> None:
        cfg = self._load()
        cfg[key] = value
        self._save(cfg)

    def all(self) -> Dict[str, Any]:
        """Returns the entire configuration dictionary."""
        return self._load()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _ensure_file(self) -> None:
        if not os.path.exists(self.filepath):
            self._save(dict(self.DEFAULT_CONFIG))
        else:
            # Merge any missing defaults without overwriting existing keys
            cfg = self._load()
            updated = False
            for k, v in self.DEFAULT_CONFIG.items():
                if k not in cfg:
                    cfg[k] = v
                    updated = True
            if updated:
                self._save(cfg)

    def _load(self) -> Dict[str, Any]:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return dict(self.DEFAULT_CONFIG)

    def _save(self, cfg: Dict[str, Any]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4, ensure_ascii=False) 