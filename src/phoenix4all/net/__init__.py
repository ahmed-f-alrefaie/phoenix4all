def is_remote_url(path: str) -> bool:
    """Check if a given path is a remote URL.

    Args:
        path: The path to check.
    Returns:
        True if the path is a remote URL, False otherwise.
    """
    return path.startswith(("http://", "https://", "ftp://"))
