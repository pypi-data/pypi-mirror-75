import os
import time

import pandas as pd

from seeq import spy
from seeq.spy import _login
from seeq.spy.workbooks import Analysis
from seeq.sdk import *


def login(url=None):
    key_path = os.path.join(get_test_data_folder(), 'keys', 'agent.key')
    credentials = open(key_path, "r").read().splitlines()

    spy.login(credentials[0], credentials[1], url=url)

    wait_for_example_data()


def get_client():
    return _login.client


def get_test_data_folder():
    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'sq-run-data-dir'))


def wait_for(boolean_function):
    start = time.time()
    while True:
        if boolean_function():
            break

        if time.time() - start > 240:
            return False

        time.sleep(1.0)

    return True


def wait_for_example_data():
    if not wait_for(is_example_data_indexed):
        raise Exception("Timed out waiting for Example Data to finish indexing")


def is_example_data_indexed():
    # noinspection PyBroadException
    try:
        agents_api = AgentsApi(_login.client)
        agent_status = agents_api.get_agent_status()
        for agents in agent_status:
            if 'JVM Agent' in agents.id:
                if agents.status != 'CONNECTED':
                    return False

                for connection in agents.connections:
                    if 'Example Data' in connection.name and \
                            connection.status == 'CONNECTED' and \
                            connection.sync_status == 'SYNC_SUCCESS':
                        return True

    except BaseException:
        return False

    return False


def create_worksheet_for_url_tests():
    search_results = spy.search({
        'Name': 'Temperature',
        'Path': 'Example >> Cooling Tower 1 >> Area A'
    })

    display_items = pd.DataFrame([{
        'Type': 'Signal',
        'Name': 'Temperature Minus 5',
        'Formula': '$a - 5',
        'Formula Parameters': {
            '$a': search_results.iloc[0]
        }
    }, {
        'Type': 'Condition',
        'Name': 'Cold',
        'Formula': '$a.validValues().valueSearch(isLessThan(80))',
        'Formula Parameters': {
            '$a': search_results.iloc[0]
        }
    }, {
        'Type': 'Scalar',
        'Name': 'Constant',
        'Formula': '5',
    }])

    push_df = spy.push(metadata=display_items, workbook=None)

    workbook = Analysis({
        'Name': 'test_items_from_URL'
    })

    worksheet = workbook.worksheet('search from URL')
    worksheet.display_range = {
        'Start': '2019-01-01T00:00Z',
        'End': '2019-01-02T00:00Z'
    }
    worksheet.display_items = push_df

    spy.workbooks.push(workbook)

    return workbook
