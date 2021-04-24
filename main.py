import os

import pandas as pd

import utils
import plots
import repo_parsing
import json


def main():
    if not os.path.exists('repos_info'):
        os.mkdir('repos_info')
    org = 'klaytn'
    repo = 'klaytn'

    df = utils.read_all_history_from_files(org, repo)
    if df is None:
        history = repo_parsing.get_all(org, repo)
        utils.write_all_history_to_files(org, repo, history)
        df = utils.read_all_history_from_files(org, repo)

    plots.plot([
        *plots.oc_issues(df),
        plots.releases(df),
        plots.commits(df)]
    )

    plots.plot(plots.commits_count_grouped(df, 'M'))
    # plots.plot([plots.issues_c_dt(df)])


if __name__ == '__main__':
    main()
