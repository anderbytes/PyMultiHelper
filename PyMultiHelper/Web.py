from bs4 import BeautifulSoup


def getElementByID(htmlContent: str,
                   elementId: str) -> dict:
    """
    Extracts details of an element with a specific ID from the given HTML content.

    Args:
        htmlContent (str): The HTML content as a string.
        elementId (str): The ID of the element to search for.

    Returns:
        dict: A dictionary containing the element's tag name, id, content and class.

    Raises:
        ValueError: If the element with the specified ID is not found.
    """
    soup = BeautifulSoup(htmlContent, 'html.parser')
    element = soup.find(id=elementId)

    if element is None:
        raise ValueError(f"Element with id '{elementId}' not found")

    # Extract specific attributes
    element_info = {
        "element": element.name,
        "id": element.get("id", None),
        "text": element.get_text(strip=True),
        "class": element.get("class", [])
    }

    return element_info


def getElementByContent(htmlContent: str,
                        textValue: str,
                        elementName: str = None) -> dict:
    """
    Extracts details of an element containing a specific text value within its content (ignores 'value' attributes).

    Args:
        htmlContent (str): The HTML content as a string.
        textValue (str): The exact text value to search for within the element's content.
        elementName (str, optional): The name of the element to filter by (e.g., 'span', 'div').

    Returns:
        dict: A dictionary containing the element's tag name, id, text content, class, and other details.

    Raises:
        ValueError: If no element with the specified text content is found,
                    if more than one element is found, or if the specified element doesn't exist.
    """
    soup = BeautifulSoup(htmlContent, 'html.parser')

    # Normalize the input textValue by stripping extra spaces
    textValue_normalized = textValue.strip()

    # Create a filter function to find elements
    def filter_elements(tag):
        # If an elementName is specified, match it
        if elementName and tag.name != elementName:
            return False
        return tag.get_text(strip=True) == textValue_normalized

    # Find all elements that contain exactly the provided text value, filtered by element name if provided
    elements = soup.find_all(filter_elements)

    if len(elements) == 0:
        raise ValueError(f"No element found with text '{textValue}'")
    elif len(elements) > 1:
        raise ValueError(f"Multiple elements found with text '{textValue}'")

    # Only one element found, extract its details
    element = elements[0]

    element_info = {
        "element": element.name,
        "id": element.get("id", None),
        "text": element.get_text(strip=True),
        "class": element.get("class", [])
    }

    return element_info
