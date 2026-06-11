import sqlite3


DATABASE = "hitl.db"


def initialize_db():

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()

    cursor.execute(

        """
        CREATE TABLE IF NOT EXISTS
        hitl_tasks (

            task_id TEXT PRIMARY KEY,

            query TEXT,

            response TEXT,

            confidence_score REAL,

            status TEXT
        )
        """
    )

    connection.commit()

    connection.close()


initialize_db()