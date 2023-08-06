from datetime import datetime
import json
from unittest import TestCase

from dhooks_lite.serializers import JsonDateTimeEncoder

from . import set_test_logger

MODULE_PATH = 'dhooks_lite.serializers'
logger = set_test_logger(MODULE_PATH, __file__)


class TestJsonDateTimeEncoder(TestCase):

    def test_encode(self):

        my_date = datetime(2020, 8, 3, 16, 5, 0)
        my_dict = {"alpha": "dummy", "bravo": my_date}

        result = json.loads(json.dumps(my_dict, cls=JsonDateTimeEncoder))        
        self.assertEqual(result, {"alpha": "dummy", "bravo": "2020-08-03T16:05:00"})

