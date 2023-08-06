import os
import pytest
import tempfile

from seeq import spy

from . import test_load
from .. import Workbook, Topic
from ... import _common
from ...tests import test_common

example_export_workbooks = None


def setup_module():
    test_common.login()


# The tests for pulling workbooks are light because so much of the functionality is tested in the push code. I.e.,
# the push code wouldn't work if the pull code had a problem, since the pull code is what produced the saved workbooks.
# (Same goes for the spy.workbooks.save() functionality.)

@pytest.mark.system
def test_pull():
    push_df = spy.workbooks.push(test_load.load_example_export(), refresh=False, path='test_pull', label='test_pull')

    # Make sure the "include_references" functionality works properly by just specifying the Topic. It'll pull in
    # the Analyses
    to_pull_df = push_df[push_df['Workbook Type'] == 'Topic'].copy()

    to_pull_df.drop(columns=['ID'], inplace=True)
    to_pull_df.rename(columns={'Pushed Workbook ID': 'ID'}, inplace=True)
    to_pull_df['Type'] = 'Workbook'

    pull_workbooks = spy.workbooks.pull(to_pull_df)

    pull_workbooks = sorted(pull_workbooks, key=lambda w: w['Workbook Type'])

    analysis = pull_workbooks[0]  # type: Workbook
    assert analysis.id == (push_df[push_df['Workbook Type'] == 'Analysis'].iloc[0]['Pushed Workbook ID'])
    assert analysis.name == (push_df[push_df['Workbook Type'] == 'Analysis'].iloc[0]['Name'])
    assert len(analysis.datasource_maps) >= 3
    assert len(analysis.item_inventory) >= 25

    assert analysis['URL'] == push_df[push_df['Workbook Type'] == 'Analysis'].iloc[0]['URL']

    worksheet_names = [w.name for w in analysis.worksheets]
    assert worksheet_names == [
        'Details Pane',
        'Calculated Items',
        'Histogram',
        'Metrics',
        'Journal',
        'Global',
        'Boundaries'
    ]

    topic = pull_workbooks[1]
    worksheet_names = [w.name for w in topic.worksheets]
    assert len(topic.datasource_maps) == 3
    assert worksheet_names == [
        'Static Doc',
        'Live Doc'
    ]


@pytest.mark.system
def test_render():
    spy.workbooks.push(test_load.load_example_export(), refresh=False, path='test_render', label='test_render')

    search_df = spy.workbooks.search({
        'Workbook Type': 'Topic',
        'Path': 'test_render',
        'Name': 'Example Topic'
    }, recursive=True)

    workbooks = spy.workbooks.pull(search_df, include_rendered_content=True, include_referenced_workbooks=False,
                                   include_inventory=False)

    with tempfile.TemporaryDirectory() as temp:
        spy.workbooks.save(workbooks, temp, render_topic_documents=True)
        topic = [w for w in workbooks if isinstance(w, Topic)][0]

        topic_folder = os.path.join(temp, f'Example Topic ({topic.id})')
        assert os.path.exists(topic_folder)

        render_folder = os.path.join(topic_folder, 'RenderedTopic')
        assert os.path.exists(os.path.join(render_folder, 'index.html'))
        for worksheet in topic.worksheets:
            assert os.path.exists(os.path.join(render_folder, f'{worksheet.document.id}.html'))
            for content_image in worksheet.document.rendered_content_images.keys():
                assert os.path.exists(_common.get_image_file(render_folder, content_image))

            for static_image in worksheet.document.images.keys():
                assert os.path.exists(_common.get_image_file(render_folder, static_image))
