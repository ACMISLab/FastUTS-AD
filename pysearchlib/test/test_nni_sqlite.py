import os
from unittest import TestCase
from pysearchlib.utils.util_nni_sqlite import NNISqlite


class TestNNISqlite(TestCase):

    def test_nni_tools(self):
        experiment_working_directory = os.path.join(os.getcwd(),
                                                    "data/nnilog")
        id = "error_with_faild_trials"
        ndp = NNISqlite(experiment_working_directory=experiment_working_directory,
                        id=id)
        assert ndp.has_error() is True

    def test_nni_tools_2(self):
        experiment_working_directory = os.path.join(os.getcwd(),
                                                    "data/nnilog")
        id = "normal"
        ndp = NNISqlite(experiment_working_directory=experiment_working_directory,
                        id=id)
        assert ndp.has_error() is False

    def test_nni_tools_3(self):
        experiment_working_directory = os.path.join(os.getcwd(),
                                                    "data/nnilog")
        id = "err_connect_to_nni_server"
        ndp = NNISqlite(experiment_working_directory=experiment_working_directory,
                        id=id)
        assert ndp.has_error() is False

    def test_get_all_metrics(self):
        experiment_working_directory = os.path.join(os.getcwd(),
                                                    "data/nnilog")
        id = "normal"
        ndp = NNISqlite(experiment_working_directory=experiment_working_directory,
                        id=id)
        assert ndp.get_all_metrics().shape[0] == 32
        assert ndp.get_default_metrics().shape[0] == 32
        assert isinstance(ndp.get_mean_default_metrics(), float)

    def test_get_all_metrics1(self):
        experiment_working_directory = os.path.join(os.getcwd(),
                                                    "data/nnilog")
        id = "error_default"
        ndp = NNISqlite(experiment_working_directory=experiment_working_directory,
                        id=id)
        assert isinstance(ndp.get_mean_default_metrics(), float)

    def test_get_all_err(self):
        experiment_working_directory = os.path.join(os.getcwd(),
                                                    "data/nnilog")
        id = "xx"
        ndp = NNISqlite(experiment_working_directory=experiment_working_directory,
                        id=id)
        assert ndp.get_all_metrics().shape[0] == 32
        assert ndp.get_default_metrics().shape[0] == 32
        assert isinstance(ndp.get_mean_default_metrics(), float)

    def test_get_all_profile(self):
        experiment_working_directory = os.path.join(os.getcwd(),
                                                    "data/nnilog")
        id = "normal"
        ndp = NNISqlite(experiment_working_directory=experiment_working_directory,
                        id=id)
        print(ndp.is_all_trials_success())
        assert ndp.is_all_trials_success() is True
        assert ndp.get_max_trial_number() == 32

    def test_get_all_profile1(self):
        experiment_working_directory = os.path.join(os.getcwd(),
                                                    "data/nnilog")
        id = "failed_trials"
        ndp = NNISqlite(experiment_working_directory=experiment_working_directory,
                        id=id)
        print(ndp.get_failed_trials())
        self.assertEqual(ndp.get_failed_trials(), ['ZV0ym'])
