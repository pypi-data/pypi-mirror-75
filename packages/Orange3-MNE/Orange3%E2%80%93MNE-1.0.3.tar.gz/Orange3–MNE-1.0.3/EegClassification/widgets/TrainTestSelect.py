from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input, Output

from EegClassification.structs.ClassificationStruct import ClassificationStruct
from EegClassification.structs.TestTrainStruct import TestTrainStruct
from Utils.UiHelper import UiHelper


class TrainTestSelect(widget.OWWidget):
    name = "Train/Test Select"
    description = "Takes in Classification struct and creates a Test Train struct from them."
    icon = "icons/test-train-select.png"
    priority = 7
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        train_struct = Input("Train Classification Struct", ClassificationStruct)
        test_struct = Input("Test Classification Struct", ClassificationStruct)

    # Outputs of the widget
    class Outputs:
        test_train_struct = Output("Train Test Struct", TestTrainStruct)

    # Widget initialization
    def __init__(self):
        self.train_struct = None
        self.test_struct = None

        self.confirm_button = None

        self.create_ui()

    def update(self):
        self.clear_messages()

        if self.train_struct is None or self.test_struct is None:
            self.warning("Both training and testing structs have to be set.")
            return

        x_train = self.train_struct.get_features()
        y_train = self.train_struct.get_labels()
        x_test = self.test_struct.get_features()
        y_test = self.test_struct.get_labels()

        validation = x_test.shape[0]
        struct = TestTrainStruct(x_train, y_train, x_test, y_test, validation)

        self.Outputs.test_train_struct.send(struct)

    @Inputs.train_struct
    def set_train_struct(self, struct):
        if struct is not None:
            self.train_struct = struct.copy()
        else:
            self.train_struct = None

    @Inputs.test_struct
    def set_test_struct(self, struct):
        if struct is not None:
            self.test_struct = struct.copy()
        else:
            self.test_struct = None

    #
    # GUI Functions and Callbacks
    #
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label(text="Converts Train and Test Classification Structs into "
                                           "a struct that can be used in classification widgets.",
                                      stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(label)

        self.confirm_button = UiHelper.create_button(text="Confirm settings",
                                                     callback=self.update,
                                                     stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        layout.addWidget(self.confirm_button)
