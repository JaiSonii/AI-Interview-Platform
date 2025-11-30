import redis
import json
import os
from app.services.question_generator import QuestionGenerator
from app.services.db import DB
from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(host='localhost', port=6379, db=0)
db = DB(os.getenv('DATABASE_URL'))
generator = QuestionGenerator()

def process_jobs():
    print("Worker started. Waiting for jobs...")
    try:
        while True:
            item = r.blpop(['job_queue'], timeout=1)  # <-- timeout needed
            if not item:
                continue

            _, raw_data = item #type:ignore
            job_data = json.loads(raw_data)
            print(f"Processing Job: {job_data['job_id']}")

            try:
                result = generator.invoke(
                    role=job_data['role'], 
                    exp_range=job_data['exp_range'], 
                    description=job_data['description']
                )
                roadmap_json = [topic.model_dump() for topic in result.roadmap] #type:ignore
                print(roadmap_json)
                db.update_job_roadmap(job_data['job_id'], roadmap_data=roadmap_json)

            except Exception as e:
                print(f"Failed to process job: {e}")

    except KeyboardInterrupt:
        print("\nShutting down worker gracefully...")
