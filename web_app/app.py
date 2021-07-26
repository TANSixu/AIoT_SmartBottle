import os
import sys

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import psycopg2 as psy
import time

db = psy.connect(database='Smart_bottle', user='postgres', password='123456', host='192.168.3.116',
                         port='5432')
cur = db.cursor()

app = Flask(__name__)

class Record():
    def __init__(self, time, amt):
        self.time = time
        self.amt = amt

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index():
    current_time = time.strftime("%Y-%m-%d", time.localtime())
    # current_time = '2021-7-25'
    cur.execute('''select * from drinking
                      order by  time desc   
                      limit 5''')
    result = cur.fetchall()
    record = []
    for r in result:
        hour = r[0]
        amt = format(r[1], '.2f')
        record.append(Record(hour, amt))
        
    cur.execute('''select* from daily_report('%s')''' %(current_time))
    daily = cur.fetchall()
    freq = []
    volume = []
    for dr in daily:
        freq.append(dr[0])
        volume.append(round(dr[1], 3))

    return render_template('index.html', freq=freq, vol=volume, records=record, cur_date=str(current_time))

@app.route('/statistics')
def statistics():
    cur.execute('''select to_char(time, 'yyyy-MM-dd') as day, count(*) as freq, sum(drinking_amount) as tot_amt
                        from drinking
                        group by day
                        order by day
                        limit 3''')
    result = cur.fetchall()
    days = []
    days_freq=[]
    days_amt=[]
    for r in result:
        days.append(r[0])
        days_freq.append(r[1])
        days_amt.append(round(r[2], 2))

    if len(days)<5:
        days_freq = [0 for i in range(5-len(days))]+days_freq
        days_amt = [0 for i in range(5-len(days))]+days_amt
    return render_template('statistics.html', freq = days_freq, amt = days_amt)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)