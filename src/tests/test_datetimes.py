from unittest import mock, TestCase

from datetime import date

from src import datetimes


@mock.patch(
    f"src.datetimes.date",
    autospec=True,
    name="datetime",
)
class GetNextMonthFirstDayTests(TestCase):
    # arbitrary
    year = 2023
    day = 12

    def test_handles_generic_month(
        self,
        mock_date: mock.MagicMock,
    ) -> None:
        # set up
        month = 6
        mock_date.today.return_value = date(
            year=self.year,
            month=month,
            day=self.day,
        )
        next_month_first_day = date(
            year=self.year,
            month=month + 1,
            day=1,
        )
        # the test itself
        self.assertEqual(
            datetimes.get_next_month_first_day(),
            next_month_first_day,
        )

    def test_handlesyear_transition(
        self,
        mock_date: mock.MagicMock,
    ) -> None:
        # set up
        mock_date.today.return_value = date(
            year=self.year,
            month=12,
            day=self.day,
        )
        next_month_first_day = date(
            year=self.year + 1,
            month=1,
            day=1,
        )
        # the test itself
        self.assertEqual(
            datetimes.get_next_month_first_day(),
            next_month_first_day,
        )
