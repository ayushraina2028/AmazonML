from constants import LABELS, CONFUSION, UNIT_PATTERNS, NUM_PATTERN, QTY_PATTERN

BBox = list[list[float]]
Match = tuple[BBox, str, float]

def get_size(bbox: BBox):
    """
    Takes the two "axes" to be the lines joining the centers of oppossite edges.
    Returns the shorter of the lengths of these.
    This is intended to be the height, though it may not be for very short text.
    """
    dx: tuple[float, float] = (bbox[1][0] + bbox[2][0] - bbox[0][0] - bbox[3][0],
                               bbox[1][1] + bbox[2][1] - bbox[0][1] - bbox[3][1])
    dy: tuple[float, float] = (bbox[2][0] + bbox[3][0] - bbox[0][0] - bbox[1][0],
                               bbox[2][1] + bbox[3][1] - bbox[0][1] - bbox[1][1])
    norm_sq = lambda v: v[0] * v[0] + v[1] * v[1]
    return min(norm_sq(dx), norm_sq(dy))

class MatchX:
    def __init__(self, match: Match, entity: str):
        self.bbox = match[0]
        self.text = match[1].lower() # redundant since matches should already be sanitized
        self.confidence = match[2]
        self.contains_label = any(label in self.text for label in LABELS[entity])
        # self.contains_unit = any(pat.search(self.text) for pat in UNIT_PATTERNS[entity])
        # self.contains_num = NUM_PATTERN.search(self.text) is not None
        self.contains_qty = QTY_PATTERN[entity].search(self.text) is not None
        self.font_size = get_size(self.bbox)

    def to_list(self) -> list[float|bool]:
        return [x for xs in self.bbox for x in xs] + [
            self.confidence,
            self.contains_label,
            # self.contains_unit,
            # self.contains_num,
            self.contains_qty
        ]

THRESHOLD = 0.5
NUM_MATCH_THRESHOLD = 20

def sanitize(img_dim: tuple[int, int], ocr: list[Match]) -> list[Match]:
    scale = lambda bbox: [[p[0] / img_dim[0], p[1] / img_dim[1]] for p in bbox]
    profuse = lambda s: ''.join(CONFUSION.get(c, c) for c in s)
    return [(scale(match[0]), profuse(match[1].lower()), match[2]) for match in ocr]

def hard_process(entity: str, ocr: list[Match]) -> list[MatchX]:
    mxs = sorted((MatchX(x, entity) for x in ocr if x[2] > THRESHOLD), key=lambda mx: mx.confidence, reverse=True)
    mxs = [mx for mx in mxs if (mx.contains_label or mx.contains_qty)][:NUM_MATCH_THRESHOLD]
    return mxs
