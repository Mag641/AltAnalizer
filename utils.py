import json
import os
import time
from typing import List, Tuple

import pandas as pd
from pandas.api.extensions import no_default
from tqdm import tqdm

from constants import DATETIME_FORMAT, TARGETS


def check_dir_exist(org: str, repo: str):
    if not os.path.exists(f'repos_info/{org}_{repo}'):
        os.mkdir(f'repos_info/{org}_{repo}')


def log_error(error):
    with open('error.txt', 'w+') as file:
        file.write(json.dumps(error, indent=4))


def is_repo_or_owner_url(url: str):
    slash_count = url.count('/')
    if slash_count == 3:
        return 1
    elif slash_count == 4:
        return 2
    else:
        return None


def series_from_file(org, repo, target: str):
    from repo_parsing import get_history, get_commits_datetimes, get_issues_datetimes, get_releases_datetimes
    try:
        with open(f'repos_info/{org}_{repo}/{org}_{repo}_{target}.txt', 'r') as file:
            history_str = file.readlines()
    except FileNotFoundError:
        if target == 'issues_opens' or target == 'issues_closes':
            issues_history = get_history(org, repo, 'issues')
            issues_opens, issues_closes = get_issues_datetimes(issues_history)
            data = {
                'issues_opens': issues_opens,
                'issues_closes': issues_closes,
            }
        else:
            history = get_history(org, repo, target)
            get_datetimes_func = locals()[f'get_{target}_datetimes']
            history_datetimes = get_datetimes_func(history)
            data = {target: history_datetimes}
        write_all_history_to_files(org, repo, data)
        with open(f'repos_info/{org}_{repo}/{org}_{repo}_{target}.txt', 'r') as file:
            history_str = file.readlines()

    index = [
        pd.to_datetime(
            dt.rstrip('\n'), format=DATETIME_FORMAT
        )
        for dt in history_str
    ]
    history = pd.Series([1] * len(index), index=index, name=target)
    history.sort_index(ascending=False, inplace=True)
    return history


def read_all_history_from_files(org: str, repo: str):
    # TODO: Refactor and rename all things like 'commits_HISTORY', 'commits_DATETIMES', 'DATETIMES' and so on
    if not os.path.exists(f'repos_info/{org}_{repo}'):
        return None
    com_rel_series_dict = {}  # dict, containing series of commits and releases
    issues_series_dict = {}
    for target in TARGETS:
        s = series_from_file(org, repo, target)
        if 'issues' in target:
            s = pd.Series(s.index, name=s.name)
            issues_series_dict[target] = s
        else:
            com_rel_series_dict[target] = s

    com_rel_df = pd.DataFrame(com_rel_series_dict)
    com_rel_df = com_rel_df.astype(float)

    issues_df = pd.DataFrame(issues_series_dict)

    return com_rel_df, issues_df


def write_all_history_to_files(org, repo, whole_history):
    for key, value in whole_history.items():
        with open(f'repos_info/{org}_{repo}/{org}_{repo}_{key}.txt', 'w') as file:
            file.truncate()
            file.write('\n'.join(value))


def write_issues_to_file(org: str, repo: str, issues_formatted: List[Tuple]):
    print('Writing issues to file...')
    with open(f'repos_info/{org}_{repo}/{org}_{repo}_issues.txt', 'w') as file:
        file.truncate()
        issues_count = len(issues_formatted)
        pbar = tqdm(issues_formatted)
        for i, issue in enumerate(pbar):
            pbar.set_description(f'Issue {i + 1} of {issues_count}')
            file.write(f'{issue[0]} {issue[1]}\n')


def groupby(
        data: pd.DataFrame = None,
        by=None,
        axis=0,
        level=None,
        as_index: bool = True,
        sort: bool = True,
        group_keys: bool = True,
        squeeze: bool = no_default,
        observed: bool = False,
        dropna: bool = True,
):
    timeline_start_datetime = pd.to_datetime(data['issues'][0], format=DATETIME_FORMAT)
    timeline_end_datetime = pd.to_datetime(data['issues'][-1], format=DATETIME_FORMAT)

    timeline = pd.date_range(timeline_start_datetime, timeline_end_datetime, freq=by)
    issues_grouped = {item: (0, 0) for item in timeline}

    for issue in tqdm(data['issues'], desc='Transforming issues...'):
        issue_datetimes_str = issue.split(' ')
        open_datetime = pd.to_datetime(issue_datetimes_str[0], format=DATETIME_FORMAT)

        if issue_datetimes_str[1] != '':
            close_datetime = pd.to_datetime(issue_datetimes_str[1], format=DATETIME_FORMAT)
            found_close = False
            for datetime in timeline:
                if not found_close:
                    if close_datetime <= datetime:
                        issues_grouped[datetime][1] += 1
                        found_close = True
                if open_datetime <= datetime:
                    issues_grouped[datetime][0] += 1
                    break
        else:
            for datetime in timeline:
                if open_datetime <= datetime:
                    issues_grouped[datetime][0] += 1
                    break


def process_http_error(e):
    if e.response.status_code == 502:
        print('Bad Gateway(502)!')
        time.sleep(1)
    else:
        print(e.response.json())
        for _ in tqdm(range(30), desc='Waiting...'):
            time.sleep(1)


def _check_for_duplicates(commits_with_info):
    for i, dt in enumerate(tqdm(commits_with_info['dts'])):
        for j, another_dt in enumerate(commits_with_info['dts'][i + 1:]):
            if dt == another_dt:
                print(f'{i} = {i + 1 + j} {dt}')
                for key in commits_with_info['info'][i].keys():
                    print(f'{key}:\t{commits_with_info["info"][i][key]}\t{commits_with_info["info"][i + 1 + j][key]}')
