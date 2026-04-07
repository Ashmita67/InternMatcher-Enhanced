def calculate_match_score(user_skills, job_skills):
    """
    Calculates a match score between a user's skills and a job's required skills.
    Returns a score between 0 and 100.
    """
    if not job_skills or not user_skills:
        return 0
        
    user_skills_set = set([s.lower() for s in user_skills])
    job_skills_set = set([s.lower() for s in job_skills])
    
    # Calculate intersection (skills both have)
    intersection = user_skills_set.intersection(job_skills_set)
    
    # Calculate score based on percentage of job skills met
    match_percentage = (len(intersection) / len(job_skills_set)) * 100
    
    return round(match_percentage)

def match_jobs(user_skills, jobs_list):
    """
    Takes a list of user skills and a list of jobs, calculates the match score
    for each, and returns a sorted list of jobs (highest match first).
    """
    matched_jobs = []
    
    for job in jobs_list:
        score = calculate_match_score(user_skills, job.get('skills_required', []))
        job_copy = job.copy()
        job_copy['match_score'] = score
        matched_jobs.append(job_copy)
        
    # Sort by descending match score
    matched_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    
    return matched_jobs
