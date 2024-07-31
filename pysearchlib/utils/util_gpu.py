import subprocess
import traceback
from pysearchlib.utils.util_log import get_logger
from pysearchlib.utils.util_system import UtilSys

log = get_logger()


class UGPU:
    @staticmethod
    def get_available_memory(gpu_index):
        """
        Returns the available memory for the given GPU index.
        The units is MB.

        Parameters
        ----------
        gpu_index :

        Returns
        -------

        """
        if UtilSys.is_macos():
            UtilSys.is_debug_mode() and log.info("Skip set GPU memory since in MacOS!")
            return -1
        try:
            command = f"nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits --id={gpu_index}"
            UtilSys.is_debug_mode() and log.info("Get GPU available memory command: [{}]".format(command))
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                log.error("Get GPU available memory failed since"
                          f"[{stderr.decode().strip()}]")
                return -1
            else:
                return float(stdout.decode().strip())
        except Exception as e:

            log.error(traceback.format_exc())
            return -1


if __name__ == '__main__':
    UGPU.get_available_memory(0)
