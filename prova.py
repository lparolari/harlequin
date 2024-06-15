from harlequin import HarlequinDataset

ds = HarlequinDataset(
    "data/harlequin/images", "data/harlequin/annotations/instances_test.json"
)

i = 0  # simulating a training setp

sample_id = ds.get_id(i)

img = ds.get_image(sample_id)
img_ann = ds.get_image_ann(sample_id)
tgt_ann = ds.get_target_ann(sample_id)

# harlequin comes with both captions and queries,
# we can extract queries from caption using indexes
caption = img_ann["caption"]
queries = [
    caption[query_pos[0] : query_pos[1]]
    for tgt in tgt_ann
    if (query_pos := tgt["tokens_positive"][0])
]

print(type(img))
# The man with a gray jacket and cyan sunglasses is holding cameras and standing in front of a car .

print(img_ann.keys())
# ['cyan sunglasses', 'a gray jacket', 'cameras', 'a car', 'The man']

# each target has a bounding box associated, identifying it in the image
print(tgt_ann[0].keys())

print(boxes)
# [[222, 120, 115, 35], [53, 164, 438, 292], [83, 336, 356, 136], [1, 372, 464, 139], [56, 70, 432, 441]]
