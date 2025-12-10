from unittest import TestCase

from src import iterables


class FirstWhereTests(TestCase):
    def test_finds_element(self) -> None:
        expected_element = 12
        self.assertEqual(
            iterables.first_where(
                [1, 2, expected_element, 180, 11],
                lambda x: x > 10,
                None,
            ),
            expected_element,
        )

    def test_uses_fallback(self) -> None:
        fallback = 12
        self.assertEqual(
            iterables.first_where(
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                lambda x: x > 10,
                fallback,
            ),
            fallback,
        )


class ChunksTests(TestCase):
    def test_splits_into_chunks(self) -> None:
        expected_chunks = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(
            list(iterables.chunks([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)),
            expected_chunks,
        )

    def test_splits_into_chunks_with_remainder(self) -> None:
        expected_chunks = [[1, 2, 3], [4, 5, 6], [7, 8]]
        self.assertEqual(
            list(iterables.chunks([1, 2, 3, 4, 5, 6, 7, 8], 3)),
            expected_chunks,
        )
