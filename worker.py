import requests
import sqlite3
import time
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
URL_JOBS = 'https://api.github.com/repos/awesome-jobs/vietnam/issues'


def crawl_jobs():
    data_base = 'jobs.db'
    conn = sqlite3.connect(data_base)
    c = conn.cursor()

    try:
        c.execute('''CREATE TABLE jobs
                (job_id integer, link_job text, title text,
                    postdate text, contents text)''')
        conn.commit()
    except:
        pass
    sql = 'DELETE FROM jobs'
    c.execute(sql)
    conn.commit()
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

@sched.scheduled_job('cron', hour=10)
# @sched.scheduled_job('interval', seconds=10)
def main():
    # now = datetime.now()
    #     if now.hour == 21 and now.minute == 16 and now.second == 30:
    #         crawl_jobs()
    # print('start crawl: {}'.format(datetime.now()))
    crawl_jobs()


if __name__ == "__main__":
    sched.start()
    # main()
