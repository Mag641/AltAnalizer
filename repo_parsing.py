import re
from typing import Dict, List, AnyStr

import pandas as pd
import requests
from requests.exceptions import HTTPError
from tqdm import tqdm

from constants import *
from utils import log_error, check_dir_exist, process_http_error


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
            for page in tqdm(range(2, last_page + 1), desc='Parsing pages'):
                events = requests.get(
                    url,
                    params={'q': f'repo:{org}/{repo} type:issue', 'page': page},
                    auth=AUTH_PARAMS
                )
                try:
                    events.raise_for_status()
                except HTTPError as e:
                    process_http_error(e)
                    events = requests.get(
                        url,
                        params={'q': f'repo:{org}/{repo} type:issue', 'page': page},
                        auth=AUTH_PARAMS
                    )
                    if events.status_code != 200:
                        print(events.json())
                        exit(1)

                events_json.extend(events.json()['items'])
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
        check_dir_exist(org, repo)
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
                for page in tqdm(range(2, last_page + 1), desc='Parsing pages'):
                    events = requests.get(
                        url,
                        params={'page': page},
                        auth=AUTH_PARAMS
                    )
                    try:
                        events.raise_for_status()
                    except HTTPError as e:
                        process_http_error(e)
                        events = requests.get(
                            url,
                            params={'page': page},
                            auth=AUTH_PARAMS
                        )
                        if events.status_code != 200:
                            print(events.json())
                            exit(1)

                    events_json.extend(events.json())
        else:
            log_error(events.json())
            exit(1)
        return events_json


def get_commits_datetimes(commits_history):
    datetimes = []
    for obj in tqdm(commits_history, desc='Formatting commits...'):
        author_date = obj['commit']['author']['date']
        committer_date = obj['commit']['committer']['date']
        if author_date not in datetimes:
            datetimes.append(author_date)
        elif committer_date != author_date:
            if committer_date not in datetimes:
                datetimes.append(committer_date)
        else:
            pass
    return datetimes


def _get_commits_datetimes_urls(commits_history):
    dates_urls = []
    for obj in tqdm(commits_history, desc='Formatting commits...'):
        dates_urls.append((obj['commit']['committer']['date'], obj['html_url']))
    return dates_urls


def get_releases_datetimes(releases_history):
    release_datetimes = []
    for release in tqdm(releases_history, desc='Formatting releases...'):
        release_datetimes.append(release['published_at'])
    return release_datetimes


def get_issues_datetimes(issues_history):
    issues_opens = []
    issues_closes = []
    for issue in tqdm(issues_history, desc='Formatting issues...'):
        issues_opens.append(issue['created_at'])
        issues_closes.append(issue['closed_at'] if issue['closed_at'] is not None else '')
    return issues_opens, issues_closes


# Not needed for now(legacy)
def to_dataframe(history: Dict[AnyStr, List]):
    df = pd.DataFrame(history)
    return df
    '''
    start_datetimes = []
    end_datetimes = []
    for series in history:
        start_datetimes.append(series[0])
        end_datetimes.append(series[-1])

    earlier_datetime = min(start_datetimes)
    latest_datetime = max(end_datetimes)

    timeline = pd.date_range(earlier_datetime, latest_datetime, freq='H')
    '''
