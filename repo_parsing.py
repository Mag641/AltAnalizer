import re

import requests

from utils import log_error


def get_commits_gistory(main_url: str, endpoint: str, format_params: tuple, auth_params: tuple):
    events = requests.get(
        main_url + endpoint.format(*format_params),
        auth=auth_params
    )
    if events.status_code == 200:
        events_json = events.json()

        p = re.compile('page=([0-9]+)>; rel="last"')
        last_page = int(p.search(events.headers['Link']).group(1))
        print(f'Last page: {last_page}')

        for page in range(2, last_page + 1):
            print(f'Page: {page}')
            events = requests.get(
                main_url + endpoint.format(*format_params), params={'page': page},
                auth=auth_params
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


def get_commits_dates(history):
    dates = list()
    for obj in history:
        dates.append(obj['commit']['author']['date'])
    return dates
