# CareerTrack – Job Application Management System

A web-based job application management system built using Python Flask and PostgreSQL.

CareerTrack helps users organize their job applications, manage company details, track interview schedules, and monitor application statistics through a dashboard.

## Features

- Dashboard with live application statistics
- Add and manage company details
- Add and track job applications
- Update application statuses
- Delete job applications
- Schedule and view interviews
- PostgreSQL database integration
- Responsive user interface

## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS
- **Database:** PostgreSQL
- **Version Control:** Git and GitHub
- **Development Tool:** Visual Studio Code

## Project Structure

```text
CareerTrack/
│
├── app.py
├── .gitignore
├── .env
├── templates/
│   ├── dashboard.html
│   ├── companies.html
│   ├── add_company.html
│   ├── applications.html
│   ├── add_application.html
│   ├── update_application.html
│   ├── interviews.html
│   └── add_interview.html
│
└── static/
    └── style.css
```

## Installation and Setup

1. Clone this repository:

```bash
git clone https://github.com/Keerthana03582/-CareerTrack.git
```

2. Open the project folder:

```bash
cd -CareerTrack
```

3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

5. Install the required packages:

```bash
pip install flask psycopg2-binary python-dotenv
```

6. Create a PostgreSQL database named `careertrack` and configure the required tables.

7. Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_NAME=careertrack
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

Replace the password placeholder with your own local PostgreSQL password. Never upload your `.env` file.

8. Run the application:

```bash
python app.py
```

9. Open your browser:

```text
http://127.0.0.1:5000
```

## Learning Outcomes

Through this project, I practised:

- Python Flask application development
- PostgreSQL database connectivity
- CRUD operations
- SQL queries and relational database concepts
- HTML and CSS integration
- Git version control and GitHub publishing

## Future Enhancements

- Automated job application tracking
- Email reminders for interviews
- Advanced analytics and reports
- AI-powered job recommendations

## Author

**Keerthana**

B.Tech Computer Science and Engineering Graduate – 2026

GitHub: https://github.com/Keerthana03582