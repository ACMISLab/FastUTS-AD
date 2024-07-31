import os
import sys

import psutil
from psutil import NoSuchProcess


def single_process_check(pid_file=None):
    """
    Check if this process has been running. Exit if it has been running, otherwise start to run it.


    Returns
    -------

    """
    if has_process_running(pid_file=pid_file):
        print(f"Process has been running at {os.getpid()} ")
        sys.exit(-1)


def set_process_title(title=None):
    """
    Set the process title as current file name
    Returns
    -------

    """
    from setproctitle import setproctitle
    if title is None:
        title = os.path.basename(sys.argv[0])
    setproctitle(title)


def has_process_running(pid_file=None):
    """
    Determines whether this process is running.

    Ensure that only one instance is running

    The principle is to record process id to a file (/tmp/sys.argv[0]).

    Returns
    -------

    """
    pid = get_process_id_from_file(pid_file)
    if pid == -1:
        flag = False
    elif pid > 0:

        try:
            pid = psutil.Process(int(pid))
            if pid.is_running():
                flag = True
            else:
                flag = False
        except NoSuchProcess:
            flag = False

    else:
        flag = False

    if not flag:
        write_process_id_to_file()

    return flag


def get_process_id_from_file(pid_file=None):
    """
    -1 means not found

    Returns
    -------

    """
    if pid_file is None:
        p_file = get_process_pid_file()
    else:
        p_file = pid_file
    if not os.path.exists(p_file):
        return -1
    with open(get_process_pid_file(), "r") as f:
        pid = f.read()
    return int(pid)


def write_process_id_to_file():
    pid = os.getpid()
    with open(get_process_pid_file(), "w") as f:
        f.write(str(pid))
    return pid


def get_process_pid_file():
    process_name = os.path.basename(sys.argv[0])
    process_file = os.path.join("/tmp", process_name + ".pid")
    return process_file
