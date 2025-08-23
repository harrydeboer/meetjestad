import unittest
import meet_je_stad_api_service

class TestMeetJeStadService(unittest.TestCase):

    def test_knmi_coll(self) -> None:
        result = meet_je_stad_api_service.MeetJeStadAPIService().get_data('2024-11-16,12:00',
                                                                   '2024-11-17,12:00',
                                                                   'sensors',
                                                                   'csv')
        self.assertIsInstance(result, list)