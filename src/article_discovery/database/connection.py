import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from article_discovery.database.models import Base
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables created.")
