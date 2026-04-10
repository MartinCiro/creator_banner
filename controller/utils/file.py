from os import makedirs, path as os_path
from json import load, dump

class FileUtils:

    @staticmethod
    def ensure_dir(path: str):
        makedirs(path, exist_ok=True)

    @staticmethod
    def read_json(path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return load(f)
        except Exception:
            return None

    @staticmethod
    def write_json(path: str, data, indent=4):
        with open(path, "w", encoding="utf-8") as f:
            dump(data, f, ensure_ascii=False, indent=indent)

    @staticmethod
    def exists(path: str) -> bool:
        return os_path.exists(path)
