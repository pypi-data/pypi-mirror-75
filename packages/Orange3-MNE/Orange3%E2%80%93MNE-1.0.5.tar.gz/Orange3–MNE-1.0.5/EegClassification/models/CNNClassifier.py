import keras_metrics
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.callbacks import EarlyStopping
from keras.layers import Conv2D, AveragePooling2D, Dense, Flatten, Dropout
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential


# Applies convolutional neural network
# to both training and testing data
class CNNClassifier:

    # Configuration of the model
    def __init__(self, channels, time_samples, loss, n_epochs):
        self.model = Sequential((
            # The first conv layer learns `nb_filter` filters (aka kernels),
            # each of size ``(filter_length, nb_input_series)``.
            # Its output will have shape (None, window_size - filter_length + 1, nb_filter), i.e., for each position in
            # the input timeseries, the activation of each filter at that position.
            Conv2D(6, (3, 3), activation='elu', input_shape=(channels, time_samples, 1)),
            BatchNormalization(),
            Dropout(0.5),  # added 28. 05. 2019

            AveragePooling2D(pool_size=(1, 8)),  # Downsample the output of convolution by 2X.
            Flatten(),

            Dense(100, activation='elu'),
            BatchNormalization(),
            Dropout(0.5),

            Dense(2, activation='softmax'),
        ))
        # To perform (binary) classification instead:
        self.model.compile(loss=loss, optimizer='adam',
                           metrics=[tf.metrics.BinaryAccuracy(), tf.metrics.AUC(name='auc'), keras_metrics.precision(),
                                    keras_metrics.recall()])
        #        if self.param.verbose:
        #           print(self.model.summary())
        self.n_epochs = n_epochs
        self.verbose = True

    def get_model(self):
        return self.model

    # Fits the model using training data and applies early stopping based
    # on the validation subset:
    # x[number of examples x number of channels x samples in each epoch x 1]
    # y[number of examples x number of categories - default 2]
    # self.param.validation determines the validation set size
    def fit(self, x_train, y_train, x_val, y_val):
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1, mode='auto')
        hist = self.model.fit(x_train, y_train, epochs=self.n_epochs, batch_size=16, shuffle=True,
                              callbacks=[early_stopping], verbose=self.verbose,
                              validation_data=(x_val, y_val))

        val_metrics = [hist.history['val_binary_accuracy'][-1], hist.history['val_auc'][-1],
                       hist.history['val_precision'][-1], hist.history['val_recall'][-1]]
        return val_metrics

    def evaluate(self, x, y):
        metrics = self.model.evaluate(x, y)
        if len(metrics) == 5:
            metrics = [metrics[1], metrics[2], metrics[3], metrics[4]]

        return metrics
