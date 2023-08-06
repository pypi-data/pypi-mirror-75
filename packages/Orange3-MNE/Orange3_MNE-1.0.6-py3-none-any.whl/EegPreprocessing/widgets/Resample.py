import mne
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget import settings
from orangewidget.utils.signals import Input, Output

from Utils.UiHelper import UiHelper


class Resample(widget.OWWidget):
    name = "EEG Resample"
    description = "Resamples the epochs to given sample rate"
    icon = "icons/resample.png"
    priority = 10
    want_main_area = False

    sample_rate = settings.Setting(100, schema_only=True)

    # Inputs of the widget
    class Inputs:
        epochs = Input("Epochs", mne.Epochs)

    # Outputs of the widget
    class Outputs:
        epochs = Output("Epochs", mne.Epochs)

    # Widget initialization
    def __init__(self):
        self.sample_rate_input = None
        self.epochs = None

        self.create_ui()

    def update(self):
        if self.epochs is not None:
            epochs = self.epochs.copy()
            self.sample_rate = float(self.sample_rate_input.text())
            epochs.resample(self.sample_rate)

            self.Outputs.epochs.send(epochs)

    @Inputs.epochs
    def set_epochs(self, epochs):
        if epochs is not None:
            self.epochs = epochs.copy()
        else:
            self.epochs = None

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label("Sampling rate (Hz):")
        self.sample_rate_input = UiHelper.create_spin_box(value=self.sample_rate, minimum=1, maximum=1000)

        layout.addWidget(label, 0, 0)
        layout.addWidget(self.sample_rate_input, 0, 1)

        confirm_button = UiHelper.create_button(text="Confirm settings",
                                                callback=self.update,
                                                stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        layout.addWidget(confirm_button, 1, 1)
