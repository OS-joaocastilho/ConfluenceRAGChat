import os


def load_atlassian_api_key():
    """
    Load the Atlassian API key from environment variables.

    Returns:
        str: The Atlassian API key retrieved from the environment.

    Raises:
        KeyError: If "ATLASSIAN_API_KEY" is not set in the environment variables.
    """
    return os.environ["ATLASSIAN_API_KEY"]


def load_atlassian_username():
    """
    Load the Atlassian username from environment variables.

    Returns:
        str: The Atlassian username retrieved from the environment.

    Raises:
        KeyError: If "ATLASSIAN_USERNAME" is not set in the environment variables.
    """
    return os.environ["ATLASSIAN_USERNAME"]
