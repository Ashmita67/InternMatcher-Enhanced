from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

def calculate_tfidf_similarity(user_skills, job_skills):
    """
    Uses TF-IDF + cosine similarity to compute match score.
    Returns score between 0–100.
    """
    if not user_skills or not job_skills:
        return 0

    # Convert skill lists into strings
    user_text = " ".join(user_skills)
    job_text = " ".join(job_skills)

    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([user_text, job_text])
        
        similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
        return round(similarity * 100)
    
    except Exception as e:
        print(f"TF-IDF error: {e}")
        return 0
    
def match_jobs(user_skills, jobs_list):
    matched_jobs = []
    
    for job in jobs_list:
        job_skills = job.get('skills_required', [])
        
        tfidf_score = calculate_tfidf_similarity(user_skills, job_skills)
        basic_score = calculate_match_score(user_skills, job_skills)
        
        score = round((0.7 * tfidf_score) + (0.3 * basic_score))
        
        job_copy = job.copy()
        job_copy['match_score'] = score
        matched_jobs.append(job_copy)
        
    matched_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    
    return matched_jobs