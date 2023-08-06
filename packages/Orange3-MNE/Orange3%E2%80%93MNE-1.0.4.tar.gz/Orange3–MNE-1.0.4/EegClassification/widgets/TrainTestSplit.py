from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget import settings
from orangewidget.utils.signals import Input, Output
from sklearn.model_selection import train_test_split

from EegClassification.structs.ClassificationStruct import ClassificationStruct
from EegClassification.structs.TestTrainStruct import TestTrainStruct
from Utils.UiHelper import UiHelper


class TrainTestSplit(widget.OWWidget):
    name = "Train/Test Split"
    description = "Takes in a Classification struct and then splits the data into a training and testing parts " \
                  "and creates a Test Train struct."
    icon = "icons/test-train.png"
    priority = 8
    want_main_area = False

    validation = settings.Setting(25, schema_only=True)

    # Inputs of the widget
    class Inputs:
        classification_struct = Input("Classification Struct", ClassificationStruct)

    # Outputs of the widget
    class Outputs:
        train_struct = Output("Train Test Struct", TestTrainStruct)

    # Widget initialization
    def __init__(self):
        self.class_struct = None
        self.class_struct_orig = None

        self.validation_input = None
        self.confirm_button = None

        self.create_ui()

    def update(self):
        try:
            self.validation = int(self.validation_input.text())
        except ValueError as err:
            self.error(f"Value must be numbers only. Using initial value. {str(err)}")

        try:
            temp_validation = self.validation / 100.0
            x_train, x_test, y_train, y_test = train_test_split(self.class_struct.get_features(),
                                                                self.class_struct.get_labels(),
                                                                test_size=temp_validation,
                                                                random_state=0, shuffle=True)

            val = round(temp_validation * x_train.shape[0])
            struct = TestTrainStruct(x_train, y_train, x_test, y_test, val)
            self.Outputs.train_struct.send(struct)
        except Exception as err:
            self.error(f"An error has occurred: {str(err)}")
            self.Outputs.train_struct.send(None)

    @Inputs.classification_struct
    def set_class_struct(self, struct):
        if struct is not None:
            self.class_struct = struct.copy()
            self.class_struct_orig = struct.copy()
            self.confirm_button.setDisabled(False)
        else:
            self.class_struct = None
            self.class_struct_orig = None
            self.confirm_button.setDisabled(True)

    #
    # GUI Functions and Callbacks
    #
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label("Validation %:")
        self.validation_input = UiHelper.create_spin_box(0, 100, False, value=self.validation)

        layout.addWidget(label, 0, 0)
        layout.addWidget(self.validation_input, 0, 1)

        self.confirm_button = UiHelper.create_button(text="Confirm Settings",
                                                     callback=self.update,
                                                     stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        self.confirm_button.setDisabled(True)
        layout.addWidget(self.confirm_button, 1, 1)
