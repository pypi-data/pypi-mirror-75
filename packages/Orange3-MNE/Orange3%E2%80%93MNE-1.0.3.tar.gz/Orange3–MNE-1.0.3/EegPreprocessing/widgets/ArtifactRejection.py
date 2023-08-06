import mne
from Orange.widgets import widget, gui, settings
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input, Output

from Utils.UiHelper import UiHelper


class ArtifactRejection(widget.OWWidget):
    name = "EEG Artifact Rejection"
    description = "Reject epochs based on given amplitude threshold. " \
                  "Epoch is rejected if absolute value of peak is greater then threshold."
    icon = "icons/rejection.png"
    priority = 10
    want_main_area = False

    V_TO_MV = 1_000_000.0  # convert to μVolts
    threshold = settings.Setting(35.0, schema_only=True)

    # Inputs of the widget
    class Inputs:
        epochs = Input("Epochs", (mne.io.BaseRaw, mne.Epochs, mne.Evoked))

    # Outputs of the widget
    class Outputs:
        epochs = Output("Epochs", mne.Epochs)

    # Widget initialization
    def __init__(self):
        self.epochs = None
        self.threshold_input = None
        self.label_info = None

        self.create_ui()

    @Inputs.epochs
    def set_epochs(self, epochs):
        if isinstance(type(epochs), mne.io.BaseRaw) or isinstance(type(epochs), mne.Evoked):
            self.warning("Rejection works only with Epochs.")
            return

        self.label_info.setText("Rejected ???%")

        if epochs is not None:
            self.epochs = epochs.copy()
        else:
            self.epochs = None

    def update(self):
        self.threshold = threshold_temp = float(self.threshold_input.value())

        if self.epochs is not None:
            bad_indices = []
            threshold_temp /= self.V_TO_MV

            for index, evoked in enumerate(self.epochs.iter_evoked()):
                ch_name, latency, peak = evoked.get_peak(return_amplitude=True)

                if abs(peak) > threshold_temp:
                    bad_indices.append(index)

            epochs_result = self.epochs.copy()
            epochs_result.drop(bad_indices)

            drop_percentage = (len(bad_indices) / self.epochs.events.shape[0]) * 100
            self.label_info.setText("Rejected: {:.2f}%".format(drop_percentage))

            self.Outputs.epochs.send(epochs_result)

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label("Threshold (μV):")
        self.threshold_input = UiHelper.create_spin_box(value=self.threshold, is_double=True, minimum=1, maximum=1000)

        layout.addWidget(label, 1, 0)
        layout.addWidget(self.threshold_input, 1, 1)

        self.label_info = UiHelper.create_label("Rejected ???%", stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(self.label_info, 2, 0)

        confirm_button = UiHelper.create_button(text="Confirm settings",
                                                stylesheet=UiHelper.BUTTON_STYLES['btn_success'],
                                                callback=self.update)
        layout.addWidget(confirm_button, 3, 1)
