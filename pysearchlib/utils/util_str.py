import re


def clear_str(txt):
    """
    Clear txt
    Parameters
    ----------
    str :

    Returns
    -------

    """
    return  re.sub('\\x1b', '', txt).replace("[0m","").replace("\n")
