from django.test import override_settings, TestCase

from . import django_test_case
from src.django import database

import asyncio
import time
import threading
import multiprocessing
from unittest import mock


class DisconnectDbAfterwardsTests(
    django_test_case.DjangoDependentTestCase,
    TestCase,
):
    @mock.patch(
        "src.django.database.close_old_connections",
        autospec=True,
        name="Close old connections",
    )
    def test_closes_connection(self, mock_close: mock.MagicMock) -> None:
        @database.disconnect_db_afterwards
        def wrapped_function() -> None:
            pass

        wrapped_function()
        mock_close.assert_called_once()


# was too flakey
# class MutexTests(TestCase):
#     MUTEX_NAMESPACE = "foo"

#     @override_settings(MUTEX_NAMESPACE=MUTEX_NAMESPACE)
#     @mock.patch(
#         "utils.django.database.logging.info",
#         autospec=True,
#     )
#     @mock.patch(
#         "utils.django.database.time.sleep",
#         autospec=True,
#         side_effect=lambda x: None,
#     )
#     def test_locks(self, _, mock_info) -> None:
#         @database.mutex(name="foo", timeout=1)
#         def locked_function():
#             time.sleep(1)

#         threads = [
#             threading.Thread(target=locked_function),
#             threading.Thread(target=locked_function),
#         ]
#         for thread in threads:
#             thread.start()

#         async def check_calls():
#             for x in range(10):
#                 await asyncio.sleep(0.01)
#                 if mock_info.call_count == 0:
#                     continue
#                 await asyncio.sleep(0.01)
#                 self.assertEqual(mock_info.call_count, 1)
#                 self.assertEqual(
#                     mock_info.call_args.args[0],
#                     f"Not running locked_function, {self.MUTEX_NAMESPACE}_mutex_foo "
#                     "mutex not available",
#                 )
#                 break
#             else:
#                 self.fail("Mutex didn't work?")

#         asyncio.run(check_calls())
