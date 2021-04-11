import json
from tqdm import tqdm
from typing import List, Tuple


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
            pbar.set_description(f'Issue {i+1} of {issues_count}')
            file.write(f'{issue[0]} {issue[1]}\n')
