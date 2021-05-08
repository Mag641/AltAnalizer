USERNAME = 'Mag641'
TOKEN = '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'
AUTH_PARAMS = (USERNAME, TOKEN)

MAIN_URL = 'https://github.com'

API_MAIN_URL = 'https://api.github.com'
ORG_EVENTS_END = '/orgs/{}/events'
REPO_END = '/repos/{}/{}'

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

eth_repo = 'https://github.com/ethereum/go-ethereum'
klaytn_reop = 'https://github.com/klaytn/klaytn'

TARGETS = ('commits', 'issues_opens', 'issues_closes', 'releases')


def _generate_freqs():
    frequencies = []
    letters = ['D', 'W', 'M', 'Q']
    numbers_ranges = [range(1, 7), range(1, 4), range(1, 12), range(1, 4)]
    for numbers_range, letter in zip(numbers_ranges, letters):
        for number in numbers_range:
            if number == 1:
                frequencies.append(letter)
            else:
                frequencies.append(str(number) + letter)
    return frequencies


FREQUENCIES = _generate_freqs()
FREQUENCIES_HUMAN = {
    'D': 'days',
    'W': 'weeks',
    'SM': 'semi-months',
    'M': 'months',
    'Q': 'quarters',
}

START_FREQUENCIES = {
    'commits': '2W',
    'issues_opens': 'W',
    'issues_closes': 'W',
    'releases': '3M'
}

START_FREQUENCIES_INDICES = {
    key: FREQUENCIES.index(value)
    for key, value in START_FREQUENCIES.items()
}
