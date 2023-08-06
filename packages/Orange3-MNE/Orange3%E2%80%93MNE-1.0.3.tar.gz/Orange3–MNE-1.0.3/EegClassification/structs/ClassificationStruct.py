import copy

from numpy.core.records import ndarray


class ClassificationStruct:
    """
    This structure holds vectors and parameters that are used for Classification.
    """

    def __init__(self, features: ndarray, labels: ndarray, sfreq: float, ch_names: list):
        self.ch_names = ch_names
        self.sfreq = sfreq
        self.features = features
        self.labels = labels

    def set_features(self, features):
        self.features = features

    def set_labels(self, labels):
        self.labels = labels

    def get_features(self):
        return self.features

    def get_labels(self):
        return self.labels

    def get_sfreq(self):
        return self.sfreq

    def get_ch_names(self):
        return self.ch_names

    def copy(self):
        return copy.deepcopy(self)
