from datetime import datetime


def convert_timestamp_to_minutes(timestamp):
    if timestamp > 1000 ** 3:
        return timestamp / 1000 ** 3


class UtilTime:
    @staticmethod
    def convert_datatime_to_timestamp(time_str):
        return convert_datatime_to_timestamp(time_str)


def convert_datatime_to_timestamp(time_str: str):
    """
    input:
    2023-10-07 17:48:06

    Returns:
    1696672086.0

    -------

    """
    format_str = "%Y-%m-%d %H:%M:%S"
    timestamp = datetime.strptime(time_str, format_str).timestamp()
    return timestamp


def convert_timestamp_to_datetime(timestamp_str: float):
    """
    input:
    1696673086.0

    output:

    Returns
    -------

    """
    # from datetime import datetime

    # timestamp = 1696673086.0
    format_str = "%Y-%m-%d %H:%M:%S"
    assert len(str(timestamp_str)) <= 12, "The given timestamp is error."

    datetime_obj = datetime.fromtimestamp(timestamp_str)
    time_str = datetime_obj.strftime(format_str)
    return time_str
