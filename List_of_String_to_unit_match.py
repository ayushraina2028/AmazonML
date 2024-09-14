import re


# We are taking a list of strings, and a string, the output is a list of strings which matched.


# Example usage
# list_of_strings = [
#     "I have a 50 cm ruler",
#     "The table is 1.5 metres wide",
#     "He lifted a 20 kilogram weight",  # Full form
#     "The car weighs 2 tons",
#     "It's 10.5 cm long",
#     "She lifted a 20 kg weight",  # Abbreviation
# ]

# # Search for "20 kg" (number + unit)
# number_with_unit = "20 k9"


# Matching strings: ['He lifted a 20 kilogram weight', 'She lifted a 20 kg weight']


# Dictionary of unit abbreviations, including full forms and abbreviations


unit_abbreviations = {
    'centimetre': {'cm', 'centimetre'},
    'foot': {'ft', '"', 'foot'},
    'inch': {'in', "'", 'inch'},
    'metre': {'m', 'metre'},
    'millimetre': {'mm', 'millimetre'},
    'yard': {'yd', 'yard'},
    'gram': {'g', 'gram'},
    'kilogram': {'kg', 'k9', 'kilogram'},
    'microgram': {'µg', 'ug', 'microgram'},
    'milligram': {'mg', 'milligram'},
    'ounce': {'oz', 'ounce'},
    'pound': {'lb', 'pound'},
    'ton': {'t', 'ton'},
    'kilovolt': {'kv', 'kilovolt'},
    'millivolt': {'mv', 'millivolt'},
    'volt': {'v', 'volt'},
    'kilowatt': {'kw', 'kilowatt'},
    'watt': {'w', 'watt'},
    'centilitre': {'cl', 'centilitre'},
    'cubic foot': {'ft³', 'ft3', 'cubic foot'},
    'cubic inch': {'in³', 'in3', 'cubic inch'},
    'cup': {'cup'},
    'decilitre': {'dl', 'decilitre'},
    'fluid ounce': {'fl oz', 'fluid ounce'},
    'gallon': {'gal', 'gallon'},
    'imperial gallon': {'imp gal', 'imperial gallon'},
    'litre': {'l', 'litre'},
    'microlitre': {'µl', 'ul', 'microlitre'},
    'millilitre': {'ml', 'millilitre'},
    'pint': {'pt', 'pint'},
    'quart': {'qt', 'quart'}
}

def normalize_unit(unit):
    """ Normalize the unit by converting the full form or abbreviation into possible variants """
    for full_unit, abbreviations in unit_abbreviations.items():
        if unit == full_unit or unit in abbreviations:
            return abbreviations
    return {unit}

def remove_spaces(s):
    """ Remove all spaces in a string """
    return s.replace(' ', '')

def search_for_unit_in_list(strings_list, number_with_unit):
    """
    Searches for the second string (number + unit) in the list after normalizing units and removing spaces.
    :param strings_list: List of strings to search through
    :param number_with_unit: String of the format 'number + unit'
    :return: List of strings where the number_with_unit is found
    """
    # Extract the number and unit from the input string
    match = re.match(r'(\d+(?:\.\d+)?)\s*([a-zA-Zµ\'"³³]+)', number_with_unit)
    if not match:
        return []

    number = match.group(1)
    unit = match.group(2)

    # Normalize unit (to handle abbreviations and full names)
    possible_units = normalize_unit(unit)

    # Remove spaces in strings and search for the formatted number and unit
    found_strings = []
    for string in strings_list:
        normalized_string = remove_spaces(string)
        
        for normalized_unit in possible_units:
            # Format the number and unit without space
            search_term = f"{number}{normalized_unit}"
            if search_term in normalized_string:
                found_strings.append(string)
                break  # Break once we find a match in the string

    return found_strings

# Example usage
list_of_strings = [
    "I have a 50 cm ruler",
    "The table is 1.5 metres wide",
    "He lifted a 20 kilogram weight",  # Full form
    "The car weighs 2 tons",
    "It's 10.5 cm long"
]

# Search for "20 kg" (number + unit)
number_with_unit = "20 k9"

# Perform the search
matching_strings = search_for_unit_in_list(list_of_strings, number_with_unit)

# Output the results
print("Matching strings:", matching_strings)
