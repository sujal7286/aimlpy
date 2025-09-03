from sqlalchemy import Column, Integer, String, DateTime, func

from aimlpy.repo.datasource import Base


class RecommendationFeedbackRecord(Base):
    __tablename__ = 'recommendation_feedback'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    recommendation_id = Column(Integer, index=True)  # FK to recommendation_history.id (not enforced for simplicity)
    feedback = Column(String)  # 'positive' or 'negative'
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
