import os
from dotenv import load_dotenv

load_dotenv()


import psycopg2
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)



def get_db_connection():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    return connection



@app.route("/")
def home():
    return "Welcome to CareerTrack!"


@app.route("/db-test")
@app.route("/companies")
def companies():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT company_id, company_name, website, location
        FROM companies
        ORDER BY company_id;
    """)

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "companies.html",
        companies=records
    )
@app.route("/add-company", methods=["GET", "POST"])
def add_company():

    if request.method == "POST":

        company_name = request.form["company_name"]
        website = request.form["website"]
        location = request.form["location"]

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO companies
            (company_name, website, location)
            VALUES (%s, %s, %s)
            """,
            (company_name, website, location)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("companies"))

    return render_template("add_company.html")


@app.route("/add-application", methods=["GET", "POST"])
def add_application():

    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        company_id = request.form["company_id"]
        job_title = request.form["job_title"]
        job_url = request.form["job_url"]
        status = request.form["status"]

        cursor.execute(
            """
            INSERT INTO applications
            (company_id, job_title, job_url, status)
            VALUES (%s, %s, %s, %s)
            """,
            (company_id, job_title, job_url, status)
        )

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for("companies"))

    cursor.execute(
        "SELECT company_id, company_name FROM companies ORDER BY company_name"
    )

    companies = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("add_application.html", companies=companies)


@app.route("/applications")
def applications():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            applications.application_id,
            companies.company_name,
            applications.job_title,
            applications.application_date,
            applications.status
        FROM applications
        INNER JOIN companies
        ON applications.company_id = companies.company_id
        ORDER BY applications.application_id DESC;
    """)

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "applications.html",
        applications=records
    )

@app.route("/update-application/<int:application_id>", methods=["GET", "POST"])
def update_application(application_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        status = request.form["status"]

        cursor.execute(
            """
            UPDATE applications
            SET status = %s
            WHERE application_id = %s
            """,
            (status, application_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("applications"))

    cursor.execute(
        """
        SELECT application_id, job_title, status
        FROM applications
        WHERE application_id = %s
        """,
        (application_id,)
    )

    application = cursor.fetchone()

    cursor.close()
    connection.close()

    if application is None:
        return "Application not found", 404

    return render_template(
        "update_application.html",
        application=application
    )
@app.route("/delete-application/<int:application_id>", methods=["POST"])
def delete_application(application_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM interviews
        WHERE application_id = %s
        """,
        (application_id,)
    )

    interview_count = cursor.fetchone()[0]

    if interview_count > 0:
        cursor.close()
        connection.close()
        return "Cannot delete: this application has linked interviews."

    cursor.execute(
        """
        DELETE FROM applications
        WHERE application_id = %s
        """,
        (application_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("applications"))

@app.route("/add-interview", methods=["GET", "POST"])
def add_interview():

    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        application_id = request.form["application_id"]
        interview_date = request.form["interview_date"]
        interview_type = request.form["interview_type"]
        notes = request.form["notes"]

        cursor.execute(
            """
            INSERT INTO interviews
            (application_id, interview_date, interview_type, notes)
            VALUES (%s, %s, %s, %s)
            """,
            (application_id, interview_date, interview_type, notes)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("interviews"))

    cursor.execute("""
        SELECT
            applications.application_id,
            companies.company_name,
            applications.job_title
        FROM applications
        INNER JOIN companies
        ON applications.company_id = companies.company_id
        ORDER BY applications.application_id DESC
    """)

    applications = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "add_interview.html",
        applications=applications
    )

@app.route("/interviews")
def interviews():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            interviews.interview_id,
            companies.company_name,
            applications.job_title,
            interviews.interview_date,
            interviews.interview_type,
            interviews.notes
        FROM interviews
        INNER JOIN applications
        ON interviews.application_id = applications.application_id
        INNER JOIN companies
        ON applications.company_id = companies.company_id
        ORDER BY interviews.interview_date DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "interviews.html",
        interviews=records
    )
def db_test():
    try:
        connection = get_db_connection()
        connection.close()

        return "PostgreSQL connected successfully!"

    except Exception as error:
        return f"Database connection failed: {error}"



@app.route("/dashboard")
def dashboard():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM companies")
    total_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications")
    total_applications = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM interviews")
    total_interviews = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = %s",
        ("Selected",)
    )
    selected_applications = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = %s",
        ("Rejected",)
    )
    rejected_applications = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        total_companies=total_companies,
        total_applications=total_applications,
        total_interviews=total_interviews,
        selected_applications=selected_applications,
        rejected_applications=rejected_applications
    )



if __name__ == "__main__":
    app.run(debug=True)

