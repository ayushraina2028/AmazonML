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

unit_abbreviations: dict[str, set[str]] = {
    'centimetre': {'cm'},
    'foot': {'ft'},
    'inch': {'in'},
    'metre': {'m'},
    'millimetre': {'mm'},
    'yard': {'yd'},
    'gram': {'g'},
    'kilogram': {'kg'},
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

# all_units = {unit for entity in entity_unit_map for unit in entity_unit_map[entity]}
entity_unit_map: dict[str, set[str]] = {entity: naive_entity_unit_map[entity].union(*[unit_abbreviations[unit] for unit in naive_entity_unit_map[entity]])
    for entity in naive_entity_unit_map}

from pprint import pprint
pprint(entity_unit_map)

qty_regex = {
    # 'width': r'\d+(\.\d+)?\s*(cm|ft|in|m|mm|yd)',
    entity: rf'\d+(\.\d+)?\s*({"|".join(entity_unit_map[entity])})'
    for entity in entity_unit_map
}
pprint(qty_regex)
