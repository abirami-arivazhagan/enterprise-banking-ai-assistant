import sqlite3
from uuid import uuid4

from hitl.store import (
    DATABASE
)


class HITLManager:

    def create_review_task(
        self,
        payload
    ):

        task = {
            "task_id":
            str(uuid4()),

            "query":
            payload.get(
                "query",
                ""
            ),

            "response":
            payload.get(
                "response",
                ""
            ),

            "confidence_score":
            payload.get(
                "confidence_score",
                0.0
            ),

            "status":
            "pending"
        }

        with sqlite3.connect(DATABASE) as connection:

            connection.execute(

                """
                INSERT INTO hitl_tasks (
                    task_id,
                    query,
                    response,
                    confidence_score,
                    status
                )
                VALUES (?, ?, ?, ?, ?)
                """,

                (
                    task["task_id"],
                    task["query"],
                    task["response"],
                    task["confidence_score"],
                    task["status"]
                )
            )

        return task

    def get_pending_tasks(self):

        with sqlite3.connect(DATABASE) as connection:

            connection.row_factory = sqlite3.Row

            rows = connection.execute(

                """
                SELECT
                    task_id,
                    query,
                    response,
                    confidence_score,
                    status
                FROM hitl_tasks
                WHERE status = ?
                ORDER BY rowid DESC
                """,

                ("pending",)
            ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    def review_task(
        self,
        task_id,
        decision
    ):

        with sqlite3.connect(DATABASE) as connection:

            cursor = connection.execute(

                """
                UPDATE hitl_tasks
                SET status = ?
                WHERE task_id = ?
                """,

                (
                    decision,
                    task_id
                )
            )

        return {
            "task_id":
            task_id,

            "status":
            decision,

            "updated":
            cursor.rowcount > 0
        }
