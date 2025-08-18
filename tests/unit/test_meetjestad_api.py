import unittest
import meet_je_stad_api

class TestMeetJeStadApi(unittest.TestCase):

    def test_knmi_coll(self) -> None:
        result = meet_je_stad_api.MeetJeStadAPI().get_data('2025-02-01,12:00','2025-02-10,12:00','sensors', 'json')
        self.assertIsInstance(result, list)