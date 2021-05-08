import os

import plots
import repo_parsing
import utils


def main():
    if not os.path.exists('repos_info'):
        os.mkdir('repos_info')
    org = 'klaytn'
    repo = 'klaytn'

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
    plots.plot_with_slider(
        {'commits': plots.commits(com_rel_df, for_sliders=True)},
    )

    def change(obj, arg):
        print('CHANGE\nCHANGE\nCHANGE\n')
        print(obj, arg)


if __name__ == '__main__':
    main()
