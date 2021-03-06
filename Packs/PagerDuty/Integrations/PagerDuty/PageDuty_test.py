# -*- coding: utf-8 -*-
from PagerDuty import get_incidents_command
from CommonServerPython import *

reload(sys)
sys.setdefaultencoding('utf8')  # pylint: disable=no-member


def test_get_incidents(requests_mock):
    """
    Given:
        - An incident with non-ascii character in its documentation

    When:
        - Running get incidents command

    Then:
        - Ensure command run without failing on UnicodeError
        - Verify the non-ascii character appears in the human readable output as expected
    """
    requests_mock.get(
        'https://api.pagerduty.com/incidents?include%5B%5D=assignees&statuses%5B%5D=triggered&statuses%5B%5D'
        '=acknowledged&include%5B%5D=first_trigger_log_entries&include%5B%5D=assignments&time_zone=UTC',
        json={
            'incidents': [{
                'first_trigger_log_entry': {
                    'channel': {
                        'details': {
                            'Documentation': '•'
                        }
                    }
                }
            }]
        }
    )
    res = get_incidents_command()
    assert '| Documentation: • |' in res['HumanReadable']
