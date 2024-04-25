import argparse

import matplotlib.pyplot as plt
from tqdm import tqdm

from harlequin import Harlequin


IMAGE_FMT = "image_{i}.png"
ANNOTATION_FMT = "annotation_{i}.png"

def main():
    parser = argparse.ArgumentParser(
        description="Shows an example from the dataset given its index."
    )
    parser.add_argument("--root", type=str, help="Path to root directory with images")
    parser.add_argument("--ann_file", type=str, help="Path to annotation file")
    parser.add_argument(
        "-i",
        "--index",
        type=int,
        default=[0],
        nargs="+",
        help="Index of the sample to show",
    )
    parser.add_argument(
        "-v",
        "--visualize",
        type=str,
        default="annotation",
        choices=["annotation", 'image'],
        help="Sample visualization mode. Two modalities are available: (1) `image` saves the PIL image without annotations, `annotation` saves the matplotlib visualization of the sample with annotations.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help=f"Output path or format. By default the file will be saved with format `{IMAGE_FMT}` or `{ANNOTATION_FMT}`, depending on the mode. Available variables for formatting are (1) `i` for sample's index and `id` for sample's id.",
    )

    args = parser.parse_args()

    show_fn = {
        "image": show_image,
        "annotation": show_annotation,
    }[args.visualize]

    i_list = args.index

    ds = Harlequin(args.root, args.ann_file)

    for i in tqdm(i_list):
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


if __name__ == "__main__":
    """
    >>> python -m tools.ds_show --root data/refcoco_a/images  --ann_file data/refcoco_a/annotations/instances_test.json -i {0..9}
    """
    main()
