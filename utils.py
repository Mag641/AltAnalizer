import json


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
