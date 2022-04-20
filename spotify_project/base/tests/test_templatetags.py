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
        r = display_timedelta(self.tdelta)
        days = self.tdelta.days
        hours, remain_from_hours = divmod(self.tdelta.seconds, 3600)
        minutes, seconds = divmod(remain_from_hours, 60)
        expected = f'{days} days, {str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}'
        self.assertEqual(r, expected)
