"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from datetime import datetime, timedelta
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from aimlpy.entity.common import ErrorCode
from aimlpy.entity.recommendation import Recommendation
from aimlpy.entity.recommendation_reqres import GetRecommendationRequest, GetRecommendationResponse
from aimlpy.model.note_record import NoteRecord
from aimlpy.repo.datasource import DataSource
from aimlpy.repo.note_repo import NoteRepo
from aimlpy.repo.recommendation_feedback_repo import RecommendationFeedbackRepo
from aimlpy.repo.recommendation_history_repo import RecommendationHistoryRepo
from aimlpy.util import strutil


class RecommendationService:
    def __init__(self):
        self.db = DataSource()
        self.note_repo = NoteRepo(db=self.db)
        self.history_repo = RecommendationHistoryRepo(db=self.db)
        self.feedback_repo = RecommendationFeedbackRepo(db=self.db)

    # Existing simple stub
    def get_recommendations(self, req: GetRecommendationRequest) -> GetRecommendationResponse:
        # Simple placeholder recommendations
        recommendations: list[Recommendation] = []
        recommendations.append(
            Recommendation(user_id=req.user_id, item_id="1", score=0.9, reason="popular")
        )
        recommendations.append(
            Recommendation(user_id=req.user_id, item_id="2", score=0.8, reason="similar_content")
        )
        res = GetRecommendationResponse(error=False, recommendations=recommendations)
        return res

    # ---- New features ----
    def _extract_tags(self, text: str) -> List[str]:
        """Very simple tag extractor: looks for words prefixed with # and lower-cases them."""
        if not text:
            return []
        return [w[1:].lower() for w in text.split() if w.startswith('#') and len(w) > 1]

    def get_personalized_notes(self, user_id: int, top_k: int = 5):
        """Content-based: find other notes by same user sharing tags/keywords."""
        with self.db.get_session() as session:
            user_notes = session.query(NoteRecord).filter(NoteRecord.user_id == user_id).all()
            if not user_notes:
                return []
            # collect tag frequencies from user's notes
            tag_weights = {}
            for n in user_notes:
                for t in self._extract_tags(n.text):
                    tag_weights[t] = tag_weights.get(t, 0) + 1

            # score all notes (including other users) by tag overlap
            all_notes = session.query(NoteRecord).all()
            scored = []
            for n in all_notes:
                if n.user_id == user_id:
                    continue
                tags = set(self._extract_tags(n.text))
                if not tags:
                    continue
                score = sum(tag_weights.get(t, 0) for t in tags)
                if score > 0:
                    hist = self.history_repo.add(user_id=user_id, item_id=n.note_id, rec_type="personalized", score=float(score), reason="tag_overlap")
                    scored.append({"note_id": n.note_id, "user_id": n.user_id, "text": n.text, "score": float(score), "recommendation_id": hist.id})
            scored.sort(key=lambda x: x["score"], reverse=True)
            return scored[: top_k]

    def get_trending_notes(self, limit: int = 5):
        """Trending by most recently updated notes overall."""
        with self.db.get_session() as session:
            notes = session.query(NoteRecord).order_by(NoteRecord.updated_at.desc()).limit(limit).all()
            return [{"note_id": n.note_id, "user_id": n.user_id, "text": n.text} for n in notes]

    def get_category_recommendations(self, tag: str, limit: int = 10):
        tag = (tag or '').lower()
        with self.db.get_session() as session:
            notes = session.query(NoteRecord).filter(NoteRecord.text.ilike(f"%#{tag}%")).limit(limit).all()
            return [{"note_id": n.note_id, "user_id": n.user_id, "text": n.text} for n in notes]

    def get_review_reminders(self, user_id: int, days_threshold: int = 30, limit: int = 10):
        cutoff = datetime.utcnow() - timedelta(days=days_threshold)
        with self.db.get_session() as session:
            notes = session.query(NoteRecord).filter(NoteRecord.user_id == user_id, NoteRecord.updated_at < cutoff).order_by(NoteRecord.updated_at.asc()).limit(limit).all()
            results = []
            for n in notes:
                hist = self.history_repo.add(user_id=user_id, item_id=n.note_id, rec_type="reminder", score=None, reason=f"older_than_{days_threshold}d")
                results.append({"note_id": n.note_id, "user_id": n.user_id, "text": n.text, "recommendation_id": hist.id})
            return results

    def submit_feedback(self, user_id: int, recommendation_id: int, feedback: str, comment: str | None = None):
        fb = self.feedback_repo.add(user_id=user_id, recommendation_id=recommendation_id, feedback=feedback, comment=comment)
        return {"id": fb.id, "status": "ok"}

    def get_history(self, user_id: int, limit: int = 50):
        items = self.history_repo.list_by_user(user_id=user_id, limit=limit)
        return [{"id": i.id, "item_id": i.item_id, "type": i.rec_type, "score": i.score, "reason": i.reason, "created_at": i.created_at.isoformat() if i.created_at else None} for i in items]
