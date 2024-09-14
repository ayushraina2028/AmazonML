from constants import ALL_FORMS, qty_pattern
from text_processing import MatchX
import re

def search_for_unit_in_list(match_texts: list[MatchX], num: str, full_unit: str):
    """
    Searches for the second string (number + unit) in the list after normalizing units and removing spaces.
    :param strings_list: List of strings to search through
    :param number_with_unit: String of the format 'number + unit'
    :return: List of strings where the number_with_unit is found
    """
    found_qty: list[int] = []
    for i, match in enumerate(match_texts):
        text = match.text
        for form in ALL_FORMS[full_unit]:
            # Format the number and unit without space
            pat: re.Pattern = qty_pattern(form)
            match = pat.search(text)
            if match:
                found_qty.append(i)
                break

    return found_qty

# Example usage
list_of_strings = [
    "I have a 50 cm ruler",
    "The table is 1.5 metres wide",
    "He lifted a 320 kilogram weight",  # Full form
    "The car weighs 2 tons",
    "It's 10.5 cm long"
]

# Search for "20 kg" (number + unit)
number_with_unit = "20 k9"

# Perform the search
matching_strings = search_for_unit_in_list(list_of_strings, number_with_unit)

# Output the results
print("Matching strings:", matching_strings)
