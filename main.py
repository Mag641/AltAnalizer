import os

import pandas as pd

import utils


def main():
    if not os.path.exists('repos_info'):
        os.mkdir('repos_info')
    org = 'klaytn'
    repo = 'klaytn'

    whole_klaytn_history = utils.read_all_history_from_file(org, repo)
    df = pd.DataFrame(whole_klaytn_history)

    '''
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
    fig.show()
    print(df)
    '''


if __name__ == '__main__':
    main()
