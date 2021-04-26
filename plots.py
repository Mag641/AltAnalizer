import pandas as pd
import plotly.graph_objects as go


def plot(traces):
    all_y = []
    for trace in traces:
        all_y.extend(trace.y)
    y_upper = max(all_y)

    fig = go.Figure(layout_yaxis_range=[0, y_upper+10])
    fig.add_traces(traces)
    fig.show()


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
        x=opened_issues_datetimes,
        y=[2.1] * len(opened_issues_datetimes),
        name='opened issues',
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
        x=closed_issues_datetimes,
        y=[2] * len(closed_issues_datetimes),
        name='closed issues',
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


def commits(com_rel_df: pd.DataFrame):
    commits_datetimes = pd.Series([
        dt for i, dt
        in enumerate(com_rel_df['commits'].index)
        if not pd.isna(com_rel_df['commits'][i])
    ])
    return go.Scatter(
        x=commits_datetimes,
        y=[1.] * len(com_rel_df['commits']),
        name='commits',
        mode='markers',
        marker_color='rgb(0, 190, 255)',
        marker_line_width=2,
    )


def issues_o_dt(issues_df: pd.DataFrame):
    """
    Returns open datetimes for all issues
    :param issues_df:
    :return:
    """
    return go.Scatter(
        x=issues_df['issues_opens'], y=[2.] * len(issues_df['issues_opens']),
        name='issues opens',
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
        x=issues_df['issues_closes'],
        y=[3] * len(issues_df['issues_closes']),
        name='issues closes',
        mode='markers',
        marker_color='rgb(0, 255, 0)',
        marker_line_width=2,
    )


def releases(com_rel_df: pd.DataFrame):
    releases_datetimes = pd.Series([
        dt for i, dt
        in enumerate(com_rel_df['releases'].index)
        if not pd.isna(com_rel_df['releases'][i])
    ])
    return go.Scatter(
        x=releases_datetimes,
        y=[3] * len(com_rel_df['releases']),
        name='releases',
        mode='markers',
        marker_color='rgb(225, 0, 255)',
        marker_line_width=2,
        marker_size=12,
    )


def commits_count_grouped(com_rel_df: pd.DataFrame, by: str):
    commits_count = com_rel_df['commits'].groupby(
        pd.Grouper(freq=by)
    ).sum()
    return go.Scatter(
        x=commits_count.index,
        y=commits_count
    )


def releases_count_grouped(com_rel_df: pd.DataFrame, by: str):
    releases_count = com_rel_df['releases'].groupby(
        pd.Grouper(freq=by)
    ).sum()
    releases_count.aggregate(func=sum)
    return go.Scatter(
        x=releases_count.index,
        y=releases_count
    )


def oc_issues_corelation_grouped():
    pass
