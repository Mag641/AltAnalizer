import re

import requests

from constants import *
from utils import log_error


def get_history(org: str, repo: str, target: str):  # instead of these two use one 'repo_url'?
    url = API_MAIN_URL + REPO_END.format(org, repo) + f'/{target}'
    events = requests.get(
        url,
        auth=AUTH_PARAMS
    )
    if events.status_code == 200:
        events_json = events.json()

        p = re.compile('page=([0-9]+)>; rel="last"')
        last_page = int(p.search(events.headers['Link']).group(1))
        print(f'Last page: {last_page}')

        for page in range(2, last_page + 1):
            print(f'Page: {page}')
            events = requests.get(
                url,
                params={'page': page},
                auth=AUTH_PARAMS
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


def get_commits_datetimes(history):
    dates = list()
    for obj in history:
        dates.append(obj['commit']['author']['date'])
    return dates
