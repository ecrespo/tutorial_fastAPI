from .ValidationMD5 import gen_md5_content


# Define a function to validate the content of a file
def validation_content(content, excel=False):
    """
    This function validates the content of a file by generating its MD5 hash.

    Parameters:
    content (str): The content of the file to validate.
    excel (bool, optional): A flag indicating whether the file is an Excel file. Defaults to False.

    Returns:
    str: The MD5 hash of the content.
    """

    # Generate and return the MD5 hash of the content
    return gen_md5_content(content, excel=excel)