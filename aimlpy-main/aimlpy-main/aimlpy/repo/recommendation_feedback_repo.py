from typing import List
from sqlalchemy.orm import Session

from aimlpy.model.recommendation_feedback_record import RecommendationFeedbackRecord
from aimlpy.repo.datasource import DataSource


class RecommendationFeedbackRepo:
    def __init__(self, db: DataSource):
        self.db = db

    def add(self, user_id: int, recommendation_id: int, feedback: str, comment: str | None = None) -> RecommendationFeedbackRecord:
        with self.db.get_session() as session:
            rec = RecommendationFeedbackRecord(user_id=user_id, recommendation_id=recommendation_id, feedback=feedback, comment=comment)
            session.add(rec)
            session.commit()
            session.refresh(rec)
            return rec
