import repo_parsing
import json
import os
import utils


def main():
    org = 'klaytn'
    repo = 'klaytn'

    issues_history = repo_parsing.get_history(org, repo, 'commits')
    if not os.path.exists('repos_info'):
        os.mkdir('repos_info')
    if not os.path.exists(f'repos_info/{org}_{repo}'):
        os.mkdir(f'repos_info/{org}_{repo}')

    issues_formatted = repo_parsing.get_issues_datetimes(issues_history)
    utils.write_issues_to_file(org, repo, issues_formatted)

    '''
    releases_datetimes = repo_parsing.get_releases_datetimes(releases_history)
    with open(f'{org}_{repo}_releases.txt'.format(org=org, repo=repo), 'w') as file:
        file.truncate()
        file.write('\n'.join(releases_datetimes))
    '''
    '''
    whole_klaytn_history = repo_parsing.get_all(org, repo)
    for key, value in whole_klaytn_history:
        with open(f'{org}_{repo}_{key}.txt'.format(org=org, repo=repo, key=key), 'w') as file:
            file.truncate()
            file.write('\n'.join(value))
    '''

    #  with open('{org}_{repo}_commits.txt'.format(org=org, repo=repo), 'r') as file:
    #    commits_dates = file.readlines()

    '''
    series = pd.to_datetime(commits_dates, format='%Y-%m-%dT%H:%M:%S')
    fig = go.Figure(data=go.Scatter(x=series, y=[1] * len(series), mode='markers'))
    print(1)
    fig = go.Scatter()
    fig.show()
    '''


if __name__ == '__main__':
    main()
