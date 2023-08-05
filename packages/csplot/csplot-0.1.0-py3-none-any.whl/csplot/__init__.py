import matplotlib.pyplot as plt

import requests
import datetime
from dateutil.rrule import rrule, DAILY

def xpPlot(user: str, since: datetime.date, path: str, until = datetime.datetime.today() + datetime.timedelta(days=1), title="Code::Stats for {user}", endpoint = 'https://codestats.net'):
    r = requests.get(f"{endpoint}/api/users/{user}")

    dates = r.json()['dates']

    days = {}
    for date in rrule(DAILY, dtstart=since, until=until):
        days.update({date.strftime(r'%b %d'): dates.get(date.strftime(r'%Y-%m-%d'), 0)})

    fig, ax = plt.subplots()
    ax.bar(days.keys(), days.values())
    ax.set_title(title.format(user=user))
    ax.set_ylabel('XP')
    fig.autofmt_xdate()
    fig.savefig(path)