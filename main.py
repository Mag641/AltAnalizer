import os

import plots
import repo_parsing
import utils
from IPython.display import display
import ipywidgets as widgets


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

    fig, sliders = plots.plot_with_slider({
        'commits': plots.commits(com_rel_df, for_sliders=True),
        'releases': plots.releases(com_rel_df, yaxis='y2', for_sliders=True),
    }, org, repo, show=False)

    output = widgets.Output()
    display(output)
    controls = widgets.VBox(sliders)
    with output:
        display(controls, fig)


if __name__ == '__main__':
    main()
