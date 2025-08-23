import unittest
import knmi_dataplatform_api_service

class TestKNMIDataplatformAPIService(unittest.TestCase):

    def test_knmi_coll(self) -> None:
        result = knmi_dataplatform_api_service.KNMIDataplatformAPIService().get_coll('2025-02-01',
                                                                              '2025-02-10',
                                                                              'Tx1',
                                                                              'csv')
        self.assertIsInstance(result, list)
