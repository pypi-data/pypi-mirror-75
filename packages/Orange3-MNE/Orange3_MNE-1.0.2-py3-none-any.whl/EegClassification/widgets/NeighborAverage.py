import numpy as np
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget import settings
from orangewidget.utils.signals import Input, Output

from EegClassification.structs.TestTrainStruct import TestTrainStruct
from Utils.UiHelper import UiHelper


class NeighborAverage(widget.OWWidget):
    name = "Neighbor Average"
    description = "Averages every N trials"
    icon = "icons/averaging.png"
    priority = 9
    want_main_area = False

    train_average = settings.Setting(False, schema_only=True)
    test_average = settings.Setting(False, schema_only=True)
    train_averaging_factor = settings.Setting(1, schema_only=True)
    test_averaging_factor = settings.Setting(1, schema_only=True)

    # Inputs of the widget
    class Inputs:
        test_train_struct = Input("Train Test Struct", TestTrainStruct)

    # Outputs of the widget
    class Outputs:
        test_train_struct = Output("Train Test Struct", TestTrainStruct)

    # Widget initialization
    def __init__(self):
        self.struct = None
        self.struct_orig = None

        self.confirm_button = None
        self.train_average_checkbox = None
        self.test_average_checkbox = None
        self.train_averaging_factor_input = None
        self.test_averaging_factor_input = None

        self.create_ui()

    def update(self):
        self.clear_messages()
        if self.struct is None:
            self.warning("No input data provided.")
            return

        self.struct = self.struct_orig.copy()

        self.train_average = self.train_average_checkbox.isChecked()
        self.test_average = self.test_average_checkbox.isChecked()
        self.train_averaging_factor = int(self.train_averaging_factor_input.value())
        self.test_averaging_factor = int(self.test_averaging_factor_input.value())

        if self.train_average:
            [x_train, y_train] = self.average_data(self.struct_orig.get_x_train().copy(),
                                                   self.struct_orig.get_y_train().copy(),
                                                   self.train_averaging_factor)
            self.struct.set_x_train(x_train)
            self.struct.set_y_train(y_train)

        if self.test_average:
            [x_test, y_test] = self.average_data(self.struct_orig.get_x_test().copy(),
                                                 self.struct_orig.get_y_test().copy(),
                                                 self.test_averaging_factor)
            self.struct.set_x_test(x_test)
            self.struct.set_y_test(y_test)

        self.Outputs.test_train_struct.send(self.struct)

    def average_data(self, out_features, out_labels, averaging_factor):
        """
        Averages every N trials in EEG data

        :param out_features: EEG feature vector
        :param out_labels: labels
        :param averaging_factor: number of trials to average together
        """
        if averaging_factor <= 1:
            return [out_features, out_labels]

        # separate only targets/non-target features
        out_t_features = out_features[out_labels[:, 0] == 1, :]
        out_n_features = out_features[out_labels[:, 1] == 1, :]

        # ensemble average targets and non-targets features
        out__t_features_avg = self.average(out_t_features, averaging_factor)
        out__n_features_avg = self.average(out_n_features, averaging_factor)

        # create corresponding labels
        out_t_labels = np.tile(np.array([1, 0]), (out__t_features_avg.shape[0], 1))
        out_n_labels = np.tile(np.array([0, 1]), (out__n_features_avg.shape[0], 1))

        # connect target/non-target features/labels
        out_labels = np.vstack((out_t_labels, out_n_labels))
        out_features = np.concatenate((out__t_features_avg, out__n_features_avg), axis=0)

        return [out_features, out_labels]

    def average(self, out_features, averaging_factor):
        """
        Averages features only by a certain factor
        Taken from original source code: https://bitbucket.org/lvareka/cnnforgtn/src/eb1327b165c02b8cb1dce6059df163117086a357/main/pre_processing.py#lines-80
        """
        out_eeg_data = []
        for trial in range(0, out_features.shape[0] - 1, averaging_factor):
            avg_fv = np.average(out_features[trial:(trial + averaging_factor), :], axis=0)
            out_eeg_data.append(avg_fv)
        return np.array(out_eeg_data)

    @Inputs.test_train_struct
    def set_struct(self, struct):
        if struct is not None:
            self.struct = struct.copy()
            self.struct_orig = struct.copy()
            self.confirm_button.setDisabled(False)
        else:
            self.struct = None
            self.struct_orig = None
            self.confirm_button.setDisabled(True)

    #
    # GUI Functions and Callbacks
    #
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label("Select the data which will be averaged:")
        layout.addWidget(label)

        self.train_average_checkbox = UiHelper.create_checkbox("Train data")
        self.train_average_checkbox.setChecked(self.train_average)
        self.test_average_checkbox = UiHelper.create_checkbox("Test data")
        self.test_average_checkbox.setChecked(self.test_average)
        layout.addWidget(self.train_average_checkbox, 1, 1)
        layout.addWidget(self.test_average_checkbox, 2, 1)

        label_train = UiHelper.create_label("Train averaging factor:")
        self.train_averaging_factor_input = UiHelper.create_spin_box(0, 10, value=self.train_averaging_factor)
        layout.addWidget(label_train, 3, 0)
        layout.addWidget(self.train_averaging_factor_input, 3, 1)

        label_test = UiHelper.create_label("Test averaging factor:")
        self.test_averaging_factor_input = UiHelper.create_spin_box(0, 10, value=self.test_averaging_factor)
        layout.addWidget(label_test, 4, 0)
        layout.addWidget(self.test_averaging_factor_input, 4, 1)

        self.confirm_button = UiHelper.create_button(text="Confirm settings",
                                                     callback=self.update,
                                                     stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        self.confirm_button.setDisabled(True)
        layout.addWidget(self.confirm_button, 5, 1)
