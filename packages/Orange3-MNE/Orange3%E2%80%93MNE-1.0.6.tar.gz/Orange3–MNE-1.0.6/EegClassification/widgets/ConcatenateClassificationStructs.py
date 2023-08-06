import sys

import numpy as np
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input, Output

from EegClassification.structs.ClassificationStruct import ClassificationStruct
from Utils.UiHelper import UiHelper


class ConcatenateClassificationStructs(widget.OWWidget):
    name = "Concatenate Classification Structs"
    description = "Concatenates multiple Classification structs together."
    icon = "icons/con-classification-structs.png"
    priority = 3
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        class_struct = Input("EEG Classification Struct", ClassificationStruct, multiple=True)

    # Outputs of the widget
    class Outputs:
        class_struct = Output("EEG Classification Struct", ClassificationStruct)

    # Widget initialization
    def __init__(self):
        self.struct_list = {}
        self.confirm_button = None

        self.create_ui()

    def update(self):
        min_size = sys.maxsize
        sfreq = self.struct_list[next(iter(self.struct_list))].get_sfreq()
        ch_names = self.struct_list[next(iter(self.struct_list))].get_ch_names()

        # Find min length of the extracted epochs across all structs
        for key, value in self.struct_list.items():
            min_size = min(min_size, value.get_features().shape[0])

        min_size += 1
        features = None
        labels = None

        # Crop values to prevent overfitting
        # TODO: add checkbox
        for key, value in self.struct_list.items():
            tmp_features = value.get_features()
            if tmp_features.shape[0] > min_size - 1:
                tmp_features = tmp_features[1:min_size, :]

            if features is None:
                features = tmp_features
            else:
                features = np.concatenate((features, tmp_features))

            tmp_labels = value.get_labels().copy()
            if tmp_labels.shape[0] > min_size - 1:
                tmp_labels = tmp_labels[1:min_size]

            if labels is None:
                labels = tmp_labels
            else:
                labels = np.append(labels, tmp_labels)

        if len(labels.shape) > 1:
            labels = labels.flatten()

        self.Outputs.class_struct.send(ClassificationStruct(features, labels, sfreq, ch_names))

    @Inputs.class_struct
    def set_struct(self, struct, id):
        if struct is not None:
            self.struct_list[str(id[0])] = struct.copy()
        else:
            del self.struct_list[str(id[0])]

        if len(self.struct_list) == 0:
            self.confirm_button.setDisabled(True)
        else:
            self.confirm_button.setDisabled(False)

    #
    # GUI Functions and Callbacks
    #
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label(text="Concatenates multiple Classification Structs together "
                                           "and crops their size to match the smallest struct to prevent overfitting.",
                                      stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(label)

        self.confirm_button = UiHelper.create_button(text="Confirm settings",
                                                     callback=self.update,
                                                     stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        self.confirm_button.setDisabled(True)
        layout.addWidget(self.confirm_button)
