import os

import ipywidgets as widgets

import plots
import repo_parsing
import utils
from constants import FREQUENCIES

if not os.path.exists('repos_info'):
    os.mkdir('repos_info')
org = 'klaytn'
repo = 'klaytn'

com_rel_df, issues_df = utils.read_all_history_from_files(org, repo)
if com_rel_df is None or issues_df is None:
    history = repo_parsing.get_all(org, repo)
    utils.write_all_history_to_files(org, repo, history)
    com_rel_df, issues_df = utils.read_all_history_from_files(org, repo)

fig, slider = plots.plot_with_slider({
    'commits': plots.commits(com_rel_df, for_sliders=True),
}, show=False)


def change_trace(slider_value):
    freq = utils.human_readable_to_freq(slider_value)
    trace_index = FREQUENCIES.index(freq)

    with fig.batch_update():
        # print([trace.visible for trace in fig.data])
        for trace in fig.data:
            trace.visible = False
        # fig.show()
        # print([trace.visible for trace in fig.data])

        chosen_trace = fig.data[trace_index]
        print(chosen_trace.name, chosen_trace.visible)
        chosen_trace.visible = True
    print(chosen_trace.visible)
    fig.show()

print(slider.value)
print(slider.value in slider.options)
widgets.interact(change_trace, slider_value=slider)
