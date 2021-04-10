import re

import requests

from constants import *
from utils import log_error
from tqdm import tqdm
from pprint import pprint


def get_all(org: str, repo: str):
    print('Getting commits...')
    commits_history = get_history(org, repo, 'commits')
    commits_datetimes = get_commits_datetimes(commits_history)
    print('Getting releases...')
    releases_history = get_history(org, repo, 'releases')
    releases_datetimes = get_releases_datetimes(releases_history)

    issues_history = get_history(org, repo, 'issues')
    issues_datetimes = get_issues_datetimes(issues_history)

    whole_history = {'commits': commits_datetimes, 'releases': releases_datetimes, 'issues': issues_datetimes}
    return whole_history


def get_history(org: str, repo: str, target: str):  # instead of these two use one 'repo_url'?
    url = API_MAIN_URL + REPO_END.format(org, repo) + f'/{target}'
    events = requests.get(
        url,
        auth=AUTH_PARAMS
    )
    if events.status_code == 200:
        events_json = events.json()

        if 'Link' in events.headers:
            p = re.compile('page=([0-9]+)>; rel="last"')
            last_page = int(p.search(events.headers['Link']).group(1))
            pbar = tqdm(range(2, last_page + 1), smoothing=0)
            for page in pbar:
                pbar.set_description(f'Page {page} of {last_page}')
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


def get_releases_datetimes(releases_history):
    pass


def get_issues_datetimes(issues_history):
    pass
