import unittest
from unittest.mock import MagicMock
from pyvdr import PYVDR
from pyvdr import pyvdr
from pyvdr.svdrp import response_data


class TestPYVDR(unittest.TestCase):
    def setUp(self):
        self.func = PYVDR()
        self.func.stat = MagicMock(return_value=3)
        self.func.is_recording = MagicMock(
            return_value=[
                '220 easyVDR SVDRP VideoDiskRecorder 2.2.0; Sun Sep  1 16:27:17 2019; UTF-8']
        )

    def test__parse_channel_response(self):
        chan_ard = self.func._parse_channel_response(["", "", "1 ARD"])
        self.assertEqual(chan_ard['number'], "1")
        self.assertEqual(chan_ard['name'], "ARD")

        chan_prosieben = self.func._parse_channel_response(["", "", "11 Pro Sieben"])
        self.assertEqual(chan_prosieben['number'], "11")
        self.assertEqual(chan_prosieben['name'], "Pro Sieben")

    def test__check_timer_recording_flag(self):
        t_active = {}
        t_inactive = {}
        t_active_and_recording = {}
        t_active_and_instant_recording = {}
        t_active.update(
            {
                'status': 1,
                'name': "Test1",
                'description': "Description1",
                'date': "2018-08-01"
            })
        t_inactive.update(
            {
                'status': 1,
                'name': "Test1",
                'description': "Description1",
                'date': "2018-08-01"
            })
        t_active_and_recording.update(
            {
                'status': 9,
                'name': "t_active_and_recording",
                'description': "Description1",
                'date': "2018-08-01"
            })
        t_active_and_instant_recording.update(
            {
                'status': 11,
                'name': "t_active_and_instantrecording",
                'description': "Description1",
                'date': "2018-08-01"
            })

        # timer active, not yet recording
        self.assertTrue(self.func._check_timer_recording_flag(t_active, pyvdr.FLAG_TIMER_ACTIVE), "Timer should be active")
        self.assertFalse(self.func._check_timer_recording_flag(t_active, pyvdr.FLAG_TIMER_RECORDING), "Timer should not be recording")

        # timer active, recording
        self.assertTrue(self.func._check_timer_recording_flag(t_active_and_recording, pyvdr.FLAG_TIMER_ACTIVE), "Timer should be active")
        self.assertTrue(self.func._check_timer_recording_flag(t_active_and_recording, pyvdr.FLAG_TIMER_RECORDING), "Timer should be recording")

        # instant recording
        self.assertTrue(self.func._check_timer_recording_flag(t_active_and_instant_recording, pyvdr.FLAG_TIMER_RECORDING), "Timer active")
        self.assertTrue(self.func._check_timer_recording_flag(t_active_and_instant_recording, pyvdr.FLAG_TIMER_RECORDING), "Timer recording")
        self.assertTrue(self.func._check_timer_recording_flag(t_active_and_instant_recording, pyvdr.FLAG_TIMER_INSTANT_RECORDING), "Timer instant recording")

    def test__parse_timer_responses(self):
        parseable_responses = [
            response_data(
                "250",
                "-",
                "3 1:7:2020-07-13:1858:2025:50:99:Das perfekte Dinner~2020.07.13-19|00-Mo:<epgsearch><channel>7 - VOX</channel><searchtimer>das perfekte dinner</searchtimer><start>1594659480</start><stop>1594664700</stop><s-id>0</s-id><eventid>4572</eventid></epgsearch>"
            ),
            response_data(
                "250",
                "-",
                "3 1:17:2020-07-31:0243:0345:50:99:Bad Banks~Ein halbes Jahr ist seit dem Crash der DGI-Bank vergangen. Gabriel Fenger befindet sich noch immer in U-Haft.:<epgsearch><channel>17 - ZDF_neo HD</channel><searchtimer>Bad Banks</searchtimer><start>1596156180</start><stop>1596159900</stop><s-id>8</s-id><eventid>4357</eventid></epgsearch>"
            ),
            response_data(
                "250",
                "-",
                "4 11:1:2020-07-08:2215:0145:50:99:@Tagesthemen mit Wetter:"
            )
        ]
        expected_parsed_timers = [
            {
                'status': '1',
                'channel': '7',
                'date': '2020-07-13',
                'name': 'Das perfekte Dinner~2020.07.13-19|00-Mo',
                'description': '',
                'series': True,
                'instant': False
            },
            {
                'status': '1',
                'channel': '17',
                'date': '2020-07-31',
                'name': 'Bad Banks~Ein halbes Jahr ist seit dem Crash der DGI-Bank vergangen. Gabriel Fenger befindet sich noch immer in U-Haft.',
                'description': '',
                'series': True,
                'instant': False
            },
            {
                'status': '11',
                'channel': '1',
                'date': '2020-07-08',
                'name': '@Tagesthemen mit Wetter',
                'description': '',
                'series': False,
                'instant': False
            }
        ]

        for i in range(len(parseable_responses)):
            timer = self.func._parse_timer_response(parseable_responses[i])
            self.assertEqual(
                timer,
                expected_parsed_timers[i]
            )


if __name__ == '__main__':
    unittest.main()
