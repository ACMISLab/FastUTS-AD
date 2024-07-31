import hashlib


def get_str_hash(string):
    """
    Get the hash code of string

    Parameters
    ----------
    string : str
        The input str

    Returns
    -------
    str
        The hash code of the string

    """
    if not isinstance(string,str):
        raise ValueError(f"get_str_hash excepts str, but recept {type(string)}")
    return hashlib.sha1(string.encode("utf8")).hexdigest()
