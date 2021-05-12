from functools import partial

import ipywidgets as widgets
import pandas as pd
import plotly.graph_objects as go
from tqdm import tqdm

from constants import FREQUENCIES, DEFAULT_FREQUENCIES, DEFAULT_FREQUENCIES_INDICES
from utils import freq_to_human_readable, human_readable_to_freq


def _switch_trace(fig, slider_num, sliders_count, slider_value):
    freq = human_readable_to_freq(slider_value['new'])
    traces_pack_start_index = int((len(fig.data) / sliders_count) * slider_num)
    trace_index = traces_pack_start_index + FREQUENCIES.index(freq)
    next_traces_pack_index = traces_pack_start_index + len(FREQUENCIES)
    with fig.batch_update():
        for i, trace in enumerate(fig.data[traces_pack_start_index: next_traces_pack_index]):
            j = i + traces_pack_start_index
            if j == trace_index:
                trace.visible = True
            else:
                trace.visible = False


def _create_grouping_slider(value, target):
    return widgets.SelectionSlider(
        options=[
            freq_to_human_readable(freq)
            for freq in FREQUENCIES
        ],
        value=value,
        description=f'Group {target} by:',
        disabled=False,
        continuous_update=True,
        orientation='horizontal',
        readout=True
    )


def _calc_y_upper(traces):
    y_upper = max([
        max(trace.y)
        for trace in traces
    ])
    return y_upper


def plot(traces):
    if isinstance(traces, list):
        y_upper = _calc_y_upper(traces)
    else:
        y_upper = max(traces.y)

    fig = go.Figure(layout_yaxis_range=[0, y_upper + 10])
    fig.add_traces(traces)
    fig.show()


def plot_with_slider(traces_packs_dict, org: str, repo: str, show=True):
    if 'releases' in traces_packs_dict.keys():
        layout = go.Layout(
            yaxis=dict(
                zeroline=True,
                showline=True
            ),
            yaxis2=dict(
                zeroline=True,
                showline=True,
                overlaying='y',
                side='right'
            )
        )
        fig = go.FigureWidget(layout=layout)
        fig.layout.yaxis2.title = 'releases number'
    else:
        fig = go.FigureWidget()

    traces_packs_count = len(traces_packs_dict)
    sliders = []
    for i, pair in enumerate(traces_packs_dict.items()):
        target, traces_pack = pair

        target_default_plot_index = DEFAULT_FREQUENCIES_INDICES[target]
        traces_pack[target_default_plot_index].visible = True
        fig.add_traces(traces_pack)

        sliders.append(
            _create_grouping_slider(
                value=freq_to_human_readable(
                    DEFAULT_FREQUENCIES[target]
                ),
                target=target
            )
        )
        switch_trace = partial(_switch_trace, fig, i, traces_packs_count)
        sliders[-1].observe(switch_trace, 'value')

    fig.layout.title = f'{org}/{repo} history'
    if show:
        fig.show(config={
            'scrollZoom': True,
            'displaylogo': False,
            'displayModeBar': True,
        })
    else:
        return fig, sliders


def o_issues(issues_df: pd.DataFrame):
    """
    Returns trace with open datetimes of the issues, that are not closed yet
    :param issues_df:
    :return:
    """
    opened_issues_datetimes = pd.Series([
        open_dt
        for i, open_dt in enumerate(issues_df['issues_opens'])
        if pd.isna(issues_df['issues_closes'][i])
    ])
    return go.Scatter(
        name='opened issues',
        x=opened_issues_datetimes,
        y=[2.1] * len(opened_issues_datetimes),
        mode='markers',
        marker_color='rgb(245, 66, 66)',
        marker_line_width=2,
    )


def c_issues(issues_df: pd.DataFrame):
    """
    Returns trace with open datetimes of the issues, that are alreayd closed
    :param issues_df:
    :return:
    """
    closed_issues_datetimes = pd.Series([
        open_dt
        for i, open_dt in enumerate(issues_df['issues_opens'])
        if not pd.isna(issues_df['issues_closes'][i])
    ])
    return go.Scatter(
        name='closed issues',
        x=closed_issues_datetimes,
        y=[2] * len(closed_issues_datetimes),
        mode='markers',
        marker_color='rgb(66, 245, 66)',
        marker_line_width=2,
    )


def oc_issues(issues_df: pd.DataFrame):
    """
    Short variant for o_issues, c_issues
    :param issues_df:
    :return:
    """
    opened_trace = o_issues(issues_df)
    closed_trace = c_issues(issues_df)
    return opened_trace, closed_trace


def issues_o_dt(issues_df: pd.DataFrame):
    """
    Returns open datetimes for all issues
    :param issues_df:
    :return:
    """
    return go.Scatter(
        name='issues opens',
        x=issues_df['issues_opens'],
        y=[2.] * len(issues_df['issues_opens']),
        mode='markers',
        marker_color='rgb(255, 0, 0)',
        marker_line_width=2,
    )


def issues_c_dt(issues_df: pd.DataFrame):
    """
    Returns close datetimes for all issues
    :param issues_df:
    :return:
    """
    return go.Scatter(
        name='issues closes',
        x=issues_df['issues_closes'],
        y=[3] * len(issues_df['issues_closes']),
        mode='markers',
        marker_color='rgb(0, 255, 0)',
        marker_line_width=2,
    )


def commits(com_rel_df: pd.DataFrame, by=None, yaxis=None, for_sliders=False):
    # TODO: What is better, own return for each case or one return in the end.
    if by is None:
        # Without grouping
        if for_sliders:
            traces = []
            for freq in tqdm(FREQUENCIES, desc='Preparing plots...'):
                traces.append(
                    target_grouped_by('commits', com_rel_df, freq, yaxis, False)
                )
            return traces
        else:
            # Just all commits
            commits_datetimes = pd.Series([
                dt for i, dt
                in enumerate(com_rel_df['commits'].index)
                if not pd.isna(com_rel_df['commits'][i])
            ])
            return go.Scatter(
                name='commits',
                x=commits_datetimes,
                y=[1.] * len(com_rel_df['commits']),
                yaxis=yaxis,
                mode='markers',
                marker_color='rgb(0, 190, 255)',
                marker_line_width=2,
            )
    else:
        # With grouping
        return target_grouped_by(com_rel_df, com_rel_df, by)


def releases(com_rel_df: pd.DataFrame, by=None, yaxis=None, for_sliders=False):
    if by is None:
        # Without grouping
        if for_sliders:
            traces = []
            for freq in tqdm(FREQUENCIES, desc='Preparing plots...'):
                traces.append(
                    target_grouped_by('releases', com_rel_df, freq, yaxis, False)
                )
            return traces
        else:
            # Just all commits
            releases_datetimes = pd.Series([
                dt for i, dt
                in enumerate(com_rel_df['releases'].index)
                if not pd.isna(com_rel_df['releases'][i])
            ])
            return go.Scatter(
                name='releases',
                x=releases_datetimes,
                y=[3] * len(com_rel_df['releases']),
                yaxis=yaxis,
                mode='markers',
                marker_color='rgb(225, 0, 255)',
                marker_line_width=2,
            )
    else:
        # With grouping
        return target_grouped_by('releases', com_rel_df, by)


def target_grouped_by(target, com_rel_df: pd.DataFrame, by: str, yaxis=None, visible=True):
    commits_count = com_rel_df[target].groupby(
        pd.Grouper(freq=by)
    ).sum()

    freq_human = freq_to_human_readable(by)
    if freq_human:
        target += f' per {freq_human}'
    return go.Scatter(
        name=target,
        visible=visible,
        x=commits_count.index,
        y=commits_count,
        yaxis=yaxis
    )


'''
def commits_grouped_by(com_rel_df: pd.DataFrame, by: str, visible=True):
    name = 'commits'
    commits_count = com_rel_df[name].groupby(
        pd.Grouper(freq=by)
    ).sum()

    freq_human = freq_to_human_readable(by)
    if freq_human:
        name += f' per {freq_human}'
    return go.Scatter(
        name=name,
        visible=visible,
        x=commits_count.index,
        y=commits_count,
    )


def releases_count_grouped(com_rel_df: pd.DataFrame, by: str):
    name = 'releases'
    releases_count = com_rel_df['releases'].groupby(
        pd.Grouper(freq=by)
    ).sum()

    freq_human = freq_to_human_readable(by)
    if freq_human:
        name += f' per {freq_human}'
    return go.Scatter(
        name=name,
        x=releases_count.index,
        y=releases_count,
    )


def oc_issues_corelation_grouped():
    pass
'''
