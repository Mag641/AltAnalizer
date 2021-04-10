import requests

from utils import log_error
from constants import *
import re


def get_commits_datetimes(history):
    dates = list()
    for obj in history:
        dates.append(obj['commit']['author']['date'])
    return dates


def get_commits_history(org: str, repo: str):  # instead of these two use one 'repo_url'?
    repo_url = API_MAIN_URL + COMMITS_END.format(org, repo)
    events = requests.get(
        repo_url,
        auth=(USERNAME, TOKEN)
    )
    if events.status_code == 200:
        events_json = events.json()

        p = re.compile('page=([0-9]+)>; rel="last"')
        last_page = int(p.search(events.headers['Link']).group(1))
        print(f'Last page: {last_page}')

        for page in range(2, last_page + 1):
            print(f'Page: {page}')
            events = requests.get(
                repo_url,
                params={'page': page},
                auth=(USERNAME, TOKEN)
            )
            if events.status_code == 200:
                events_json.extend(events.json())
            else:
                log_error(events.json())
                exit(1)
    else:
        log_error(events.json())
        exit(1)
    return events_json


def get_releases_history(repo: str):
    pass


def get_releases_datetimes(releases_history):
    pass
