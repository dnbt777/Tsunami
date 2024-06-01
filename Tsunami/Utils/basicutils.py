### Basic utilities used everywhere ###

import os
from bs4 import BeautifulSoup


def clean_string_for_file_system(string, max_length = 254):
    cleaned = ''.join(c for c in string if c.isalnum() or c in '._ ')
    return cleaned[:max_length]



def save_chars_as_file(chars, path_to_file, extension=".md"):
    # Check if the directory exists, if not create it
    chars = str(chars)
    directory = os.path.dirname(path_to_file)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path_to_file + extension, 'w', encoding='utf-8', errors='ignore') as file:
            file.write(chars)



def get_chars_from_file(path_to_file):
    """
    Safely reads the contents of a file and returns it as a string.
    Handles exceptions and ensures the file is properly closed after reading.
    """
    if not os.path.exists(path_to_file):
        raise FileNotFoundError(f"The file {path_to_file} does not exist.")

    try:
        with open(path_to_file, 'r', encoding='utf-8', errors="ignore") as file:
            return file.read()
    except IOError as e:
        # Handle possible I/O errors such as permission issues
        print(f"Failed to read file {path_to_file}: {e}")
        raise
    except Exception as e:
        # Handle other possible exceptions
        print(f"An error occurred while reading the file {path_to_file}: {e}")
        raise



def clean_html_string(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove all script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()
    
    # Get text from the HTML, preserving only the headers
    clean_text_parts = []
    for element in soup.body.find_all(recursive=False):
        if element.name and element.name.startswith('h'):
            # Keep headers as they are, including their tags
            clean_text_parts.append(str(element))
        else:
            # Extract text from other elements
            clean_text_parts.append(element.get_text())
    
    # Combine all parts into a single string
    clean_text = '\n'.join(clean_text_parts)
    
    return clean_text
