import numpy as np
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget import settings
from orangewidget.utils.signals import Input, Output

from EegClassification.structs.ClassificationStruct import ClassificationStruct
from Utils.UiHelper import UiHelper


class RejectAmplitude(widget.OWWidget):
    name = "Reject Amplitude in Vector"
    description = "Removes all epochs exceeding amplitude threshold in absolute value."
    icon = "icons/rejection.png"
    priority = 5
    want_main_area = False
    V_TO_MV = 1_000_000

    threshold = settings.Setting(100.0, schema_only=True)
    voltage_checked = settings.Setting(False, schema_only=True)

    # Inputs of the widget
    class Inputs:
        struct = Input("Classification Struct", ClassificationStruct)

    # Outputs of the widget
    class Outputs:
        struct = Output("Classification Struct", ClassificationStruct)

    # Widget initialization
    def __init__(self):
        self.struct = None
        self.struct_original = None
        self.amplitude_threshold = None
        self.rejected_label = None
        self.voltage_checkbox = None

        self.create_ui()

    @Inputs.struct
    def set_struct(self, struct: ClassificationStruct):
        if struct is not None:
            self.struct = struct.copy()
            self.struct_original = struct.copy()
        else:
            self.struct = None
            self.struct_original = None

    def update(self):
        if self.struct_original is not None:
            self.reject_amplitude()
            self.Outputs.struct.send(self.struct)

    def reject_amplitude(self):
        """
        Function for amplitude rejection taken over from the original code:
        https://bitbucket.org/lvareka/cnnforgtn/src/eb1327b165c02b8cb1dce6059df163117086a357/main/pre_processing.py#lines-33

        :return: void
        """
        self.threshold = float(self.amplitude_threshold.value())

        output_features = []
        retain_targets = []

        orig_features = self.struct_original.get_features()
        orig_labels = self.struct_original.get_labels()

        self.voltage_checked = self.voltage_checkbox.isChecked()
        temp_threshold = self.threshold
        if not self.voltage_checked:
            temp_threshold /= self.V_TO_MV

        for i in range(orig_features.shape[0]):
            reject = False

            for j in range(orig_features.shape[1]):
                if np.max(np.absolute(orig_features[i][j])) > temp_threshold:
                    reject = True

            if not reject:
                output_features.append(orig_features[i])
            retain_targets.append(not reject)

        output_features = np.array(output_features)
        self.rejected_label.setText("Rejected: {:.2f}%".format((1 - output_features.shape[0] / orig_features.shape[0]) * 100))

        self.struct.set_features(output_features)
        self.struct.set_labels(orig_labels[retain_targets, :])

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label("Amplitude threshold (μV):")
        self.amplitude_threshold = UiHelper.create_spin_box(value=self.threshold, minimum=0, maximum=1000,
                                                            is_double=True)

        layout.addWidget(label, 0, 0)
        layout.addWidget(self.amplitude_threshold, 0, 1)

        self.voltage_checkbox = UiHelper.create_checkbox("Data in μV")
        self.voltage_checkbox.setChecked(self.voltage_checked)
        label_note = UiHelper.create_label(
            "Note: Data from BrainVision files are usually in V.\nThis checkbox switches between V/μV.",
            stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(label_note, 1, 0)
        layout.addWidget(self.voltage_checkbox, 1, 1)

        self.rejected_label = UiHelper.create_label("Rejected: ???", stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(self.rejected_label, 2, 0)

        confirm_button = UiHelper.create_button(text="Confirm settings",
                                                callback=self.update,
                                                stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        layout.addWidget(confirm_button, 3, 1)
