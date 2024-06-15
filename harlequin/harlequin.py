import contextlib
import os

from torchvision.datasets import CocoDetection


class HarlequinDataset(CocoDetection):
    """
    Interface to data that follows the COCO dataset format detailed
    at https://cocodataset.org/#format-data.
    """

    def __init__(
        self, root, annFile, transform=None, target_transform=None, transforms=None
    ):
        # suppress coco prints to stdout
        with open(os.devnull, "w") as devnull:
            with contextlib.redirect_stdout(devnull):
                super().__init__(root, annFile, transform, target_transform, transforms)

    def get_target_ann(self, image_id):
        return self._load_target(image_id)

    def get_image_ann(self, image_id):
        return self.coco.loadImgs(image_id)[0]

    def get_image(self, image_id):
        return self._load_image(image_id)

    def get_id(self, index):
        return self.ids[index]

    def get_category(self, category_id):
        return self.coco.cats[category_id]["name"]


if __name__ == "__main__":
    # Run with: `python -m harlequin.harlequin --show_data`

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=str, default="data/harlequin/images/")
    parser.add_argument(
        "--ann_file", type=str, default="data/harlequin/annotations/instances_test.json"
    )
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument("--show_sample", action="store_true")
    parser.add_argument("--show_data", action="store_true")

    args = parser.parse_args()

    harlequin = HarlequinDataset(root=args.root, annFile=args.ann_file)

    if args.show_sample:
        harlequin.show_sample(args.index)

    if args.show_data:
        from pprint import pprint

        sample_id = harlequin.get_id(args.index)

        print("=========================")
        print("image")
        pprint(harlequin.get_image(sample_id))

        print("=========================")
        print("image ann")
        pprint(harlequin.get_image_ann(sample_id))

        print("=========================")
        print("target ann")
        pprint(harlequin.get_target_ann(sample_id))
