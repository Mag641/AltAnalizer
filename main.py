import os

import pandas as pd

import repo_parsing
import utils
import plotly.graph_objects as go
from pprint import pprint


def main():
    if not os.path.exists('repos_info'):
        os.mkdir('repos_info')
    org = 'klaytn'
    repo = 'klaytn'

    '''
    found_issues = repo_parsing.search_issues(org, repo)
    pprint(found_issues)
    issues_raw_history = repo_parsing.get_history(org, repo, 'issues')
    for issue in issues_raw_history:
        if 'wallet cannot sync' in issue['body']:
            print('a')
    pprint(issues_raw_history)
    
    whole_klaytn_history = repo_parsing.get_all(org, repo)
    utils.write_all_history_to_files(org, repo, whole_klaytn_history)
    '''

    whole_klaytn_history = utils.read_all_history_from_file(org, repo)
    df = pd.DataFrame(whole_klaytn_history)

    new_df = df['commits'].groupby(pd.Grouper(freq='M'))
    new_df.aggregate(func=sum)
    fig = go.Figure(data=go.Line(new_df))
    fig.show()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['commits'], y=[1]*len(df['commits']),
        name='commits',
        mode='markers',
        marker_color='rgb(0, 190, 255)',
    ))
    fig.add_trace(go.Scatter(
        x=df['issues_opens'], y=[2] * len(df['issues_opens']),
        name='issues_opens',
        mode='markers',
        marker_color='rgb(255, 0, 0)',
    ))
    fig.add_trace(go.Scatter(
        x=df['issues_closes'], y=[3] * len(df['issues_closes']),
        name='issues_closes',
        mode='markers',
        marker_color='rgb(0, 255, 0)',
    ))
    fig.add_trace(go.Scatter(
        x=df['releases'], y=[4] * len(df['releases']),
        name='releases',
        mode='markers',
        marker_color='rgb(225, 0, 255)',
    ))
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
    fig.show()
    print(df)



    '''            
    releases_datetimes = repo_parsing.get_releases_datetimes(releases_history)
    with open(f'{org}_{repo}_releases.txt'.format(org=org, repo=repo), 'w') as file:
        file.truncate()
        file.write('\n'.join(releases_datetimes))

    series = pd.to_datetime(commits_dates, format='%Y-%m-%dT%H:%M:%S')
    fig = go.Figure(data=go.Scatter(x=series, y=[1] * len(series), mode='markers'))
    print(1)
    fig = go.Scatter()
    fig.show()
    '''


if __name__ == '__main__':
    main()
