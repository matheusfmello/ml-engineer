import logging
from typing import List, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base()


class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=func.now())
    model_id = Column(String, nullable=False)
    prediction = Column(Integer)
    probability = Column(Float)


class DatabaseService:
    """
    A service to manage database interactions for predictions.
    """
    def __init__(self, logger: logging.Logger, db_path: str = "database/predictions.db"):
        self.logger = logger
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False, future=True)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        self._initialize_db()

    def _initialize_db(self):
        """Initializes the SQLite database and creates the predictions table."""
        try:
            Base.metadata.create_all(self.engine)
            self.logger.info(f"SQLite database initialized at {self.db_path}")
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            raise

    def insert_prediction(self, model_id: str, prediction: int, probability: float = None):
        """
        Inserts a new prediction record into the database.

        Args:
            model_id (str): The model identifier.
            prediction (int): The predicted value.
            probability (float, optional): The probability associated with the prediction.
            Defaults to None.
        """
        session: Session = self.SessionLocal()
        try:
            pred = Prediction(model_id=model_id, prediction=prediction, probability=probability)
            session.add(pred)
            session.commit()
            self.logger.info("Prediction stored in database.")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error storing prediction in database: {e}")
        finally:
            session.close()

    def get_history(self, model_id) -> List[Dict[str, Any]]:
        """
        Retrieves the prediction history from the SQLite database.

        Returns:
            A list of prediction history records.
        """
        self.logger.info("Retrieving prediction history from database.")
        history_records = []
        session: Session = self.SessionLocal()
        try:
            results = (
                session.query(Prediction)
                .filter_by(model_id=model_id)
                .order_by(Prediction.timestamp.desc())
                .all()
            )
            for row in results:
                history_records.append(
                    {
                        "timestamp": row.timestamp.isoformat() if row.timestamp else None,
                        "model_id": row.model_id,
                        "prediction": row.prediction,
                        "probability": row.probability
                    }
                )
        except Exception as e:
            self.logger.error(f"Error retrieving history from database: {e}")
        finally:
            session.close()

        return history_records
