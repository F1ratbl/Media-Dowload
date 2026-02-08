from sqlalchemy import Column, String, Integer, DateTime
from app.database import Base
from datetime import datetime

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key = True, index = True)
    task_id = Column(String, unique= True, index = True)
    title = Column(String)
    thumbnail = Column(String)
    type = Column(String)
    url = Column(String)
    file_path = Column(String)
    date = Column(DateTime, default = datetime.now)