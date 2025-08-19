import unittest
import knmi_dataplatform_service

class TestKNMIDataplatformService(unittest.TestCase):

    def test_knmi_coll(self) -> None:
        result = knmi_dataplatform_service.KNMIDataplatformService().get_coll('2025-02-01','2025-02-10','Tx1')
        self.assertIsInstance(result, list)

    # def test_knmi_obs(self) -> None:
        # result = knmi_dataplatform.KNMIDataplatform().knmi_obs('2025-02-01','2025-02-10', 'param')
        # self.assertIsInstance(result, list)