import unittest
from PIL import Image

from harlequin import Harlequin


def harlequin_dataset(
    root="data/harlequin/images",
    ann_file="data/harlequin/annotations/instances_test.json",
):
    return Harlequin(root, ann_file)


class TestHarlequin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.harlequin_dataset = harlequin_dataset()

    def test_getitem_return_tuple(self):
        self.assertIsInstance(self.harlequin_dataset[0], tuple)
        self.assertEqual(len(self.harlequin_dataset[0]), 2)

    def test_getitem_tuple_has_image(self):
        self.assertIsInstance(self.harlequin_dataset[0][0], Image.Image)

    def test_getitem_tuple_has_target(self):
        target = self.harlequin_dataset[0][1]

        self.assertIsInstance(target, list)

        target0 = target[0]

        self.assertIsInstance(target0, dict)
        self.assertIn("area", target0)
        self.assertIn("iscrowd", target0)
        self.assertIn("image_id", target0)
        self.assertIn("bbox", target0)
        self.assertIn("category_id", target0)
        self.assertIn("id", target0)

        bbox = target0["bbox"]

        self.assertIsInstance(bbox, list)
        self.assertEqual(len(bbox), 4)

    def test_get_id(self):
        self.assertEqual(
            self.harlequin_dataset.get_id(0), self.harlequin_dataset.ids[0]
        )

    def test_get_image_return_image(self):
        self.assertEqual(
            self.harlequin_dataset.get_image(self.harlequin_dataset.ids[0]),
            self.harlequin_dataset[0][0],
        )

    def test_get_image_ann_return_image_ann(self):
        image_ann = self.harlequin_dataset.coco.loadImgs(self.harlequin_dataset.ids[0])[
            0
        ]

        self.assertEqual(
            self.harlequin_dataset.get_image_ann(self.harlequin_dataset.ids[0]),
            image_ann,
        )

    def test_get_target_ann_return_target(self):
        self.assertEqual(
            self.harlequin_dataset.get_target_ann(self.harlequin_dataset.ids[0]),
            self.harlequin_dataset[0][1],
        )
