from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
from utils.db import execute_query
from utils.resume_parser import extract_text_from_pdf, extract_skills
from utils.job_api import fetch_jobs
from utils.matcher import match_jobs
from functools import wraps
import os

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Basic login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = execute_query("SELECT * FROM users WHERE username = %s", (username,), fetch=True)
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user exists
        existing_user = execute_query("SELECT id FROM users WHERE username = %s OR email = %s", (username, email), fetch=True)
        if existing_user:
            flash('Username or email already exists.', 'error')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password)
        try:
            user_id = execute_query(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, hashed_password),
                commit=True
            )
            if user_id is None:
                flash('CRITICAL ERROR: Database is not connected! Please create the MySQL database.', 'error')
                return redirect(url_for('register'))
                
            session['user_id'] = user_id
            session['username'] = username
            flash('Registration successful!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash('An error occurred during registration.', 'error')
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    
    # Get profile and skills
    profile = execute_query("SELECT * FROM profiles WHERE user_id = %s", (user_id,), fetch=True)
    skills = []
    if profile and profile['extracted_skills']:
        skills = profile['extracted_skills'].split(',')
        
    # Get saved jobs
    saved_jobs = execute_query("SELECT * FROM saved_jobs WHERE user_id = %s ORDER BY saved_at DESC", (user_id,), fetchall=True)
    
    return render_template('dashboard.html', profile=profile, skills=skills, saved_jobs=saved_jobs)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']
    
    if request.method == 'POST':
        if 'resume' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
            
        file = request.files['resume']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
            
        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{user_id}_{filename}")
            file.save(filepath)
            
            # Analyze
            text = extract_text_from_pdf(filepath)
            
            # Truncate text to avoid MySQL TEXT length limit (65535 bytes max)
            if len(text) > 60000:
                text = text[:60000]
                
            skills_list = extract_skills(text)
            skills_str = ','.join(skills_list)
            
            # Save or update profile
            existing_profile = execute_query("SELECT id FROM profiles WHERE user_id = %s", (user_id,), fetch=True)
            if existing_profile:
                execute_query(
                    "UPDATE profiles SET resume_text = %s, extracted_skills = %s WHERE user_id = %s",
                    (text, skills_str, user_id),
                    commit=True
                )
            else:
                execute_query(
                    "INSERT INTO profiles (user_id, resume_text, extracted_skills) VALUES (%s, %s, %s)",
                    (user_id, text, skills_str),
                    commit=True
                )
                
            flash('Resume uploaded and analyzed successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid file type. Please upload a PDF file.', 'error')
            return redirect(url_for('profile'))
            
    # GET request
    profile_data = execute_query("SELECT * FROM profiles WHERE user_id = %s", (user_id,), fetch=True)
    skills = []
    if profile_data and profile_data['extracted_skills']:
        skills = profile_data['extracted_skills'].split(',')
        
    return render_template('profile.html', profile=profile_data, skills=skills)

@app.route('/jobs')
@login_required
def jobs():
    user_id = session['user_id']
    
    # Get user skills
    profile = execute_query("SELECT extracted_skills FROM profiles WHERE user_id = %s", (user_id,), fetch=True)
    user_skills = []
    if profile and profile['extracted_skills']:
        user_skills = profile['extracted_skills'].split(',')
        
    # Fetch all jobs (mock)
    # In a real app we might pass user_skills as query params to the external API
    all_jobs = fetch_jobs(user_skills)
    
    if user_skills:
        # Match based on skills
        matched_jobs = match_jobs(user_skills, all_jobs)
    else:
        # No skills, just return fetched jobs without scores
        matched_jobs = all_jobs
        
    return render_template('jobs.html', jobs=matched_jobs, skills=user_skills)

@app.route('/save_job', methods=['POST'])
@login_required
def save_job():
    user_id = session['user_id']
    job_id = request.form.get('job_id')
    job_title = request.form.get('job_title')
    company = request.form.get('company')
    url = request.form.get('url')
    
    try:
        execute_query(
            "INSERT INTO saved_jobs (user_id, job_id, job_title, company, url) VALUES (%s, %s, %s, %s, %s)",
            (user_id, job_id, job_title, company, url),
            commit=True
        )
        flash('Job saved to your dashboard!', 'success')
    except Exception as e:
        flash('Job might already be saved.', 'error')
        
    return redirect(url_for('jobs'))

if __name__ == '__main__':
    app.run(debug=True)
