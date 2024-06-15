import argparse
import re

from tabulate import tabulate

from harlequin import HarlequinDataset, search


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""
Search for a string in the dataset captions and print found entries.
Supports regex. Use `--idx` to show indices only.""",
        epilog="""
Examples:
    python -m tools.ds_search --search "a blue dog runs through a field ." --root data/harlequin/images --ann_file data/harlequin/annotations/instances_test.json 
    python -m tools.ds_search --search "a \w+ dog runs through a field ." --root data/harlequin/images --ann_file data/harlequin/annotations/instances_test.json""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--root", type=str, required=True, help="Path to root directory with images"
    )
    parser.add_argument(
        "--ann_file", type=str, required=True, help="Path to annotation file"
    )
    parser.add_argument(
        "--search",
        type=str,
        default="",
        help="String to search in captions (case insensitive, supports regex)",
    )
    parser.add_argument(
        "--idx",
        default=False,
        action="store_true",
        help="Show indices only. Could be useful in bash pipelines.",
    )
    args = parser.parse_args()

    # load the dataset
    ds = HarlequinDataset(args.root, args.ann_file)

    # perform search
    pattern = re.compile(args.search, re.IGNORECASE)
    found_indices, found_ids = search(ds, pattern)

    # print results
    if args.idx:
        print("\n".join(map(str, found_indices)))
    else:
        data = [
            {
                "sample_id": sample_id,
                "i": i,
                "caption": ds.get_image_ann(sample_id)["caption"],
            }
            for i, sample_id in zip(found_indices, found_ids)
        ]

        if len(found_ids) > 0:
            print(tabulate(data, headers="keys", numalign="left"))
        print(f"Found {len(found_ids)} entries")
