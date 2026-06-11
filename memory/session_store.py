import sqlite3


DATABASE = "memory.db"


def initialize_memory_db():

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()

    cursor.execute(

        """
        CREATE TABLE IF NOT EXISTS
        sessions (

            session_id TEXT,

            query TEXT,

            response TEXT
        )
        """
    )

    connection.commit()

    connection.close()


initialize_memory_db()