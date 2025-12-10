from unittest import TestCase

from src import iterables


class FirstWhereTests(TestCase):
    def test_finds_element(self):
        expected_element = 12
        self.assertEqual(
            iterables.first_where(
                [1, 2, expected_element, 180, 11],
                lambda x: x > 10,
                None,
            ),
            expected_element,
        )

    def test_uses_fallback(self):
        fallback = 12
        self.assertEqual(
            iterables.first_where(
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                lambda x: x > 10,
                fallback,
            ),
            fallback,
        )

    def test_raises_if_condition_not_callable(self):
        with self.assertRaises(TypeError):
            iterables.first_where([1, 2, 3], condition=True)


class ChunksTests(TestCase):
    def test_splits_into_chunks(self):
        expected_chunks = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(
            list(iterables.chunks([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)),
            expected_chunks,
        )

    def test_splits_into_chunks_with_remainder(self):
        expected_chunks = [[1, 2, 3], [4, 5, 6], [7, 8]]
        self.assertEqual(
            list(iterables.chunks([1, 2, 3, 4, 5, 6, 7, 8], 3)),
            expected_chunks,
        )
