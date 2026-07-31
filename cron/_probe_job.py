#!/usr/bin/env python3
import json

with open('/root/.hermes/cron/jobs.json') as f:
    d = json.load(f)

jobs = d.get('jobs', [])
for job in jobs:
    if job.get('name') == 'daily-news-briefing':
        print(f"JOB ID: {job.get('job_id')}")
        print(f"Name: {job.get('name')}")
        print(f"Schedule: {job.get('schedule')}")
        prompt = job.get('prompt', '')
        print(f"\n--- PROMPT ({len(prompt)} chars) ---")
        print(prompt[:3000])
        print(f"\n--- SKILLS: {job.get('skills', [])}")
        break
else:
    print("daily-news-briefing not found")
    print("Available jobs:", [j.get('name') for j in jobs])
