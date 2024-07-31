import datetime
import os.path
import sys
import time

from pysearchlib.utils.util_datatime import get_datatime
from pysearchlib.utils.util_directory import make_dirs
from pysearchlib.utils.util_system import UtilSys


class UtilComm:
    is_init = False

    @staticmethod
    def get_system_runtime():
        runtime_dir = os.path.join(os.path.expanduser("~"), "runtime")
        make_dirs(runtime_dir)
        if UtilComm.is_init is False:
            UtilComm.is_init = True
        return runtime_dir

    @staticmethod
    def get_joblib_cache_dir():
        paths = os.path.abspath(__file__).split(os.sep)
        home = os.path.join(os.sep, paths[1], paths[2], "joblib_cache")
        make_dirs(home)
        return home

    @staticmethod
    def get_backup_dir():
        paths = os.path.abspath(__file__).split(os.sep)
        home = os.path.join(os.sep, paths[1], paths[2], "backup")
        make_dirs(home)
        return home

    @staticmethod
    def get_runtime_directory():
        if UtilSys.RUNTIME_HOME is not None:
            return UtilSys.RUNTIME_HOME
        else:
            paths = os.path.abspath(__file__).split(os.sep)
            home = os.path.join(os.sep, paths[1], paths[2], paths[3], "runtime")
            make_dirs(home)
            return home

    @staticmethod
    def get_entrance_directory():
        home = os.path.abspath(os.path.dirname(sys.argv[0]))
        make_dirs(home)
        return home

    @staticmethod
    def get_file_name(filename, home=os.path.abspath(os.path.dirname(sys.argv[0]))):
        home = UtilComm.get_runtime_directory(home)
        make_dirs(home)
        return os.path.join(home, filename)

    @staticmethod
    def get_workdir(workdir, home=os.path.abspath(os.path.dirname(sys.argv[0]))):
        _dir = os.path.join(UtilComm.get_runtime_directory(home), workdir)
        make_dirs(_dir)
        return _dir

    @staticmethod
    def get_filename_entry():
        return os.path.basename(sys.argv[0])[:-3]


class UC(UtilComm):
    @classmethod
    def done(cls):
        """
        Mention that the process is finished.
        Returns
        -------

        """
        print()
        print("+" * 80)

        print("{:*^80}".format(f"Script [{os.path.basename(sys.argv[0])}] is done at {get_datatime()}"))
        print("+" * 80)
        print()


if __name__ == '__main__':
    print(UtilComm.get_filename_entry())
    UC.done()
