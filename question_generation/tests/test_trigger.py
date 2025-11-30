import redis
import json
import uuid

# Connect to the SAME Redis instance
r = redis.Redis(host='localhost', port=6379, db=0)

# 1. Create a Fake Job Payload (Simulating what Node.js sends)
fake_job_id = "e0280d16-0f5c-4ca2-b976-762372be9e3d" # Generate a random UUID
payload = {
    "job_id": fake_job_id,
    "role": "Senior Python Developer",
    "exp_range": {"min_exp": 3, "max_exp": 5},
    "description": "We need a python expert with Django and AWS experience. Must know System Design."
}

# 2. Push to the Queue
print(f"Pushing Job {fake_job_id} to Redis...")
r.rpush('job_queue', json.dumps(payload))
print("✅ Done. Check your worker terminal.")