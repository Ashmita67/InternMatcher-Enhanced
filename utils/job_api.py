import requests
import random

def fetch_jobs(skills, location="Remote", limit=10):
    """
    Fetches real remote software internships/jobs from the public remotive.io API.
    Since remotive doesn't require an API key, it's perfect for demonstration!
    """
    
    url = "https://remotive.com/api/remote-jobs"
    params = {
        "category": "software-dev",
        "limit": 50 # Fetch a batch to filter through
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            
            formatted_jobs = []
            for job in jobs:
                # Remotive doesn't provide explicit "skills_required" arrays,
                # so we extract them from the description and tags
                job_text = (job.get("description", "") + " " + " ".join(job.get("tags", []))).lower()
                
                # Check which of our common skills appear in this job's text
                common_skills = [
                    "python", "java", "c++", "javascript", "react", "node.js", "flask", "django", 
                    "sql", "mysql", "mongodb", "aws", "docker", "kubernetes", "machine learning", 
                    "html", "css", "git", "linux", "c#", "php", "ruby", "swift",
                    "kotlin", "typescript", "angular", "vue", "spring", "express", "postgresql",
                    "azure", "gcp", "tensorflow", "pytorch", "pandas", "numpy", "c", "go", "rust"
                ]
                
                job_skills = [s for s in common_skills if s in job_text]
                
                # If we couldn't find any explicit skills, just pick a few random ones from the job description tags
                if not job_skills and job.get("tags"):
                    job_skills = [str(tag).lower() for tag in job.get("tags")[:3]]
                elif not job_skills:
                   job_skills = ["programming", "development"]

                import re
                
                # Strip raw HTML tags that remotive provides in the description
                clean_description = re.sub(r'<[^>]+>', '', str(job.get("description", "")))
                clean_description = clean_description.replace('&nbsp;', ' ').replace('&amp;', '&').strip()

                formatted_jobs.append({
                    "id": str(job.get("id")),
                    "title": job.get("title", "Software Developer"),
                    "company": job.get("company_name", "Remote Company"),
                    "location": job.get("candidate_required_location", "Remote"),
                    "description": clean_description[:200] + "...", 
                    "skills_required": job_skills,
                    "url": job.get("url")
                })
            
            # If the user has skills, try to prioritize jobs that actually overlap before slicing the limit
            if skills:
                user_skills_set = set([s.lower() for s in skills])
                formatted_jobs.sort(key=lambda j: len(user_skills_set.intersection(set(j['skills_required']))), reverse=True)
                
            # Randomize slightly if no skills so it doesn't look identical every time
            elif formatted_jobs:
               random.shuffle(formatted_jobs)

            return formatted_jobs[:limit]
            
    except Exception as e:
        print(f"Error fetching from Job API: {e}")
        
    # Fallback to mock data if the API fails or you are offline
    print("Falling back to local mock jobs.")
    return [
        {
            "id": "job_1",
            "title": "Software Engineering Intern",
            "company": "TechNova",
            "location": "Remote",
            "description": "Looking for a Python and Flask intern to help build web applications.",
            "skills_required": ["python", "flask", "sql", "git"],
            "url": "https://example.com/jobs/1"
        },
        {
            "id": "job_2",
            "title": "Frontend Developer Intern",
            "company": "CreativeWeb",
            "location": "Remote",
            "description": "Seeking an intern proficient in React, JavaScript, HTML, and CSS.",
            "skills_required": ["javascript", "react", "html", "css"],
            "url": "https://example.com/jobs/2"
        }
    ]
