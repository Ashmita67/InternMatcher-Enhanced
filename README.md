# InternMatcher - College Project Report

## 1. Project Overview
InternMatcher is a full-stack web application developed to bridge the gap between students and relevant internship opportunities. Finding an internship that matches a student's particular skill set can be time-consuming and tedious. InternMatcher solves this problem by allowing users to upload their resumes in PDF format. The system then automatically parses the resume, extracts the technical skills, and matches them against aggregated job listings, presenting the user with a tailored list of open positions complete with match scores.

## 2. Features of the System
- **User Authentication**: Secure user registration and login system with encrypted passwords.
- **Resume Processing**: PDF upload functionality with automated text extraction and NLP-based parsing to identify key technical skills.
- **Job Aggregation**: Simulated integration with external Job APIs to fetch remote and local internship opportunities.
- **Job Matching Algorithm**: A custom algorithm that calculates an intersection-based percentage score comparing the user's extracted skills against the required skills for each job.
- **Interactive Dashboard**: A personalized user dashboard showing extracted skills and previously saved jobs.
- **Saved Jobs**: Functionality allowing users to bookmark jobs they are interested in applying for later.
- **Skill Filters & Management**: The ability to update resumes to refresh the extracted skill list, directly affecting job search results.

## 3. System Architecture
The application follows a standard Client-Server architecture:
- **Frontend (Client)**: Built with HTML, Vanilla CSS (incorporating modern aesthetics and glassmorphism), and Jinja2 templating. It handles user interaction and displays data iteratively.
- **Backend (Server)**: A Python Flask web server. It manages session state, routes requests, processes business logic (like handling file uploads), and interacts with utility modules.
- **Database**: A MySQL database storing user credentials, profile information, cached skills, and saved jobs.

**Data Flow Explanation:**
User → Frontend (HTML/CSS) → Flask Backend (app.py) → MySQL Database (Stores User/Resume Data) → Job APIs (Fetches external listings) → Matcher Algorithm → Filtered Job Results displayed on Frontend.

## 4. Project Folder Structure
```
InternMatcher/
├── app.py                 # Main Flask application and route definitions
├── config.py              # Configuration globals (DB credentials, Settings)
├── requirements.txt       # Python dependencies list
├── schema.sql             # MySQL Database schema script for initialization
├── README.md              # Complete Project Documentation Report
├── utils/                 # Utility modules outlining separation of concerns
│   ├── db.py              # Database connection and query execution helper
│   ├── resume_parser.py   # PDF text extraction and NLP skill parsing
│   ├── job_api.py         # External Job API fetching and aggregation logic
│   └── matcher.py         # Job matching algorithm calculating intersection scores
├── static/                # Static assets served to the client
│   ├── css/               # Vanilla CSS for styling (Modern UI)
│   ├── js/                # Vanilla JS for interactive elements (if any)
│   └── img/               # Images and icons directory
└── templates/             # HTML Templates rendered via Jinja2
    ├── base.html          # Base layout providing navbar and flash messages
    ├── index.html         # Landing page
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── dashboard.html     # User dashboard showing skills and saved jobs
    ├── profile.html       # Resume upload and skills viewing
    └── jobs.html          # Job listings and search results with match scores
```

## 5. Database Design
The system uses a relational database (MySQL) with the following schema:

- **`users` Table:**
  - `id` (INT, Primary Key, Auto-increment): Unique identifier for the user.
  - `username` (VARCHAR): Unique username chosen by the user.
  - `email` (VARCHAR): Unique email address.
  - `password_hash` (VARCHAR): Securely hashed representation of the user's password.
  - `created_at` (TIMESTAMP): Account creation timestamp.

- **`profiles` Table:**
  - `id` (INT, Primary Key, Auto-increment): Unique identifier.
  - `user_id` (INT, Foreign Key): Links to `users.id` (Cascades on delete).
  - `resume_text` (TEXT): The raw text extracted from the uploaded PDF.
  - `extracted_skills` (TEXT): Comma-separated list of identified skills.
  - `updated_at` (TIMESTAMP): Last profile update timestamp.

- **`saved_jobs` Table:**
  - `id` (INT, Primary Key, Auto-increment): Unique identifier.
  - `user_id` (INT, Foreign Key): Links to `users.id` (Cascades on delete).
  - `job_id` (VARCHAR): Unique identifier from the external job API.
  - `job_title` (VARCHAR): The title of the saved job.
  - `company` (VARCHAR): The company offering the job.
  - `url` (TEXT): Link to apply for the job.
  - `saved_at` (TIMESTAMP): When the job was saved.

## 6. Installation Guide
Follow these beginner-friendly steps to run the project locally.

**Step 1: Install Python**
Ensure you have Python 3.8+ installed on your machine. You can download it from [python.org](https://www.python.org/).

**Step 2: Install MySQL**
Install MySQL Server. You can use tools like XAMPP or download MySQL Community Server directly. Ensure the MySQL service is running.

**Step 3: Install Dependencies**
Open your terminal/command prompt, navigate to the `InternMatcher` folder, and run:
```bash
pip install -r requirements.txt
```
*Note: You may also need to download the SpaCy english model:*
```bash
python -m spacy download en_core_web_sm
```

**Step 4: Create Database and Import Schema**
Open your MySQL command line client or a tool like phpMyAdmin/MySQL Workbench, and run the SQL commands found in `schema.sql`:
```bash
mysql -u root -p < schema.sql
```

**Step 5: Configure Database Connection**
Open `config.py` (or create a `.env` file) and ensure the `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DB` match your local MySQL setup (default user is usually `root` with no password).

## 7. How to Run the Project
Once installed and configured, run the following command in the `InternMatcher` directory:
```bash
python app.py
```
Open your web browser and navigate to: `http://127.0.0.1:5000/`

## 8. System Walkthrough
1. **Landing Page:** The user arrives at the homepage and is presented with the application's value proposition.
2. **Registration/Login:** The user creates a new account or logs in to an existing one. Credentials are saved securely.
3. **Profile Setup:** The user navigates to the Profile section and uploads their resume in PDF format.
4. **Analysis:** The system parses the PDF, extracts the text, and identifies programming languages and technologies.
5. **Dashboard Verification:** The user can view their extracted skills on their personalized dashboard.
6. **Job Searching:** The user navigates to "Find Jobs". The system fetches jobs (simulated API) and ranks them against the user's extracted skills, attaching a "Match Score".
7. **Saving Jobs:** The user can click "Save" on interesting jobs, which then appear on their Dashboard for future reference.

## 9. Expected Deliverables
- [x] Working full-stack web application
- [x] Flask backend system
- [x] MySQL database schema
- [x] Responsive frontend interface
- [x] Resume skill extraction system
- [x] Job matching algorithm
- [x] Project documentation

## 10. Future Improvements
- **AI-based skill extraction:** Upgrade the NLP model to use more advanced LLM models (e.g., OpenAI API) for highly accurate entity extraction.
- **Automatic job application:** Build browser automation extensions to try and auto-fill applications based on user profile data.
- **Email alerts for new jobs:** Implement a scheduled worker (like Celery) to email users when new high-match jobs are found daily.
- **Machine learning job recommendation system:** Replace the basic intersection algorithm with a collaborative filtering or content-based machine learning model that learns from user "Save" interactions.

## 11. Conclusion
InternMatcher successfully provides a proof-of-concept pipeline demonstrating how automation and specifically resume parsing can heavily optimize the job hunting experience. By aggregating requirements and crossing them with an individual's verified skills, the system reduces the noise for job seekers, pointing them directly toward the high-probability opportunities where their specific technical background is actively desired. This project showcases the powerful integration of full-stack web development (Flask/MySQL) with applied NLP methodologies.
