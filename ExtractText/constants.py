Entity = str
Unit = str
Label = str

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

entity_unit_map: dict[Entity, set[Unit]] = {
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

LABELS: dict[Entity, set[Label]] = {
    'width': {'width', 'size'},
    'height': {'height', 'ht', 'size'},
    'depth': {'depth'},
    'item_weight': {'weight', 'wt', 'content'},
    'maximum_weight_recommendation': {'weight', 'wt', 'content'},
    'voltage': {'voltage'},
    'wattage': {'wattage', 'power'},
    'item_volume': {'vol', 'capacity', 'size'}
}

ALL_FORMS: dict[Unit, set[Unit]] = {
    'centimetre': {'cm'},
    'foot': {'ft', 'feet', '"'},
    'inch': {'in', 'inches', "'"},
    'metre': {'m'},
    'millimetre': {'mm'},
    'yard': {'yd'},
    'gram': {'g'},
    'kilogram': {'kg', 'k9'},
    'microgram': { 'µg', 'ug' },
    'milligram': {'mg'},
    'ounce': {'oz'},
    'pound': {'lb'},
    'ton': {'t', 'tonnes'}, # t for ton?
    'kilovolt': {'kv'},
    'millivolt': {'mv'},
    'volt': {'v'},
    'kilowatt': {'kw'},
    'watt': {'w'},
    'centilitre': {'cl'},
    'cubic foot': { 'cubic feet', 'ft3' },
    'cubic inch': { 'cubic inches', 'in3' },
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
for full_unit, abbs in ALL_FORMS.items():
    abbs.add(full_unit)

for full_unit, forms in ALL_FORMS.items():
    forms = {''.join(CONFUSION.get(c, c) for c in unit) for unit in forms}
    forms = forms.union({''.join(possible_confusion.get(c, c) for c in unit) for unit in forms if len(unit) > 1})
    ALL_FORMS[full_unit] = forms

UNITS: dict[Entity, set[Unit]] = {
    entity: set.union(*[ALL_FORMS[full_unit] for full_unit in full_units])
        for entity, full_units in entity_unit_map.items()
}

import re
UNIT_PATTERNS: dict[str, set[re.Pattern]] = {
    entity: {re.compile(fr'(?<![a-z]){unit}[s]?(?![a-z])') for unit in UNITS[entity]}
        for entity in UNITS
}
NUM_PATTERN: re.Pattern = re.compile(r'\d+([\.\,]\d)?')

def qty_pattern(unit: str) -> re.Pattern:
    return re.compile(fr'(\d+(?:[\.\,]\d+)?)\s*({unit}[s]?)(?![a-z])')
QTY_PATTERN: dict[str, re.Pattern] = {
    entity: re.compile(fr'(\d+([\.\,]\d+)?)\s*({"|".join(UNITS[entity])})[s]?(?![a-z])')
        for entity in UNITS
}

if __name__ == '__main__':
    from pprint import pprint
    pprint(UNITS)
    pprint(QTY_PATTERN)