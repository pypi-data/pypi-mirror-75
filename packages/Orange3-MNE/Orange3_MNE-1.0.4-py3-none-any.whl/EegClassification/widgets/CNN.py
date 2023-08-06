import numpy as np
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget import settings
from orangewidget.utils.signals import Input
from sklearn.model_selection import ShuffleSplit

from EegClassification.models.CNNClassifier import CNNClassifier
from EegClassification.structs.TestTrainStruct import TestTrainStruct
from EegClassification.widgets.AbstractClassifierRunner import AbstractClassifierRunner
from Utils.UiHelper import UiHelper


class CNN(widget.OWWidget, AbstractClassifierRunner):
    name = "Convolutional Neural Network"
    description = ""
    icon = "icons/cnn.png"
    priority = 11
    want_main_area = False

    epochs = settings.Setting(30, schema_only=True)
    iterations = settings.Setting(30, schema_only=True)

    # Inputs of the widget
    class Inputs:
        test_train_struct = Input("Train Test Struct", TestTrainStruct)

    # Outputs of the widget
    class Outputs:
        pass

    # Widget initialization

    def __init__(self):
        self.test_train_struct = None

        self.epochs_input = None
        self.iterations_input = None
        self.confirm_button = None
        self.validation_label = None
        self.test_label = None

        self.create_ui()

    def update(self):
        # TODO: nefunguje u workflow přímo z orange
        self.validation_label.setText("Validation: ???")
        self.test_label.setText("Test: ???")

        self.clear_messages()
        if self.test_train_struct is None:
            self.warning("No input data were supplied.")
            return

        val = self.test_train_struct.get_validation()

        self.epochs = int(self.epochs_input.text())
        self.iterations = int(self.iterations_input.text())
        shuffle_split = ShuffleSplit(n_splits=self.iterations, test_size=val, random_state=0)
        model = CNNClassifier(self.test_train_struct.get_x_train().shape[1],
                              self.test_train_struct.get_x_train().shape[2],
                              'categorical_crossentropy', self.epochs)

        try:
            [val_results, test_results] = self.run_model(model, self.test_train_struct, shuffle_split)

            validation_label_text = f"Validation:\n\tavg:\t{np.round(np.mean(val_results, axis=0) * 100, 2)}\n\tstd:\t{np.round(np.std(val_results, axis=0) * 100, 2)}"
            test_label_text = f"Test:\n\tavg:\t{np.round(np.mean(test_results, axis=0) * 100, 2)}\n\tstd:\t{np.round(np.std(test_results, axis=0) * 100, 2)}"
            self.validation_label.setText(validation_label_text)
            self.test_label.setText(test_label_text)
        except ValueError as err:
            self.error(str(err))

    @Inputs.test_train_struct
    def set_struct(self, struct):
        if struct is not None:
            self.test_train_struct = struct.copy()
            self.confirm_button.setDisabled(False)
        else:
            self.test_train_struct = None
            self.confirm_button.setDisabled(True)

    #
    # GUI
    #
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label_epochs = UiHelper.create_label("Number of epochs:")
        self.epochs_input = UiHelper.create_spin_box(minimum=1, maximum=1000, value=self.epochs)
        layout.addWidget(label_epochs, 0, 0)
        layout.addWidget(self.epochs_input, 0, 1)

        label_iterations = UiHelper.create_label("Number of iterations:")
        self.iterations_input = UiHelper.create_spin_box(minimum=1, maximum=1000, value=self.iterations)
        layout.addWidget(label_iterations, 1, 0)
        layout.addWidget(self.iterations_input, 1, 1)

        label_info = UiHelper.create_label(
            text="Results are in a following format: [Accuracy, AUC, Precision, Recall] \n"
                 "Note: If only one result is displayed it corresponds to Accuracy.",
            stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(label_info, 2, 0)

        self.validation_label = UiHelper.create_label("Validation: ???")
        self.test_label = UiHelper.create_label("Test: ???")
        layout.addWidget(self.validation_label, 3, 0)
        layout.addWidget(self.test_label, 4, 0)

        self.confirm_button = UiHelper.create_button(text="Start computation",
                                                     callback=self.update,
                                                     stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        self.confirm_button.setDisabled(True)
        layout.addWidget(self.confirm_button, 5, 1)
