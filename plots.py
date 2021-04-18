import pandas as pd
import plotly.graph_objects as go


def plot_opened_closed_issues(df: pd.DataFrame):
    not_closed_issues = pd.Series([
        open_dt
        for i, open_dt in enumerate(df['issues_opens'])
        if pd.isna(df['issues_closes'][i])
    ])
    closed_issues = pd.Series([
        open_dt
        for open_dt in df['issues_opens']
        if open_dt not in not_closed_issues
    ])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=not_closed_issues,
        y=[1] * len(not_closed_issues),
        name='opened',
        mode='markers',
        marker_color='rgb(245, 149, 66)'
    ))
    fig.add_trace(go.Scatter(
        x=closed_issues,
        y=[1] * len(closed_issues),
        name='opened',
        mode='markers',
        marker_color='rgb(66, 245, 66)'
    ))
    fig.show()


def plot_commits_history(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['commits'],
        y=[1] * len(df['commits']),
        name='commits',
        mode='markers',
        marker_color='rgb(0, 190, 255)'
    ))
    fig.show()


def plot_issues_opens_history(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['issues_opens'], y=[2] * len(df['issues_opens']),
        name='issues_opens',
        mode='markers',
        marker_color='rgb(255, 0, 0)',
    ))
    fig.show()


def plot_issues_closes_history(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['issues_closes'],
        y=[3] * len(df['issues_closes']),
        name='issues_closes',
        mode='markers',
        marker_color='rgb(0, 255, 0)',
    ))
    fig.show()


def plot_relases_history(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['releases'],
        y=[4] * len(df['releases']),
        name='releases',
        mode='markers',
        marker_color='rgb(225, 0, 255)',
    ))
    fig.show()


def plot_commits_count_history(df: pd.DataFrame, by: str):
    commits_count = df['commits'].groupby(pd.Grouper(freq=by))
    commits_count.aggregate(func=sum)
    fig = go.Figure(data=go.Line(commits_count))
    fig.show()
