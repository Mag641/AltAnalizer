import json
import re

import pandas as pd
import requests

import plotly.express as px
import plotly.graph_objs as go

USERNAME = 'Mag641'
TOKEN = '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'

MAIN_URL = 'https://api.github.com'
ORG_EVENTS_END = '/orgs/{org}/events'
REPOS_EVENTS_END = '/repos/{owner}/{repo}/events'
COMMITS_END = '/repos/{}/{}/commits'

eth_repo = 'https://github.com/ethereum/go-ethereum'
klaytn_reop = 'https://github.com/klaytn/klaytn'


def log_error(error):
    with open('error.txt', 'w+') as file:
        file.write(json.dumps(error, indent=4))


def get_commits_dates(history):
    dates = list()
    for obj in history:
        dates.append(obj['commit']['author']['date'])
    return dates


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


def main():
    '''
        commits_history = get_commits_gistory(MAIN_URL, COMMITS_END, ('klaytn', 'klaytn'), (USERNAME, TOKEN))
        commits_dates = get_commits_dates(commits_history)
        with open('klaytn_commits.txt', 'w') as file:
            file.truncate()
            file.write('\n'.join(commits_dates))
        '''

    with open('klaytn_commits.txt', 'r') as file:
        commits_dates = file.readlines()

    series = pd.to_datetime(commits_dates, format='%Y-%m-%dT%H:%M:%S')
    fig = go.Figure(data=go.Scatter(x=series, y=[1] * len(series), mode='markers'))
    fig.show()


if __name__ == '__main__':
    main()
