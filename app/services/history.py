from sqlalchemy.orm import Session
from app.models import History
from datetime import datetime
from app.database import SessionLocal

# HISTORY MANAGER
class HistoryManager:

    @staticmethod
    def load():
        db: Session = SessionLocal()
        try:
            results = db.query(History).order_by(History.date.desc()).limit(50).all()
            history_list = []
            for item in results:
                history_list.append({
                    "id": item.task_id,
                    "title": item.title,
                    "thumbnail": item.thumbnail,
                    "type": item.type,
                    "date": item.date.strftime("%d.%m.%Y %H:%M"), # Tarih formatı
                    "url": item.url,
                    "file_path": item.file_path
                })
            return history_list
        except Exception as e:
            print(f"Error loading history: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def save(item):
        db: Session = SessionLocal()

        new_item = History(
            task_id = item["id"],
            title = item["title"],
            thumbnail = item["thumbnail"],
            type = item["type"],
            url = item["url"],
            file_path = item["file_path"],
            date = datetime.now()
        )
        db.add(new_item)
        db.commit()
        db.close()