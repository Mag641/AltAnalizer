import repo_parsing


def main():
    org = 'klaytn'
    repo = 'klaytn'

    whole_klaytn_history = repo_parsing.get_all(org, repo)
    for key, value in whole_klaytn_history:
        with open(f'{org}_{repo}_{key}.txt'.format(org=org, repo=repo, key=key), 'w') as file:
            file.truncate()
            file.write('\n'.join(value))


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
