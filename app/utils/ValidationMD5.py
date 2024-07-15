import hashlib


# Define a function to generate the MD5 hash of a file
def gen_md5_file(filepath):
    """
    This function generates the MD5 hash of a file.

    Parameters:
    filepath (str): The path to the file.

    Returns:
    str: The MD5 hash of the file.
    """
    # Initialize a new MD5 hash object
    hasher = hashlib.md5()

    # Open the file in binary mode
    with open(filepath, 'rb') as archivo:
        # Read the file in chunks of 8192 bytes
        while chunk := archivo.read(8192):
            # Update the hash object with each chunk
            hasher.update(chunk)
    # Return the hexadecimal representation of the hash
    return hasher.hexdigest()


# Define a function to generate the MD5 hash of a content string
def gen_md5_content(content, excel=False):
    """
    This function generates the MD5 hash of a content string.

    Parameters:
    content (str): The content string.
    excel (bool, optional): A flag indicating whether the content is from an Excel file. Defaults to False.

    Returns:
    str: The MD5 hash of the content.
    """
    # Initialize a new MD5 hash object
    hasher = hashlib.md5()
    # If the content is not from an Excel file
    if not excel:
        # Update the hash object with the encoded content
        hasher.update(content.encode('utf-8'))
    else:
        # Update the hash object with the content
        hasher.update(content)

    # Return the hexadecimal representation of the hash
    return hasher.hexdigest()