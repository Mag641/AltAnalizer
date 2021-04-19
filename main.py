import os

import pandas as pd

import utils
import plots
import repo_parsing


def main():
    if not os.path.exists('repos_info'):
        os.mkdir('repos_info')
    org = 'ethereum'
    repo = 'go-ethereum'

    whole_history = utils.read_all_history_from_file(org, repo)
    if not whole_history:
        history = repo_parsing.get_all(org, repo)
        utils.write_all_history_to_files(org, repo, history)
        whole_history = utils.read_all_history_from_file(org, repo)
    df = pd.DataFrame(whole_history)

    plots.plot([
        *plots.oc_issues(df),
        plots.releases(df),
        plots.commits(df)]
    )

    plots.plot(plots.commits_count_grouped(df, 'M'))
    # plots.plot([plots.issues_c_dt(df)])

    '''
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
    fig.show()
    print(df)
    '''


if __name__ == '__main__':
    main()
