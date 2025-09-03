from typing import List, Optional
from sqlalchemy.orm import Session

from aimlpy.model.recommendation_history_record import RecommendationHistoryRecord
from aimlpy.repo.datasource import DataSource


class RecommendationHistoryRepo:
    def __init__(self, db: DataSource):
        self.db = db

    def add(self, user_id: int, item_id: int, rec_type: str, score: float = None, reason: str = None) -> RecommendationHistoryRecord:
        with self.db.get_session() as session:
            rec = RecommendationHistoryRecord(user_id=user_id, item_id=item_id, rec_type=rec_type, score=score, reason=reason)
            session.add(rec)
            session.commit()
            session.refresh(rec)
            return rec

    def list_by_user(self, user_id: int, limit: int = 50) -> List[RecommendationHistoryRecord]:
        with self.db.get_session() as session:
            return session.query(RecommendationHistoryRecord).filter(RecommendationHistoryRecord.user_id == user_id)                .order_by(RecommendationHistoryRecord.created_at.desc()).limit(limit).all()
