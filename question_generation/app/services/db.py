import psycopg2
from psycopg2.extras import Json
from contextlib import contextmanager

class DB:
    def __init__(self, DB_URL: str | None) -> None:
        self.db_url = DB_URL
        if not self.db_url:
            raise ValueError('DB URL not provided')

    @contextmanager
    def _get_conn(self):
        """
        Creates a fresh connection for a single operation 
        and ensures it closes even if errors occur.
        """
        conn = None
        try:
            conn = psycopg2.connect(self.db_url)
            yield conn
            conn.commit()  # Saves the changes (Transaction)
        except Exception as e:
            if conn:
                conn.rollback()  # Undoes changes if error happens
            raise e
        finally:
            if conn:
                conn.close() # Closes connection to prevent leaks

    def update_job_roadmap(self, job_id: str, roadmap_data: list):
        """
        Updates the Job table with the generated roadmap and sets status to OPEN.
        """
        query = """
            UPDATE "Job" 
            SET "roadmap" = %s, 
                "status" = 'OPEN',
                "updatedAt" = NOW()
            WHERE "id" = %s;
        """
        
        # We use the context manager here to get a fresh connection
        with self._get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (Json(roadmap_data), job_id))
                print(f"Database updated for Job {job_id}")