from unittest import TestCase

from datetime import \
    datetime, \
    timedelta

from rsm.override.rsmutils import RsmUtils


today = datetime.now()

#from rsm.override.rsm import RsmBase
#from rsm.override.rsmsdk import RsmSDK

# class TestClasses(TestCase):
#     def test_cls_rsmbase(self):
#         with self.assertRaises(NameError):
#             RsmBase()
#
#     def test_cls_rsmsdk(self):
#         assert RsmSDK()
#
#     def test_cls_rsmutils(self):
#         assert RsmUtils()
#


class TestRsmUtils(TestCase):
    def test_convert_string_to_unix_time(self):
        result = RsmUtils.convert_string_to_unix_time(str(today))
        print(result)
        assert result

    def test_convert_datetime_to_unix_time(self):
        result = RsmUtils.convert_datetime_to_unix_time(today)
        print(result)
        assert result

    def test_convert_string_to_datetime(self):
        result = RsmUtils.convert_string_to_datetime(str(today))
        print(result)
        assert result

    def test_convert_unixtime_to_datetime(self):
        result = RsmUtils.convert_unixtime_to_datetime(int(today.timestamp()))
        print(result)
        assert result

    def test_validate_timestamp_no_offset(self):
        self.assertEqual(today, RsmUtils.validate_timestamp(today, offset=0))

    def test_validate_timestamp_offset(self):
        self.assertEqual(first=today - timedelta(days=1),
                         second=RsmUtils.validate_timestamp(today - timedelta(days=1), offset=1))
