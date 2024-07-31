import traceback

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from typeguard import typechecked

from pysearchlib.metrics.uts.metrics import get_metrics, get_metrics_cacheable, generate_curve, UtilMetrics
from pysearchlib.utils.util_log import get_logger

log = get_logger()


class UTSMetricHelper:

    def __init__(self, window_size):
        self.window_size = window_size
        pass

    @staticmethod
    def get_metrics_all(labels, score, window_size, metric_type="all"):
        # Post-processing
        # all
        # if np.sum(labels) == 0:
        #     return None
        # try:
        #     score = MinMaxScaler(feature_range=(0, 1)).fit_transform(score.reshape(-1, 1)).ravel()
        #     return get_metrics(score, labels, metric=metric_type, window_size=window_size)
        # except:
        #     log.error(traceback.format_exc())
        #     return None
        return UTSMetricHelper.get_metrics_all_cache(labels, score, window_size, metric_type)
    @staticmethod
    def get_metrics_all_cache(labels, score, window_size, metric_type="all"):
        # Post-processing
        try:
            score = MinMaxScaler(feature_range=(0, 1)).fit_transform(score.reshape(-1, 1)).ravel()
            return get_metrics_cacheable(score, labels, metric=metric_type, window_size=window_size)
        except KeyboardInterrupt:
            return None
        except:
            print(np.max(labels), np.max(score))
            log.error(traceback.format_exc())
            return None

    @staticmethod
    def get_none_metrics():
        return {'Precision': -1, 'Recall': -1, 'F': -1, 'AUC_ROC': -1, 'AUC_PR': -1,
                'Precision_at_k': -1, 'Rprecision': -1, 'Rrecall': -1, 'RF': -1,
                'R_AUC_ROC': -1, 'R_AUC_PR': -1, 'VUS_ROC': -1, 'VUS_PR': -1}

    @staticmethod
    def vus_accuracy(score, label, window_size):
        """
        Return the VUS ROC and VUS PR scores

        VUS_ROC, VUS_PR=UTSMetricHelper.vus_accuracy()
        Parameters
        ----------
        score :
        label :
        window_size :

        Returns
        -------

        """
        # _, _, _, _, _, _, VUS_ROC, VUS_PR = generate_curve(label, score, 2 * window_size)
        score = MinMaxScaler(feature_range=(0, 1)).fit_transform(score.reshape(-1, 1)).ravel()
        tpr_3d, fpr_3d, prec_3d, window_3d, VUS_ROC, VUS_PR = UtilMetrics().RangeAUC_volume(labels_original=label,
                                                                                            score=score,
                                                                                            windowSize=2 * window_size)
        return VUS_ROC, VUS_PR

