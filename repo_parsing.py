import os
import re
from typing import Dict, List, AnyStr

import requests
from tqdm import tqdm

from constants import *
from utils import log_error, check_dir
import pandas as pd


def _get_issues(org, repo):
    url = API_MAIN_URL + '/search/issues'
    print('Getting issues...')
    events = requests.get(
        url,
        params={'q': f'repo:{org}/{repo} type:issue'},
        auth=AUTH_PARAMS
    )
    if events.status_code == 200:
        events_json = events.json()['items']
        if 'Link' in events.headers:
            p = re.compile('page=([0-9]+)>; rel="last"')
            last_page = int(p.search(events.headers['Link']).group(1))
            pbar = tqdm(range(2, last_page + 1))
            for page in pbar:
                pbar.set_description(f'Page {page} of {last_page}')
                events = requests.get(
                    url,
                    params={'q': f'repo:{org}/{repo} type:issue', 'page': page},
                    auth=AUTH_PARAMS
                )
                if events.status_code == 200:
                    events_json.extend(events.json()['items'])
                else:
                    log_error(events.json())
                    exit(1)
    else:
        log_error(events.json())
        exit(1)
    return events_json


def get_all(org: str, repo: str):
    commits_history = get_history(org, repo, 'commits')
    commits_datetimes = get_commits_datetimes(commits_history)

    releases_history = get_history(org, repo, 'releases')
    releases_datetimes = get_releases_datetimes(releases_history)

    issues_history = get_history(org, repo, 'issues')
    issues_opens, issues_closes = get_issues_datetimes(issues_history)

    whole_history = {
        'commits': commits_datetimes,
        'releases': releases_datetimes,
        'issues_opens': issues_opens,
        'issues_closes': issues_closes
    }
    return whole_history


def get_history(org: str, repo: str, target: str):  # instead of these two use one 'repo_url'?
    if target == 'issues':
        return _get_issues(org, repo)
    else:
        check_dir(org, repo)
        print(f'Getting {target}...')
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
                pbar = tqdm(range(2, last_page + 1))
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


def get_commits_datetimes(commits_history):
    print('Formatting commits...')
    dates = list()

    commits_count = len(commits_history)
    pbar = tqdm(commits_history)
    for i, obj in enumerate(pbar):
        pbar.set_description(f'Commit {i+1} of {commits_count}')
        dates.append(obj['commit']['author']['date'])
    return dates


def get_releases_datetimes(releases_history):
    print('Formatting releases...')
    release_datetimes = list()

    releases_count = len(releases_history)
    pbar = tqdm(releases_history)
    for i, release in enumerate(pbar):
        pbar.set_description(f'Release {i+1} if {releases_count}')
        release_datetimes.append(release['published_at'])
    return release_datetimes


def get_issues_datetimes(issues_history):
    print('Formatting issues...')
    issues_opens = list()
    issues_closes = list()

    issues_count = len(issues_history)
    pbar = tqdm(issues_history)
    for i, issue in enumerate(pbar):
        pbar.set_description(f'Issue {i + 1} of {issues_count}')
        issues_opens.append(issue['created_at'])
        if issue['closed_at'] is not None:
            issues_closes.append(issue['closed_at'])

    return issues_opens, issues_closes


def to_dataframe(history: Dict[AnyStr, List]):
    df = pd.DataFrame(history)
    return df
    '''
    start_datetimes = list()
    end_datetimes = list()
    for series in history:
        start_datetimes.append(series[0])
        end_datetimes.append(series[-1])

    earlier_datetime = min(start_datetimes)
    latest_datetime = max(end_datetimes)

    timeline = pd.date_range(earlier_datetime, latest_datetime, freq='H')
    '''