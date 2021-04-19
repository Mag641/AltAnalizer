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


def o_issues(df: pd.DataFrame):
    """
    Returns trace with open datetimes of the issues, that are not closed yet
    :param df:
    :return:
    """
    opened_issues = pd.Series([
        open_dt
        for i, open_dt in enumerate(df['issues_opens'])
        if pd.isna(df['issues_closes'][i])
    ])
    return go.Scatter(
        x=opened_issues,
        y=[2.1] * len(opened_issues),
        name='opened issues',
        mode='markers',
        marker_color='rgb(245, 66, 66)',
        marker_line_width=2,
    )


def c_issues(df: pd.DataFrame):
    """
    Returns trace with open datetimes of the issues, that are alreayd closed
    :param df:
    :return:
    """
    closed_issues = pd.Series([
        open_dt
        for open_dt in df['issues_closes']
        if not pd.isna(open_dt)
    ])
    return go.Scatter(
        x=closed_issues,
        y=[2] * len(closed_issues),
        name='closed issues',
        mode='markers',
        marker_color='rgb(66, 245, 66)',
        marker_line_width=2,
    )


def oc_issues(df: pd.DataFrame):
    """
    Short variant for o_issues, c_issues
    :param df:
    :return:
    """
    opened_trace = o_issues(df)
    closed_trace = c_issues(df)
    return opened_trace, closed_trace


def commits(df: pd.DataFrame):
    return go.Scatter(
        x=df['commits'],
        y=[1.] * len(df['commits']),
        name='commits',
        mode='markers',
        marker_color='rgb(0, 190, 255)',
        marker_line_width=2,
    )


def issues_o_dt(df: pd.DataFrame):
    """
    Returns open datetimes for all issues
    :param df:
    :return:
    """
    return go.Scatter(
        x=df['issues_opens'], y=[2.] * len(df['issues_opens']),
        name='issues opens',
        mode='markers',
        marker_color='rgb(255, 0, 0)',
        marker_line_width=2,
    )


def issues_c_dt(df: pd.DataFrame):
    """
    Returns close datetimes for all issues
    :param df:
    :return:
    """
    return go.Scatter(
        x=df['issues_closes'],
        y=[3] * len(df['issues_closes']),
        name='issues closes',
        mode='markers',
        marker_color='rgb(0, 255, 0)',
        marker_line_width=2,
    )


def releases(df: pd.DataFrame):
    return go.Scatter(
        x=df['releases'],
        y=[3] * len(df['releases']),
        name='releases',
        mode='markers',
        marker_color='rgb(225, 0, 255)',
        marker_line_width=2,
        marker_size=12,
    )


def commits_count_grouped(df: pd.DataFrame, by: str):
    commits_count = df['commits'].groupby(pd.Grouper(freq=by))
    commits_count.aggregate(func=sum)
    fig = go.Figure(data=go.Line(commits_count))
    fig.show()
