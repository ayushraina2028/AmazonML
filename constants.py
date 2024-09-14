naive_entity_unit_map: dict[str, set[str]] = {
    'width': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'depth': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'height': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'item_weight': {'gram',
        'kilogram',
        'microgram',
        'milligram',
        'ounce',
        'pound',
        'ton'},
    'maximum_weight_recommendation': {'gram',
        'kilogram',
        'microgram',
        'milligram',
        'ounce',
        'pound',
        'ton'},
    'voltage': {'kilovolt', 'millivolt', 'volt'},
    'wattage': {'kilowatt', 'watt'},
    'item_volume': {'centilitre',
        'cubic foot',
        'cubic inch',
        'cup',
        'decilitre',
        'fluid ounce',
        'gallon',
        'imperial gallon',
        'litre',
        'microlitre',
        'millilitre',
        'pint',
        'quart'}
}

LABELS: dict[str, set[str]] = {
    'width': {'width', 'size'},
    'height': {'height', 'ht', 'size'},
    'depth': {'depth'},
    'item_weight': {'weight', 'wt'},
    'maximum_weight_recommendation': {'weight', 'wt'},
    'voltage': {'voltage'},
    'wattage': {'wattage', 'power'},
    'item_volume': {'vol', 'capacity', 'size'}
}

unit_abbreviations: dict[str, set[str]] = {
    'centimetre': {'cm'},
    'foot': {'ft', '"'},
    'inch': {'in', "'"},
    'metre': {'m'},
    'millimetre': {'mm'},
    'yard': {'yd'},
    'gram': {'g'},
    'kilogram': {'kg', 'k9'},
    'microgram': { 'µg', 'ug' },
    'milligram': {'mg'},
    'ounce': {'oz'},
    'pound': {'lb'},
    'ton': {'t'},
    'kilovolt': {'kv'},
    'millivolt': {'mv'},
    'volt': {'v'},
    'kilowatt': {'kw'},
    'watt': {'w'},
    'centilitre': {'cl'},
    'cubic foot': { 'ft³', 'ft3' },
    'cubic inch': { 'in³', 'in3' },
    'cup': {'cup'},
    'decilitre': {'dl'},
    'fluid ounce': {'fl oz'},
    'gallon': {'gal'},
    'imperial gallon': {'imp gal'},
    'litre': {'l'},
    'microlitre': { 'µl', 'ul' },
    'millilitre': {'ml'},
    'pint': {'pt'},
    'quart': {'qt'}
}

CONFUSION: dict[str, str] = {
    'o': '0',
    'i': '1',
    's': '5',
    'b': '6',
    'q': '9',
}
possible_confusion: dict[str, str] = {
    'g': '9',
    'z': '2',
    'l': '1',
}

UNITS: dict[str, set[str]] = {entity: naive_entity_unit_map[entity].union(*[unit_abbreviations[unit] for unit in naive_entity_unit_map[entity]])
    for entity in naive_entity_unit_map}

for entity, units in UNITS.items():
    units = {''.join(CONFUSION.get(c, c) for c in unit) for unit in units}
    units = units.union({''.join(possible_confusion.get(c, c) for c in unit) for unit in units if len(unit) > 1})
    UNITS[entity] = units

from pprint import pprint
pprint(UNITS)

import re
NUM_PATTERN: re.Pattern = re.compile(r'\d+([\.\,]\d)?')
QTY_PATTERN: dict[str, re.Pattern] = {
    entity: re.compile(rf'\d+([\.\,]\d+)?\s*({"|".join(UNITS[entity])})')
        for entity in UNITS
}
pprint(QTY_PATTERN)
