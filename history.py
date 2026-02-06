import os
import json

# HISTORY MANAGER
class HistoryManager:
    FILE_PATH = "history.json"

    @staticmethod
    def load():
        if not os.path.exists(HistoryManager.FILE_PATH):
            return []
        try:
            with open(HistoryManager.FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    @staticmethod
    def save(item):
        history = HistoryManager.load()
        history.insert(0, item)
        history = history[:50]
        with open(HistoryManager.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)