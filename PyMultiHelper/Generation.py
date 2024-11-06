import random
import string

def generateRandomString(length: int,
                          allowNumbers: bool = True,
                          allowSpecialChars: bool = True,
                          requireNumbers: bool = False,
                          requireSpecialChars: bool = False,
                          allowedSpecialChars: str = "",
                          forbiddenChars: str = "",
                          requiredChars: str = "") -> str:
    """
    Generates a random string of a specified length with configurable character options.

    Args:
        length (int): The length of the generated string. Must be greater than or equal to the number of distinct characters in requiredChars.
        allowNumbers (bool, optional): Whether to include numbers. Defaults to True.
        requireNumbers (bool, optional): Whether at least one number must be included. Defaults to False.
        allowSpecialChars (bool, optional): Whether to include special characters. Defaults to False.
        requireSpecialChars (bool, optional): Whether at least one special character must be included. Defaults to False.
        allowedSpecialChars (str, optional): Additional special characters to include in the generation.
        forbiddenChars (str, optional): Characters that should not be included in the generation.
        requiredChars (str, optional): Characters that must be included in the generated string.

    Returns:
        str: The generated random string.

    Raises:
        ValueError: If no valid characters are available for string generation, or if the length is less than the number of distinct required characters,
                    or if contradictory options are provided for number or special character requirements.
    """
    # Remove duplicates from requiredChars and convert to list
    requiredCharsList: list[str] = list(set(requiredChars))

    # Check if length is valid
    if length < len(requiredCharsList):
        raise ValueError("Length must be greater than or equal to the number of distinct required characters.")

    # Check for contradictory options
    if not allowNumbers and requireNumbers:
        raise ValueError("Cannot require numbers when numbers are not allowed.")
    if not allowSpecialChars and requireSpecialChars:
        raise ValueError("Cannot require special characters when special characters are not allowed.")

    # Start building the base character set
    characters = string.ascii_letters  # Always include letters

    if allowNumbers:
        characters += string.digits  # Include numbers if allowed

    # Only include allowed special characters if specified
    if allowSpecialChars:
        characters += allowedSpecialChars  # Include only the allowed special characters

    # Remove forbidden characters
    characters = ''.join(c for c in characters if c not in forbiddenChars)

    # Ensure all characters are unique
    characters = ''.join(set(characters))

    if not characters:  # Ensure there's at least one character to sample from
        raise ValueError("No valid characters available for string generation.")

    # Generate the random string ensuring required characters are included
    result = list(requiredCharsList)  # Start with all required characters

    # Add at least one number if required
    if requireNumbers:
        possible_numbers = [c for c in string.digits if c not in forbiddenChars]
        if not possible_numbers:
            raise ValueError("Cannot fulfill the requirement for numbers with the given options.")
        result.append(random.choice(possible_numbers))

    # Add at least one special character if required
    if requireSpecialChars:
        possible_specials = [c for c in allowedSpecialChars if c not in forbiddenChars]
        if not possible_specials:
            raise ValueError("Cannot fulfill the requirement for special characters with the given options.")
        result.append(random.choice(possible_specials))

    # Calculate remaining length available for random characters
    remaining_length = length - len(result)

    if remaining_length < 0:
        raise ValueError("The total of required characters exceeds the specified length.")

    # Fill the rest of the string with random choices if remaining length is greater than 0
    result += [random.choice(characters) for _ in range(remaining_length)] if remaining_length > 0 else []

    # Shuffle the result to ensure randomness
    random.shuffle(result)

    return ''.join(result)