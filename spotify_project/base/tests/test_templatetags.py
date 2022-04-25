from datetime import timedelta
from random import randint

from base.templatetags.date_utils import display_timedelta
from testing import BaseTestCase


class DateUtilsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.input_seconds = randint(86400, int(8.64e7 - 1))
        self.tdelta = timedelta(seconds=self.input_seconds)

    def test_time_with_days(self):
        test_delta = timedelta(seconds=10000000)
        r = display_timedelta(test_delta)
        expected = '115 days, 17:46:40'
        self.assertEqual(r, expected)
