import json
import os

import ipywidgets as widgets
from IPython.display import display
from ipywidgets.embed import embed_data

import plots
import repo_parsing
import utils
from interactivity.html_template import html_template


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

    data = embed_data(views=sliders)

    manager_state = json.dumps(data['manager_state'], default=str)
    widget_views = [json.dumps(view) for view in data['view_specs']]
    rendered_template = html_template.format(manager_state=manager_state, widget_views=widget_views)
    with open(r'interactivity\rendered_template.html', 'w') as file:
        file.write(rendered_template)
    fig_json = fig.to_json()
    with open(r'interactivity\fig_JSON.txt', 'w') as file:
        file.write(json.dumps(fig_json, indent=4))
    fig.write_html(r'interactivity\fig_html_full', full_html=True)
    fig.write_html(r'interactivity\fig_html')

    with output:
        display(controls, fig)


if __name__ == '__main__':
    main()
