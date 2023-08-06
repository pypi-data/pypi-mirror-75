from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input, Output

from EegClassification.structs.ClassificationStruct import ClassificationStruct
from Utils.UiHelper import UiHelper


class CNNReshape(widget.OWWidget):
    name = "CNN Reshape"
    description = "Add a singleton dimension to enable CNN Keras classification"
    icon = "icons/cnn-reshape.png"
    priority = 6
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        classification_struct = Input("Classification Struct", ClassificationStruct)

    # Outputs of the widget
    class Outputs:
        classification_struct = Output("Classification Struct", ClassificationStruct)

    # Widget initialization
    def __init__(self):
        self.struct = None

        self.confirm_button = None

        self.create_ui()

    def update(self):
        self.clear_messages()
        if self.struct is None:
            self.warning("No data were provided.")
            return

        struct = self.struct.copy()
        features = self.cnn_reshape(struct.get_features().copy())
        struct.set_features(features)
        self.Outputs.classification_struct.send(struct)

    def cnn_reshape(self, out_features):
        """
        Taken from original source code: https://bitbucket.org/lvareka/cnnforgtn/src/eb1327b165c02b8cb1dce6059df163117086a357/main/pre_processing.py#lines-25
        """
        out_features = out_features.reshape(out_features.shape[0], out_features.shape[1], out_features.shape[2], 1)
        return out_features

    @Inputs.classification_struct
    def set_struct(self, struct):
        if struct is not None:
            self.struct = struct.copy()
            self.confirm_button.setDisabled(False)
        else:
            self.struct = None
            self.confirm_button.setDisabled(True)

    #
    # GUI Functions and Callbacks
    #
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label(text="Adds a singleton dimension to a vector.",
                                      stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(label)

        self.confirm_button = UiHelper.create_button(text="Confirm settings",
                                                     callback=self.update,
                                                     stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        self.confirm_button.setDisabled(True)
        layout.addWidget(self.confirm_button)
