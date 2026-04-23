from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os
from dotenv import load_dotenv

# 1. Load environment variables from .env file
load_dotenv()

# 2. Define the path to the data directory
#    This will be created inside the backend folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# 3. Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# 4. Construct the full path to the SQLite database file
#    The final path will be like: .../backend/app/data/secure.db
SQLITE_FILE_PATH = os.path.join(DATA_DIR, "secure.db")

# 5. Get the database URL from the environment variable, defaulting to the local file
#    If 'DATABASE_URL' is set in .env (e.g., for PostgreSQL), it will use that instead.
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{SQLITE_FILE_PATH}")

print(f"DEBUG: Using DATABASE_URL: {DATABASE_URL}")


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()