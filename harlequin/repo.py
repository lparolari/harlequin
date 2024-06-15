import re
from typing import List, Tuple, Union

from harlequin import HarlequinDataset


def search(
    ds: HarlequinDataset, pattern: Union[str, re.Pattern]
) -> Tuple[List[int], List[int]]:
    """
    Search for a string in the dataset captions and return found entries.

    Args:
        ds: HarlequinDataset instance
        pattern: str or regex, pattern to search for

    Returns:
        found_indices: list of indices of found entries
        found_ids: list of ids of found entries
    """
    pattern = re.compile(pattern) if isinstance(pattern, str) else pattern

    found_indices = []
    found_ids = []

    for i in range(len(ds)):
        sample_id = ds.get_id(i)
        img_ann = ds.get_image_ann(sample_id)

        caption = img_ann["caption"]

        if pattern.search(caption):
            found_indices.append(i)
            found_ids.append(sample_id)

    return found_indices, found_ids
