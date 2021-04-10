import json

import pandas as pd
import plotly.graph_objs as go
from repo_parsing import get_commits_dates, get_commits_gistory

USERNAME = 'Mag641'
TOKEN = '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'

MAIN_URL = 'https://api.github.com'
ORG_EVENTS_END = '/orgs/{org}/events'
REPOS_EVENTS_END = '/repos/{owner}/{repo}/events'
COMMITS_END = '/repos/{}/{}/commits'

eth_repo = 'https://github.com/ethereum/go-ethereum'
klaytn_reop = 'https://github.com/klaytn/klaytn'


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
