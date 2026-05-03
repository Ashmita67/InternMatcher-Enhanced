# InternMatcher

Smart internship matching platform that helps students find relevant internship opportunities based on their resume skills.  
Upload a resume, extract skills automatically, and get internship recommendations with match scores.

---

## Features

- Resume upload in PDF format
- Automatic skill extraction from resume
- Internship search and matching
- Match score based job ranking
- User login and registration
- Save jobs for later
- Personal dashboard with extracted skills
- Clean and responsive interface

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **Backend:** Python, Flask
- **Database:** MySQL
- **Libraries:** SpaCy, PyPDF2
- **Tools:** Git, GitHub

---

## How It Works

1. User signs up or logs in  
2. Uploads resume in PDF format  
3. System extracts text and identifies skills  
4. Internship listings are fetched  
5. Jobs are matched with extracted skills  
6. Match score is calculated  
7. User can save relevant jobs

---

## Project Structure

```bash
InternMatcher/
├── app.py
├── config.py
├── requirements.txt
├── schema.sql
├── README.md
├── utils/
│   ├── db.py
│   ├── resume_parser.py
│   ├── job_api.py
│   └── matcher.py
├── static/
│   ├── css/
│   ├── js/
│   └── img/
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── profile.html
    └── jobs.html
```

## Database Tables

### users
Stores user account details  
`id`, `username`, `email`, `password_hash`, `created_at`

### profiles
Stores resume data and extracted skills  
`id`, `user_id`, `resume_text`, `extracted_skills`, `updated_at`

### saved_jobs
Stores bookmarked internship listings  
`id`, `user_id`, `job_id`, `job_title`, `company`, `url`, `saved_at`

## Installation

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/InternMatcher.git
cd InternMatcher ```

### 2. Create Virtual Environment
```
python -m venv venv
```
### 3. Activate Virtual Environment
```
source venv/bin/activate  (Mac,Linux)
venv\Scripts\activate     (Windows)
```
### 4. Install Dependencies
```
pip install -r requirements.txt
```
### 5. Download SpaCy Model
```
python -m spacy download en_core_web_sm
```
### 6. Setup Database
```
mysql -u root -p < schema.sql
```
### 7. Configure Database

Update database credentials in config.py
---

## Run the Project
```
cd InternMatcher
source venv/bin/activate
python app.py
```
Open in browser:
http://127.0.0.1:5000/

---

## Workflow
- Register or login
- Upload resume
- Extract skills
- View dashboard
- Search internships
- Check match score
- Save jobs

---

## Screenshots

### Landing Page
static/img/Landingpage.png
static/img/LP2.png

### Dashboard
static/img/Dashboard.png

### ResumeUpload
static/img/ResumeUpload.png

### JobMatchResults
static/img/JobMatchResults.png

---
## Future Improvements

- AI-based skill extraction
- Live internship API integration
- Email job alerts
- Smarter recommendation engine
- One-click Automatic job application

---

