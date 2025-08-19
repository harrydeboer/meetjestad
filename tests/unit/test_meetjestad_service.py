import unittest
import meet_je_stad_service

class TestMeetJeStadService(unittest.TestCase):

    def test_knmi_coll(self) -> None:
        result = meet_je_stad_service.MeetJeStadService().get_data('2017-11-16,12:00','2017-11-16,12:15','sensors', 'json', '11,14,19,26,31,37,41,47')
        self.assertIsInstance(result, list)