import copy

from numpy.core.records import ndarray


class TestTrainStruct:
    def __init__(self, x_train: ndarray, y_train: ndarray, x_test: ndarray, y_test: ndarray, validation: float):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.validation = validation
        self.original_x_train_shape = x_train.shape[0]

    def get_x_train(self):
        return self.x_train

    def get_y_train(self):
        return self.y_train

    def get_x_test(self):
        return self.x_test

    def get_y_test(self):
        return self.y_test

    def set_x_train(self, data):
        self.x_train = data

    def set_y_train(self, data):
        self.y_train = data

    def set_x_test(self, data):
        self.x_test = data

    def set_y_test(self, data):
        self.y_test = data

    def get_validation(self):
        return self.validation

    def get_original_x_train_shape(self):
        return self.original_x_train_shape

    def copy(self):
        return copy.deepcopy(self)
