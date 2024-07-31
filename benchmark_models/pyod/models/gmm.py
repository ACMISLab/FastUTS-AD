# -*- coding: utf-8 -*-
"""
Outlier detection based on Gaussian Mixture Model (GMM).
"""
# Author: Akira Tamamori <tamamori5917@gmail.com>
# License: BSD 2 clause

from __future__ import division, print_function

from sklearn.mixture import GaussianMixture
from sklearn.utils import check_array
from sklearn.utils.validation import check_is_fitted

from pyod.models.base import BaseDetector
from pyod.utils.utility import invert_order


class GMM(BaseDetector):
    """Wrapper of scikit-learn Gaussian Mixture Model with more functionalities.
    Unsupervised Outlier Detection.

    See :cite:`aggarwal2015outlier` Chapter 2 for details.

    Parameters
    ----------
    n_components : int, default=1
        The number of mixture components.

    covariance_type : {'full', 'tied', 'diag', 'spherical'}, default='full'
        String describing the type of covariance parameters to use.

    tol : float, default=1e-3
        The convergence threshold. EM iterations will stop when the
        lower bound average gain is below this threshold.

    reg_covar : float, default=1e-6
        Non-negative regularization added to the diagonal of covariance.
        Allows to assure that the covariance matrices are all positive.

    max_iter : int, default=100
        The number of EM iterations to perform.

    n_init : int, default=1
        The number of initializations to perform. The best results are kept.

    init_params : {'kmeans', 'random'}, default='kmeans'
        The method used to initialize the weights, the means and the
        precisions.

    weights_init : array-like of shape (n_components, ), default=None
        The user-provided initial weights.
        If it is None, weights are initialized using the `init_params` method.

    means_init : array-like of shape (n_components, n_features), default=None
        The user-provided initial means,
        If it is None, means are initialized using the `init_params` method.

    precisions_init : array-like, default=None
        The user-provided initial precisions (inverse of the covariance
        matrices).
        If it is None, precisions are initialized using the 'init_params'
        method.

    random_state : int, RandomState instance or None, default=None
        Controls the random seed given to the method chosen to initialize the
        parameters.

    warm_start : bool, default=False
        If 'warm_start' is True, the solution of the last fitting is used as
        initialization for the next call of fit().

    verbose : int, default=0
        Enable verbose output.

    verbose_interval : int, default=10
        Number of iteration done before the next print.

    contamination : float in (0., 0.5), optional (default=0.1)
        The amount of contamination of the data set.

    Attributes
    ----------
    weights_ : array-like of shape (n_components,)
        The weights of each mixture components.

    means_ : array-like of shape (n_components, n_features)
        The mean of each mixture component.

    covariances_ : array-like
        The covariance of each mixture component.

    precisions_ : array-like
        The precision matrices for each component in the mixture.

    precisions_cholesky_ : array-like
        The cholesky decomposition of the precision matrices of each mixture
        component.

    converged_ : bool
        True when convergence was reached in fit(), False otherwise.

    n_iter_ : int
        Number of step used by the best fit of EM to reach the convergence.

    lower_bound_ : float
        Lower bound value on the log-likelihood (of the training data with
        respect to the model) of the best fit of EM.

    decision_scores_ : numpy array of shape (n_samples,)
        The outlier scores of the training data.

    threshold_ : float
        The threshold is based on ``contamination``. It is the
        ``n_samples * contamination`` most abnormal samples in
        ``decision_scores_``. The threshold is calculated for generating
        binary outlier labels.

    labels_ : int, either 0 or 1
        The binary labels of the training data. 0 stands for inliers
        and 1 for outliers/anomalies. It is generated by applying
        ``threshold_`` on ``decision_scores_``.
    """

    def __init__(
            self,
            n_components=1,
            covariance_type="full",
            tol=1e-3,
            reg_covar=1e-6,
            max_iter=100,
            n_init=1,
            init_params="kmeans",
            weights_init=None,
            means_init=None,
            precisions_init=None,
            random_state=None,
            warm_start=False,
            contamination=0.1,
    ):
        super().__init__(contamination=contamination)
        self.n_components = n_components
        self.covariance_type = covariance_type
        self.tol = tol
        self.reg_covar = reg_covar
        self.max_iter = max_iter
        self.n_init = n_init
        self.init_params = init_params
        self.weights_init = weights_init
        self.means_init = means_init
        self.precisions_init = precisions_init
        self.random_state = random_state
        self.warm_start = warm_start

        self.detector_ = None
        self.decision_scores_ = None

    def fit(self, X, y=None):
        """Fit detector. y is ignored in unsupervised methods.

        Parameters
        ----------
        X : numpy array of shape (n_samples, n_features)
            The input samples.

        y : Ignored
            Not used, present for API consistency by convention.

        sample_weight : array-like, shape (n_samples,)
            Per-sample weights. Rescale C per sample. Higher weights
            force the classifier to put more emphasis on these points.

        Returns
        -------
        self : object
            Fitted estimator.
        """
        # validate inputs X and y (optional)
        X = check_array(X)
        self._set_n_classes(y)

        self.detector_ = GaussianMixture(
            n_components=self.n_components,
            covariance_type=self.covariance_type,
            tol=self.tol,
            reg_covar=self.reg_covar,
            max_iter=self.max_iter,
            n_init=self.n_init,
            init_params=self.init_params,
            weights_init=self.weights_init,
            means_init=self.means_init,
            precisions_init=self.precisions_init,
            random_state=self.random_state,
            warm_start=self.warm_start,
        )

        self.detector_.fit(X=X, y=y)

        # invert decision_scores_. Outliers comes with higher outlier scores
        self.decision_scores_ = invert_order(self.detector_.score_samples(X))
        self._process_decision_scores()

        return self

    def decision_function(self, X):
        """Predict raw anomaly score of X using the fitted detector.

        The anomaly score of an input sample is computed based on different
        detector algorithms. For consistency, outliers are assigned with
        larger anomaly scores.

        Parameters
        ----------
        X : numpy array of shape (n_samples, n_features)
            The training input samples. Sparse matrices are accepted only
            if they are supported by the base estimator.

        Returns
        -------
        anomaly_scores : numpy array of shape (n_samples,)
            The anomaly score of the input samples.
        """
        check_is_fitted(self, ["decision_scores_", "threshold_", "labels_"])

        # Invert outlier scores. Outliers come with higher outlier scores
        return invert_order(self.detector_.score_samples(X))

    @property
    def weights_(self):
        """The weights of each mixture components.
        Decorator for scikit-learn Gaussian Mixture Model attributes.
        """
        return self.detector_.weights_

    @property
    def means_(self):
        """The mean of each mixture component.
        Decorator for scikit-learn Gaussian Mixture Model attributes.
        """
        return self.detector_.means_

    @property
    def covariances_(self):
        """The covariance of each mixture component.
        Decorator for scikit-learn Gaussian Mixture Model attributes.
        """
        return self.detector_.covariances_

    @property
    def precisions_(self):
        """The precision matrices for each component in the mixture.
        Decorator for scikit-learn Gaussian Mixture Model attributes.
        """
        return self.detector_.precisions_

    @property
    def precisions_cholesky_(self):
        """The cholesky decomposition of the precision matrices
           of each mixture component.
        Decorator for scikit-learn Gaussian Mixture Model attributes.
        """
        return self.detector_.precisions_cholesky_

    @property
    def converged_(self):
        """True when convergence was reached in fit(), False otherwise.
        Decorator for scikit-learn Gaussian Mixture Model attributes.
        """
        return self.detector_.converged_

    @property
    def n_iter_(self):
        """Number of step used by the best fit of EM to reach the convergence.
        Decorator for scikit-learn Gaussian Mixture Model attributes.
        """
        return self.detector_.n_iter_

    @property
    def lower_bound_(self):
        """Lower bound value on the log-likelihood of the best fit of EM.
        Decorator for scikit-learn Gaussian Mixture Model attributes.
        """
        return self.detector_.lower_bound_
