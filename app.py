import sqlite3
import time
from flask import Flask, Markup
import markdown
from crawl_jobs import *
from datetime import datetime

app = Flask(__name__)
conn = sqlite3.connect('jobs.db', check_same_thread=False)
c = conn.cursor()
now = datetime.now()
if now.hour == 21 and now.minute == 16 and now.second == 30:
    crawl_jobs()

@app.route("/jobs")
def list_jobs():
    data = c.execute("SELECT * FROM jobs;").fetchall()
    conn.commit()
    time.sleep(3)
    lines = []
    # result = "<h1>List Open Jobs</h1><ul>"
    result = "<ul>"
    order = 1
    for job_id, link, title, date, details in data:
        a = '''{0}.<a href='/jobs/{1}'>{2}</a><p><small>
        <em>Date create: {3}. Job ID: {1}</em></small>
        </p>'''.format(order, job_id, title, date)
        lines.append(a)
        order += 1
    result = result + "<br>" + "<br>".join(lines) + "</ul>"
    format_result = '''
                <html lang="en">
                <head>
                <title>Tech jobs</title>
                </head>

                <body>
                <h2 style="text-align: center;">Tech jobs website</h2>
                <p style="text-align: center;"><a href='https://www.linkedin.com/in/noahz110/'>About me</a></p>
                <p style="text-align: center;">Click each link below for more informations</p>
                {}
                </body>

                </html>'''.format(result)
    return format_result


@app.route("/jobs/<string:job_id_input>")
def job_details(job_id_input):
    data = c.execute("SELECT * FROM jobs;").fetchall()
    conn.commit()
    time.sleep(3)
    for job_id, link, title, date, details in data:
        if job_id == int(job_id_input):
            job_description = Markup(markdown.markdown(details))
            a = "<p>{}</p>".format(job_description)
            b = "<h2>{}</h2>".format(title)
            result = '<ul>' + "<br>" + b + "<br>" + a + "</ul>"
            return result


if __name__ == "__main__":
    app.run(debug=True)
