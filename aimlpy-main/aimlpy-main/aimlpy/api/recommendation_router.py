"""
-- Created by: Ashok Kumar Pant
-- Email: asokpant@gmail.com
-- Created on: 04/05/2025
"""
from fastapi import APIRouter, Query
from pydantic import BaseModel

from aimlpy.entity.common import ErrorCode
from aimlpy.entity.recommendation_reqres import GetRecommendationResponse, GetRecommendationRequest
from aimlpy.service.recommendation_service import RecommendationService
from aimlpy.util import loggerutil

logger = loggerutil.get_logger(__name__)

router = APIRouter(tags=["Recommendation"])

service = RecommendationService()


@router.get("/ml/recommend", response_model=GetRecommendationResponse)
async def get_recommendation(user_id: str, top_n: int = 10):
    try:
        req = GetRecommendationRequest(user_id=user_id, top_k=top_n)
        res = service.get_recommendations(req)
        return res
    except Exception as e:
        logger.exception(f"Error: {e}")
        return GetRecommendationResponse(error=True, error_code=ErrorCode.INTERNAL_SERVER_ERROR, message=str(e))


class FeedbackRequest(BaseModel):
    user_id: int
    recommendation_id: int
    feedback: str  # 'positive' or 'negative'
    comment: str | None = None


@router.get("/recommendations/notes")
async def personalized_notes(user_id: int = Query(...), top_k: int = Query(5)):
    return {"items": service.get_personalized_notes(user_id=user_id, top_k=top_k)}


@router.get("/recommendations/trending")
async def trending_notes(limit: int = Query(5)):
    return {"items": service.get_trending_notes(limit=limit)}


@router.get("/recommendations/category")
async def category_recs(tag: str = Query(...), limit: int = Query(10)):
    return {"items": service.get_category_recommendations(tag=tag, limit=limit)}


@router.get("/recommendations/reminders")
async def review_reminders(user_id: int = Query(...), days: int = Query(30), limit: int = Query(10)):
    return {"items": service.get_review_reminders(user_id=user_id, days_threshold=days, limit=limit)}


@router.post("/recommendations/feedback")
async def add_feedback(body: FeedbackRequest):
    return service.submit_feedback(user_id=body.user_id, recommendation_id=body.recommendation_id, feedback=body.feedback, comment=body.comment)


@router.get("/recommendations/history")
async def rec_history(user_id: int = Query(...), limit: int = Query(50)):
    return {"items": service.get_history(user_id=user_id, limit=limit)}
