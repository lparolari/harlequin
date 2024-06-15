import unittest

from harlequin import HarlequinDataset, search


def harlequin_dataset(
    root="data/harlequin/images",
    ann_file="data/harlequin/annotations/instances_test.json",
):
    return HarlequinDataset(root, ann_file)


class TestHarlequin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.harlequin_dataset = harlequin_dataset()

    def test_search_by_string(self):
        pattern = "a blue dog runs through a field ."
        found_indices, found_ids = search(self.harlequin_dataset, pattern)
        self.assertEqual(len(found_indices), 2)
        self.assertEqual(len(found_ids), 2)
        self.assertEqual(found_indices, [1815, 1896])

    def test_search_by_regex(self):
        pattern = r"a \w+ dog runs through a field ."
        found_indices, found_ids = search(self.harlequin_dataset, pattern)
        self.assertEqual(len(found_indices), 6)
        self.assertEqual(len(found_ids), 6)
        self.assertEqual(found_indices, [1815, 1896, 2922, 4823, 6757, 9951])
