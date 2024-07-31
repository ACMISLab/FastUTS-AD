import pprint
import re
import subprocess
import sys
import time
import traceback
import warnings

from pysearchlib.utils.util_log import get_logger
from pysearchlib.utils.util_system import UtilSys

log = get_logger()


class CMD:
    @staticmethod
    def exe_cmd(command, home=None, check=False, timeout=None):
        """
        Timeout in seconds.

        Parameters
        ----------
        command :
        home :
        check :
        timeout : int
            Timeout in seconds.

        Returns
        -------

        """
        if home is not None:
            command = f"cd {home};{command}"
        UtilSys.is_debug_mode() and log.info(f"Exec command: \n{command} ")
        var = subprocess.run([f"{command}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             encoding="utf-8", timeout=timeout, check=check)
        if var.returncode != 0:
            warnings.warn(var.stderr.strip())
            return None
        else:
            res = var.stdout.strip()
            return res

    @staticmethod
    def run_command_print_progress(cmd):
        """
        实时输出执行结果
        Parameters
        ----------
        cmd :

        Returns
        -------

        """
        UtilSys.is_debug_mode() and log.info(f"Exec command: \n{cmd}\n")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # out = []
        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                msg = output.strip().decode("utf-8")
                # out.append(msg)
                print(msg)
            # time.sleep(0.5)
        rc = process.poll()
        if rc != 0:
            print("Exec command error: ", process.stderr.readlines(), file=sys.stderr)
            return None
        return None


class BashUtil(CMD):
    pass


class UtilBash(CMD):
    pass


class UtilCMD(CMD):
    pass


def get_bash_result(command, check=True):
    var = subprocess.run([f"{command}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         encoding="utf-8", timeout=10, check=check)

    ret = re.sub('\\x1b', '', var.stdout)
    return ret.split("\n")


def exec_cmd(command, check=False, print_result=False, split_to_array=True):
    """
    Exec command.

    ret stdout,stderr
    Parameters
    ----------
    split_to_array :bool
    print_result : bool
    show_command : bool
        Decided whether to show the exec command.
    command : str
        The command to execute
    check : bool
        The check option in subprocess.run

    Returns
    -------
    list
        stdout
    list
        stderr
    """
    UtilSys.is_debug_mode() and log.info(f"Exec command: \n{pprint.pformat(command)}")
    var = subprocess.run([f"{command}"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         encoding="utf-8", timeout=60, check=check)
    stdout = precess_std_results(var.stdout)
    stderr = precess_std_results(var.stderr)
    if var.returncode != 0:
        log.error(f"Exec command err:\n{stderr}")
    else:
        UtilSys.is_debug_mode() and log.info(f"Exec command success:\n{stderr}")

    if split_to_array:
        return stdout.split("\n"), stderr.split("\n")
    else:
        return stdout, stderr


def precess_std_results(res):
    return re.sub('\\x1b', '', res).replace("[0m", "").replace("[31m", "").replace("[39m", "")


def exec_cmd_return_stdout_and_stderr(command, retry=10, retry_interval=3, check=True, timeout=60):
    """
    Exec command.

    ret stdout,stderr
    Parameters
    ----------
    retry : int
        How many times to retry when command is failed
    command : str
        The command to execute
    retry_interval: int
        The interval between each retry

    Returns
    -------
    str
        stdout + stderr
    """
    for i in range(retry):
        try:
            UtilSys.is_debug_mode() and log.info(f"Exec command: \n{pprint.pformat(command)}")
            var = subprocess.run(
                [f"{command}"],
                shell=True,
                encoding="utf-8",
                timeout=timeout,
                check=check,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            )
            stdout = re.sub('\\x1b', '', var.stdout).replace("[0m", "")
            stderr = re.sub('\\x1b', '', var.stderr).replace("[0m", "")
            return stdout, stderr
        except Exception as e:
            log.warning(f"Execute command [{command}] failed, retry {i}/{retry} after {retry_interval} seconds."
                        f"\n Caused by {e}")
            traceback.print_exc()
            time.sleep(retry_interval)
    errmsg = f"Execute [{command}] error after retry {retry} times"
    log.error(errmsg)
    raise RuntimeError(errmsg)


def exec_cmd_and_return_str(command, retry=10, retry_interval=3, check=True, timeout=60):
    stdout, stderr = exec_cmd_return_stdout_and_stderr(command=command, retry=retry, retry_interval=retry_interval,
                                                       check=check, timeout=timeout)
    return stdout + stderr


def clear_cmd_output(output):
    return re.sub('\\x1b', '', output).replace("[0m", "").replace("\n", "")


if __name__ == '__main__':
    CMD.run_command_print_progress("xping www.baidu.com")
    CMD.run_command_print_progress("ping www.baidu.com")
