import numpy as np
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input, Output

from EegClassification.structs.ClassificationStruct import ClassificationStruct
from Utils.UiHelper import UiHelper


class PrepareVectors(widget.OWWidget):
    name = "Prepare Vectors"
    description = "Loads target and non-target vectors into a structure, which can be used in classification."
    icon = "icons/prepare-vectors.png"
    priority = 1
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        target_vector = Input("Target Vector", dict)
        non_target_vector = Input("Non-target Vector", dict)

    # Outputs of the widget
    class Outputs:
        classification_struct = Output("Classification Struct", ClassificationStruct)

    # Widget initialization
    def __init__(self):
        self.target_vector = None
        self.non_target_vector = None

        self.create_ui()

    @Inputs.target_vector
    def set_target_vector(self, vector):
        self.target_vector = vector
        self.update()

    @Inputs.non_target_vector
    def set_non_target_vector(self, vector):
        self.non_target_vector = vector
        self.update()

    def update(self):
        if self.non_target_vector is not None and self.target_vector is not None:
            target_vector = self.target_vector.get('data')
            non_target_vector = self.non_target_vector.get('data')

            target_sfreq = self.target_vector.get('sfreq')
            non_target_sfreq = self.non_target_vector.get('sfreq')

            ch_names = self.target_vector.get('ch_names') + self.non_target_vector.get('ch_names')

            # This part was taken from the original source code:
            # https://bitbucket.org/lvareka/cnnforgtn/src/eb1327b165c02b8cb1dce6059df163117086a357/main/run_analysis.py#lines-32
            #
            out_features = np.concatenate((target_vector, non_target_vector), axis=0)
            out_t_labels = np.tile(np.array([1, 0]), (target_vector.shape[0], 1))
            out_n_labels = np.tile(np.array([0, 1]), (non_target_vector.shape[0], 1))
            out_labels = np.vstack((out_t_labels, out_n_labels))

            self.Outputs.classification_struct.send(
                ClassificationStruct(features=out_features.copy(),
                                     labels=out_labels.copy(),
                                     sfreq=min(target_sfreq, non_target_sfreq),
                                     ch_names=ch_names))
        else:
            self.Outputs.classification_struct.send(None)

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label(
            text="Concatenates target and non-target vectors together, and creates vector with classification classes.",
            stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(label)

        button = UiHelper.create_button(text="Confirm settings",
                                        callback=self.update,
                                        stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        layout.addWidget(button)
