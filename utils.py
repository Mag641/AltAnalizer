import json
from typing import List, Tuple

from pandas.api.extensions import no_default
import pandas as pd
from tqdm import tqdm
from constants import DATETIME_FORMAT


def log_error(error):
    with open('error.txt', 'w+') as file:
        file.write(json.dumps(error, indent=4))


def is_repo_or_owner(url: str):
    slash_count = url.count('/')
    if slash_count == 3:
        return 1
    elif slash_count == 4:
        return 2
    else:
        return None


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
    print('Transforming issues...')
    issues_count = len(data['issues'])

    timeline_start_datetime = pd.to_datetime(data['issues'][0], format=DATETIME_FORMAT)
    timeline_end_datetime = pd.to_datetime(data['issues'][-1], format=DATETIME_FORMAT)

    timeline = pd.date_range(timeline_start_datetime, timeline_end_datetime, freq=by)
    issues_grouped = {item: (0, 0) for item in timeline}

    pbar = tqdm(data['issues'])
    for i, issue in enumerate(pbar):
        pbar.set_description(f'Issue {i} of {issues_count}')

        issue_datetimes_str = issue.split(' ')
        open_datetime = pd.to_datetime(issue_datetimes_str[0], format=DATETIME_FORMAT)

        if issue_datetimes_str[1] != 'None':
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
