import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tqdm import tqdm
from constants import FREQUENCIES, START_FREQUENCIES_INDICES
from utils import freq_to_human_readable


def plot(traces):
    if type(traces) == list:
        all_y = []
        for trace in traces:
            all_y.extend(trace.y)
        y_upper = max(all_y)
    else:
        y_upper = max(traces.y)

    fig = go.Figure(layout_yaxis_range=[0, y_upper + 10])
    fig.add_traces(traces)
    fig.show()


def plot_with_slider(traces):
    if 'releases' in traces.keys():
        fig = make_subplots(specs=[[{"secondary_y": True}]])
    else:
        '''
        y_upper = max([
            max(trace.y)
            for trace in traces
        ])
        fig = go.Figure(layout_yaxis_range=[0, y_upper + 10])
        '''
        fig = go.Figure()

    for target, traces_pack in traces.items():
        traces_pack[
            START_FREQUENCIES_INDICES[target]
        ].visible = True
        if target == 'releases':
            for trace in traces_pack:
                fig.add_trace(trace, secondary_y='True')
        else:
            fig.add_traces(traces_pack)

    traces_packs_steps = []
    for traces_pack in traces.values():
        steps = [
            dict(
                method="update",
                args=[
                    {"visible": [False] * len(traces_pack)},
                    {"title": "Slider switched to step: " + freq_to_human_readable(freq)}
                ],
            )  # layout attribute
            for trace, freq in zip(traces_pack, FREQUENCIES)
        ]

        for i, step in enumerate(steps):
            step['args'][0]['visible'][i] = True
        traces_packs_steps.append(steps)

    sliders = [
        dict(
            active=START_FREQUENCIES_INDICES[target],
            currentvalue={"prefix": "Frequency: "},
            pad={'t': 20 * (i + 1)},
            steps=traces_packs_steps[i],
        ) for i, target in enumerate(traces.keys())
    ]
    fig.update_layout(
        sliders=sliders
    )

    fig.show(config={'scrollZoom': True})


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


def commits(com_rel_df: pd.DataFrame, by=None, for_sliders=False):
    # TODO: What is better, own return for each case or one return in the end.
    if by is None:
        # Without grouping
        if for_sliders:
            traces = []
            for freq in tqdm(FREQUENCIES, desc='Preparing plots...'):
                traces.append(
                    target_grouped_by('commits', com_rel_df, freq, False)
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
                mode='markers',
                marker_color='rgb(0, 190, 255)',
                marker_line_width=2,
            )
    else:
        # With grouping
        return target_grouped_by(com_rel_df, com_rel_df, by)


def releases(com_rel_df: pd.DataFrame, by=None, for_sliders=False):
    if by is None:
        # Without grouping
        if for_sliders:
            traces = []
            for freq in tqdm(FREQUENCIES, desc='Preparing plots...'):
                traces.append(
                    target_grouped_by('releases', com_rel_df, freq, False)
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
                mode='markers',
                marker_color='rgb(225, 0, 255)',
                marker_line_width=2,
            )
    else:
        # With grouping
        return target_grouped_by('releases', com_rel_df, by)


def target_grouped_by(target, com_rel_df: pd.DataFrame, by: str, visible=True):
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
