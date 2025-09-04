import unittest
import knmi_dataplatform_api_service

class TestKNMIDataplatformAPIService(unittest.TestCase):

    def test_get_coll(self) -> None:
        service = knmi_dataplatform_api_service.KNMIDataplatformAPIService()
        result = service.get_coll('2025-02-01',
                                  '2025-02-10',
                                  'Tx1',
                                  'csv')
        self.assertListEqual(result, [])

        result = knmi_dataplatform_api_service.KNMIDataplatformAPIService().get_coll('2025-02-01',
                                                                                     '2025-02-10',
                                                                                     'Tx1',
                                                                                     'json')
        self.assertEqual(len(result[0]), 2)
