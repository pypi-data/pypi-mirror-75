import pandas as pd
from sklearn.mixture  import BayesianGaussianMixture
from sklearn.mixture  import GaussianMixture
import numpy as np
from typing import  Union
from scipy.spatial import distance

class MDO: # Mahanalobis dectection outliers
    def __init__(self) -> None:
        self.means = []
        self.precision = []
        self.weight = []
        self.data = []
        self.label = []
        self.mahanalobis_local = []
        self.mahanalobis_global = []
        self.nrb_comp = 0

    def Frequentist_gmm_inference(self, data: Union[pd.DataFrame, np.ndarray], **params) -> None:
        """
        Frequentist inference of parameters by the EM algorithms,
        accept only DataFrame with numerical data, please do the feature engineering before enter the Dataframe
        :type data: Pd.DataFrame
        :return None:
        """
        gmm = GaussianMixture(**params)
        gmm.fit(data)

        self.means = gmm.means_
        self.precision = gmm.precisions_
        self.weight = gmm.weights_
        self.label = gmm.predict(data)
        self.data = data
        self.nrb_comp = gmm.n_components


    def Bayesian_gmm_inference(self, data: Union[pd.DataFrame, np.ndarray], **params) -> None:
        """
        Bayesian inference of parameters by the EM algorithms of sklearn,
        accept only DataFrame with numerical data, please do the feature engineering before enter the Dataframe
        :param data: Set of data to do the inference
        :return: None
        """
        Bayesian_gmm = BayesianGaussianMixture(**params)
        Bayesian_gmm.fit(data)

        self.means = Bayesian_gmm.means_
        self.precision = Bayesian_gmm.precisions_
        self.weight = Bayesian_gmm.weights_
        self.label = Bayesian_gmm.predict(data)
        self.data = data
        self.nrb_comp = Bayesian_gmm.n_components

    def global_mahanalobis(self, data: Union[pd.DataFrame, np.ndarray]) -> None:
        """
        evaluate the weighted average distance from clusters
        :param data: data to check
        :return: None
        """
        self.mahanalobis_global = []
        for i in range(data.shape[0]):
          dist_point = 0
          for means, precision, weight in zip(self.means, self.precision, self.weight):
            dist_point += weight*distance.mahalanobis(means, data[i], precision)
          self.mahanalobis_global.append(dist_point)

    def local_mahanalobis(self, data: Union[pd.DataFrame, np.ndarray]) -> None:
        """
        evaluate the distance of the nearest cluster (i.e  the cluster which the point belongs)
        :param data: data to check
        :return: None
        """
        self.mahanalobis_local = []
        for i in range(data.shape[0]):
          means = self.means[self.label[i]]
          precision = self.precision[self.label[i]]
          dist_point = distance.mahalanobis(means,data[i],precision)
          self.mahanalobis_local.append(dist_point)


    def fit(self, data: Union[pd.DataFrame, np.ndarray], inference_type='bayesian', **params) -> None:
        """
        fitting of the distance
        :param data: data to check
        :param inference_type: types of inference (bayesian or frequentist)
        :param params: parameters for the inference
        :return: None
        """
        if inference_type=='bayesian': self.Bayesian_gmm_inference(data, **params)
        if inference_type=='frequentist': self.Frequentist_gmm_inference(data, **params)
        if type(self.data) == pd.DataFrame: data = self.data.values
        else: data = self.data.values

        self.global_mahanalobis(data)
        self.local_mahanalobis(data)

    def get_scoring(self, scoring="global"):
        """
        Get the scoring define by the mahanalobis distance (local or global)
        :param scoring: define if the methods return local scoring or global
        :return: 
        """
        if scoring == 'local': return self.mahanalobis_local
        elif scoring == 'global': return self.mahanalobis_global

