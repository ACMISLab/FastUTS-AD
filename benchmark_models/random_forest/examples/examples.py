from sklearn.preprocessing import MinMaxScaler

from benchmark_models.random_forest.random_forest_conf import RandomForestConf
from benchmark_models.random_forest.random_forest_model import RandomForestModel
from pysearchlib.share.dataset_loader import DatasetLoader, DataDEMOKPI
from pysearchlib.metrics.uts.uts_metric_helper import UTSMetricHelper

window_size = 99
for dataset, data_id in DataDEMOKPI.DEMO_KPIS:
    dl = DatasetLoader(dataset, data_id, window_size=window_size, is_include_anomaly_window=True, max_length=10000)
    train_x, train_y = dl.get_sliding_windows()

    modelName = 'IForest'
    conf = RandomForestConf()
    clf = RandomForestModel(conf)
    clf.fit(train_x, train_y)
    score = clf.score(train_x)
    # Post-processing
    score = MinMaxScaler(feature_range=(0, 1)).fit_transform(score.reshape(-1, 1)).ravel()
    from pysearchlib.utils.util_univariate_time_series_view import UnivariateTimeSeriesView

    uv = UnivariateTimeSeriesView(name=data_id, is_save_fig=True)
    # uv.plot_x_label_score_row2(train_x[:, -1], train_y, score)

    metrics = UTSMetricHelper.get_metrics_all(train_y, score, window_size=window_size)
    uv.plot_x_label_score_metrics_row2(train_x[:, -1], train_y, score, metrics)
    print(metrics)
