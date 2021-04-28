import os

import pandas as pd

import utils
import plots
import repo_parsing
import json


def main():
    if not os.path.exists('repos_info'):
        os.mkdir('repos_info')
    org = 'solana-labs'
    repo = 'solana'

    com_rel_df, issues_df = utils.read_all_history_from_files(org, repo)
    if com_rel_df is None or issues_df is None:
        history = repo_parsing.get_all(org, repo)
        utils.write_all_history_to_files(org, repo, history)
        com_rel_df, issues_df = utils.read_all_history_from_files(org, repo)

    '''
    plots.plot([
        *plots.oc_issues(issues_df),
        plots.releases(com_rel_df),
        plots.commits(com_rel_df)
    ])
    '''
    '''
    plots.plot(
        plots.commits(com_rel_df, 'M')
    )
    '''
    plots.plot_with_slider({
        'c': plots.commits(com_rel_df, with_sliders=True),
    })


if __name__ == '__main__':
    main()
