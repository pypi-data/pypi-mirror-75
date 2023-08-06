import numpy as np
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input, Output

from EegClassification.structs.ClassificationStruct import ClassificationStruct
from Utils.UiHelper import UiHelper


class CreateClassificationStruct(widget.OWWidget):
    name = "Create Classification Struct"
    description = "Creates a classification struct from input vector. " \
                  "Classification class corresponds to the selected Stimulus."
    icon = "icons/create-classification-struct.png"
    priority = 2
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        epoch_dict = Input("EEG Epochs Vector", dict)

    # Outputs of the widget
    class Outputs:
        struct = Output("Classification Struct", ClassificationStruct)

    # Widget initialization
    def __init__(self):
        self.confirm_button = None
        self.dict = None

        self.create_ui()

    def update(self):
        if self.dict is not None:
            class_vector = self.create_class_vector()
            struct = ClassificationStruct(self.dict['data'], class_vector, self.dict['sfreq'], self.dict['ch_names'])

            self.Outputs.struct.send(struct)

    def create_class_vector(self):
        """
        Creates a class vector based on selected stimuli, e.g., if stimuli 4 was selected,
        the class vector will be following: [4, 4, 4, ..., 4, 4], where length of the vector is given by the number of
        extracted epochs N, thus final size is [1 x N]

        :return: array
        """
        vector = np.ones((self.dict['data'].shape[0]), dtype=int)
        vector *= next(iter(self.dict['stimuli']))

        return vector

    @Inputs.epoch_dict
    def set_dict(self, epoch_dict):
        if epoch_dict is not None:
            if 'data' not in epoch_dict:
                self.error("This widget accepts the output of the Epochs to Vector widget only.")
                return

            self.dict = epoch_dict.copy()
            self.confirm_button.setDisabled(False)
        else:
            self.dict = None
            self.confirm_button.setDisabled(True)

    #
    # GUI Functions and Callbacks
    #
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label(text="Converts vector to a Classification Struct and creates a class "
                                           "vector for classification. Class vector is based on selected stimuli.",
                                      stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(label)

        self.confirm_button = UiHelper.create_button(text="Confirm settings",
                                                     callback=self.update,
                                                     stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        self.confirm_button.setDisabled(True)
        layout.addWidget(self.confirm_button)
