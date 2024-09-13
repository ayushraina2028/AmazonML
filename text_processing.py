import re
from constants import entity_unit_map, qty_regex

BBox = list[list[int]]
Match = tuple[BBox, str, float]
MatchX = tuple[Match, list[int]]

THRESHOLD = 0.5

def unit_check(entity: str):
    return lambda text: any(unit in text for unit in entity_unit_map[entity])

def qty_check(entity: str):
    return lambda text: re.search(qty_regex[entity], text)

def sanitize(img_dim: tuple[int, int], ocr: list[Match]):
    scale = lambda bbox: [[p[0] / img_dim[0], p[1] / img_dim[1]] for p in bbox]
    return [(scale(match[0]), match[1].lower(), match[2]) for match in ocr]

def get_size(bbox: BBox):
    return (bbox[2][0] - bbox[0][0]) * (bbox[2][1] - bbox[0][1])

def process(entity: str, ocr: list[Match]):
    ocrx = list(map(lambda x: (x, [0, 0, 0]), filter(lambda x: x[2] > THRESHOLD, ocr)))
    containing_entity = list(filter(lambda x: entity in x[1], ocr))
    if containing_entity:
        containing_entity = sorted(containing_entity, key=lambda x: max
    containing_unit = list(filter(unit_check(entity), ocr))
    containing_qty = list(filter(qty_check(entity), ocr))
