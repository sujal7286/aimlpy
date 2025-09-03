from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

from aimlpy.repo.datasource import Base
from aimlpy.model.note_record import NoteRecord
from aimlpy.model.user_record import UserRecord


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")


DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)

# ensure new tables are imported so metadata knows about them
from aimlpy.model.recommendation_history_record import RecommendationHistoryRecord
from aimlpy.model.recommendation_feedback_record import RecommendationFeedbackRecord
