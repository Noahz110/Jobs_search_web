import requests
import sqlite3
import time

URL_JOBS = 'https://api.github.com/repos/awesome-jobs/vietnam/issues'
data_base = 'jobs.db'
conn = sqlite3.connect(data_base)
c = conn.cursor()
c.execute('''CREATE TABLE jobs
           (job_id integer, link_job text, title text,
            postdate text, contents text)''')
conn.commit()


def crawl_jobs():
    ses = requests.Session()
    page = 1
    while True:
        params = {'page': page}
        resp = ses.get(URL_JOBS, params=params)
        data = resp.json()
        if not data:
            break
        for job in data:
            c.execute('''INSERT INTO jobs VALUES
            (?, ?, ?, ?, ?)''', (job['id'], job['html_url'], job['title'],
                                 job['created_at'][:10], job['body']))
        conn.commit()
        page += 1
        time.sleep(5)
    conn.close()
    return


def main():
    crawl_jobs()


if __name__ == "__main__":
    main()
