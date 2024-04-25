import argparse
import re
from harlequin import Harlequin

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
            Search for a string in the dataset captions and print found entries.
        """
    )
    parser.add_argument("--root", type=str, help="Path to root directory with images")
    parser.add_argument("--ann_file", type=str, help="Path to annotation file")
    parser.add_argument(
        "--search", type=str, default="", help="String to search in captions"
    )
    args = parser.parse_args()

    ds = Harlequin(args.root, args.ann_file)

    pattern = re.compile(args.search, re.IGNORECASE)
    found_indices = []
    found_ids = []

    for i in range(len(ds)):
        sample_id = ds.get_id(i)
        img_ann = ds.get_image_ann(sample_id)

        caption = img_ann["caption"]

        if pattern.search(caption):
            found_indices.append(i)
            found_ids.append(sample_id)

    for i, sample_id in zip(found_indices, found_ids):
        print(f"{sample_id} ({i}): {ds.get_image_ann(sample_id)['caption']}")

    print(f"Found {len(found_ids)} entries")
