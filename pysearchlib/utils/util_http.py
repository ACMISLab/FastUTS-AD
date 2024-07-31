import requests
from pysearchlib.utils.util_log import get_logger
import json

log = get_logger()


def http_json_get(url):
    """
    Returns the JSON representation.

    Parameters
    ----------
    url :

    Returns
    -------

    """
    try:
        req = requests.get(url)
        if req.status_code == 200:
            metric_data = json.loads(req.content)
            return metric_data
        else:
            log.error(f"Server response is {req.status_code}, expected 200.")
            return None
    except Exception as e:
        log.error(f"Url {url} is not available. \n{e.args}")
        return None
