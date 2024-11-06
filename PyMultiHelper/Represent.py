def traverseJSON(data: dict | list) -> None:
    """
    Recursively prints the keys and values of a JSON structure.

    This function traverses a JSON-like dictionary or list and prints the keys
    in a hierarchical format. If the value is not a dict or list, it prints the key along with its value.

    Args:
        data (dict or list): The JSON to traverse.

    Raises:
        TypeError: If 'data' is not a dict or list.

    Returns:
        None
    """

    # Validate input type: must be either dict or list
    if not isinstance(data, (dict, list)):
        raise TypeError(f"Expected 'dict' or 'list', but received {type(data).__name__}")

    def _print_keys(innerData, prefix=""):
        if isinstance(innerData, dict):
            for key, value in innerData.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                # Print key and value if it's not a list or dict
                if not isinstance(value, (list, dict)):
                    print(f"{new_prefix}  -->  {value}")
                # Recursively call the function for nested dicts or lists
                _print_keys(value, new_prefix)

        elif isinstance(innerData, list):
            for index, item in enumerate(innerData):
                new_prefix = f"{prefix}[{index}]"
                # Print item if it's not a list or dict
                if not isinstance(item, (list, dict)):
                    print(f"{new_prefix}  -->  {item}")
                # Recursively call the function for nested dicts or lists
                _print_keys(item, new_prefix)

    # Call the inner function to start the recursion
    _print_keys(data)