import argparse
import json

import matplotlib.pyplot as plt
from tqdm import tqdm

from harlequin import HarlequinDataset

IMAGE_FMT = "image_{i}.png"
ANNOTATION_FMT = "annotation_{i}.png"
DATA_FMT = "data_{i}.json"


def main():
    parser = argparse.ArgumentParser(
        description="Visualize samples from the dataset.",
        epilog="""
Examples:
    python -m tools.ds_show -i 0 -v image --root data/harlequin/images --ann_file data/harlequin/annotations/instances_test.json
    python -m tools.ds_show -i 0 -v annotation --root data/harlequin/images --ann_file data/harlequin/annotations/instances_test.json
    python -m tools.ds_show -i 0 -v image -o "my_image_{i}_{id}.png" --root data/harlequin/images --ann_file data/harlequin/annotations/instances_test.json
    python -m tools.ds_show -i {0..9} -v annotation --root data/harlequin/images --ann_file data/harlequin/annotations/instances_test.json
    python -m tools.ds_show -i $(python -m tools.ds_search --search "a \w+ dog runs through a field" --idx --root data/harlequin/images --ann_file data/harlequin/annotations/instances_test.json) -v annotation --root data/harlequin/images --ann_file data/harlequin/annotations/instances_test.json""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--root", type=str, required=True, help="Path to root directory with images"
    )
    parser.add_argument(
        "--ann_file", type=str, required=True, help="Path to annotation file"
    )
    parser.add_argument(
        "-i",
        "--index",
        type=int,
        default=[0],
        nargs="+",
        help="Index of the sample to show (supports multiple indices)",
    )
    parser.add_argument(
        "-v",
        "--visualize",
        type=str,
        default="annotation",
        choices=["annotation", "image", "data"],
        help="Sample visualization mode. By default the 'annotation' is used. Three modalities are available: (1) `image` saves the PIL image without annotations, (2) `annotation` saves the matplotlib visualization of the sample with annotations, (3) `data` print sample's data to standard output.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help=f"Output path or format. By default the file will be saved with format `{IMAGE_FMT}`, `{ANNOTATION_FMT}` or `{DATA_FMT}`, depending on the mode. Available variables for formatting are: `i` for sample's index and `id` for sample's id.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Do not progress bar. Useful for batch processing.",
    )

    args = parser.parse_args()

    show_fns = {"image": show_image, "annotation": show_annotation, "data": show_data}
    show_fn = show_fns[args.visualize]

    i_list = args.index

    ds = HarlequinDataset(args.root, args.ann_file)

    for i in tqdm(i_list, disable=args.quiet):
        show_fn(ds, i, output_fmt=args.output)


def show_image(ds, i, output_fmt=None):
    if output_fmt is None:
        output_fmt = IMAGE_FMT

    sample_id = ds.get_id(i)

    output = output_fmt.format(i=i, id=sample_id)

    img = ds.get_image(sample_id)
    img.save(output)


def show_annotation(ds, i, output_fmt=None):
    sample_id = ds.get_id(i)

    if output_fmt is None:
        output_fmt = ANNOTATION_FMT

    output = output_fmt.format(i=i, id=sample_id)

    img = ds.get_image(sample_id)
    tgt_ann = ds.get_target_ann(sample_id)
    img_ann = ds.get_image_ann(sample_id)

    # print(img_ann)
    # print(tgt_ann)

    caption = img_ann["caption"]

    plt.imshow(img)

    for ann in tgt_ann:
        tokens_positive = ann["tokens_positive"][0]  # TODO: move to common func
        query = caption[tokens_positive[0] : tokens_positive[1]]

        x, y, w, h = ann["bbox"]

        plt.gca().add_patch(
            plt.Rectangle(
                (x, y), w, h, fill=False, edgecolor="b", linewidth=3, alpha=0.5
            )
        )

        plt.text(
            x,
            y,
            query,
            bbox=dict(facecolor="b", alpha=0.5),
            fontsize=12,
            color="white",
        )

    plt.title(caption)
    plt.axis("off")
    plt.savefig(output)
    plt.close()


def show_data(ds, i, output_fmt=None):
    sample_id = ds.get_id(i)

    tgt_ann = ds.get_target_ann(sample_id)
    img_ann = ds.get_image_ann(sample_id)

    output = {
        "images": [img_ann],
        "annotations": tgt_ann,
    }

    if output_fmt is None:
        output_fmt = DATA_FMT

    output_file = output_fmt.format(i=i, id=sample_id)

    with open(output_file, "w") as f:
        json.dump(output, f, indent=4)


if __name__ == "__main__":
    main()
