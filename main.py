import json

import pandas as pd
import plotly.graph_objs as go
from repo_parsing import get_commits_datetimes, get_commits_history


def main():
    org = 'klaytn'
    repo = 'klaytn'
    '''
    commits_history = get_commits_gistory('klaytn', 'klaytn')
    commits_dates = get_commits_dates(commits_history)
    with open(f'{org}_{repo}_commits.txt'.format(org=org, repo=repo), 'w') as file:
        file.truncate()
        file.write('\n'.join(commits_dates))
    '''

    with open('{org}_{repo}_commits.txt'.format(org=org, repo=repo), 'r') as file:
        commits_dates = file.readlines()

    series = pd.to_datetime(commits_dates, format='%Y-%m-%dT%H:%M:%S')
    fig = go.Figure(data=go.Scatter(x=series, y=[1] * len(series), mode='markers'))
    fig.show()


if __name__ == '__main__':
    main()
