import logging
import sqlite3
from typing import List, Dict, Any
import json 

class DatabaseService:
    """
    A service to manage database interactions for predictions.
    """
    def __init__(self, logger: logging.Logger, db_path: str = "database/predictions.db"):
        self.logger = logger
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Initializes the SQLite database and creates the predictions table."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    model_id TEXT NOT NULL,
                    prediction INTEGER,
                    probability REAL
                )
            """)
            conn.commit()
            conn.close()
            self.logger.info(f"SQLite database initialized at {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Error initializing database: {e}")
            raise

    def insert_prediction(self, model_id: str, prediction: int, probability: float = None):
        """
        Inserts a new prediction record into the database.

        Args:
            model_id (Dict[str, Any]): The input data used for prediction.
            prediction (int): The predicted value.
            probability (float, optional): The probability associated with the prediction. Defaults to None.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO predictions (model_id, prediction, probability) VALUES (?, ?, ?)",
                (model_id, prediction, probability)
            )
            conn.commit()
            conn.close()
            self.logger.info("Prediction stored in database.")
        except sqlite3.Error as e:
            self.logger.error(f"Error storing prediction in database: {e}")

    def get_history(self, model_id) -> List[Dict[str, Any]]:
        """
        Retrieves the prediction history from the SQLite database.

        Returns:
            A list of prediction history records.
        """
        self.logger.info("Retrieving prediction history from database.")
        history_records = []
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT timestamp, model_id, prediction, probability
                FROM predictions
                WHERE model_id = ?
                ORDER BY timestamp DESC
                """,
                (model_id,)
            )
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                timestamp, model_id, prediction, probability = row
                history_records.append(
                    {
                        "timestamp": timestamp,
                        "model_id": model_id,
                        "prediction": prediction,
                        "probability": probability
                    }
                )
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving history from database: {e}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from database history: {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while getting history: {e}")

        return history_records
