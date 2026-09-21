from app.database.connection import engine
from app.models.database_models import Base


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    initialize_database()
    print("Database tables initialized successfully.")