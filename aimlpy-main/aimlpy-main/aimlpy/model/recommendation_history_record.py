from sqlalchemy import Column, Integer, String, Float, DateTime, func

from aimlpy.repo.datasource import Base


class RecommendationHistoryRecord(Base):
    __tablename__ = 'recommendation_history'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    item_id = Column(Integer, index=True)  # typically a note_id or external item id
    rec_type = Column(String)  # e.g., 'personalized', 'trending', 'category', 'reminder'
    score = Column(Float)
    reason = Column(String)
    created_at = Column(DateTime, default=func.now())
