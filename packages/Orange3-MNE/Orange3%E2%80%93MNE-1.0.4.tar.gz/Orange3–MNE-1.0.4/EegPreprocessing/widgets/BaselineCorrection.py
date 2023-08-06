import mne
from Orange.widgets import widget, gui, settings
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input, Output

from Utils.UiHelper import UiHelper


class BaselineCorrection(widget.OWWidget):
    name = "EEG Baseline Correction"
    description = "Allows of baseline correction for epochs"
    icon = "icons/baseline.png"
    priority = 10
    want_main_area = False

    lower_interval = settings.Setting("0", schema_only=True)
    upper_interval = settings.Setting("0", schema_only=True)

    # Inputs of the widget
    class Inputs:
        raw_data = Input("Epochs", mne.Epochs)

    # Outputs of the widget
    class Outputs:
        raw_data = Output("Epochs", mne.Epochs)

    # Widget initialization
    def __init__(self):
        self.raw_data = None
        self.lower_interval_input = None
        self.upper_interval_input = None

        self.intervals_label = None

        self.create_ui()

    @Inputs.raw_data
    def set_data(self, raw_data):
        self.raw_data = raw_data.copy()

        if self.raw_data is not None:
            self.intervals_label.setText(
                "The lower and upper value must be within {} and {}".format(self.raw_data.times.min() * 1000.0,
                                                                            self.raw_data.times.max() * 1000.0))

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label_lower = UiHelper.create_label("Lower interval (ms)")
        self.lower_interval_input = UiHelper.create_line_edit(self.lower_interval)

        label_upper = UiHelper.create_label("Upper interval (ms)")
        self.upper_interval_input = UiHelper.create_line_edit(self.upper_interval)

        confirm_button = UiHelper.create_button("Confirm settings",
                                                stylesheet=UiHelper.BUTTON_STYLES['btn_success'],
                                                callback=self.confirm_button_click)

        self.intervals_label = UiHelper.create_label("The lower and upper value must be within ? and ?",
                                                     stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(self.intervals_label, 0, 0)

        layout.addWidget(label_lower, 1, 0)
        layout.addWidget(self.lower_interval_input, 1, 1)

        layout.addWidget(label_upper, 2, 0)
        layout.addWidget(self.upper_interval_input, 2, 1)

        layout.addWidget(confirm_button, 3, 1)

    def confirm_button_click(self):
        try:
            self.clear_messages()

            self.lower_interval = self.lower_interval_input.text()
            self.upper_interval = self.upper_interval_input.text()

            lower_temp = float(self.lower_interval) / 1000.0
            upper_temp = float(self.upper_interval) / 1000.0

            if lower_temp < self.raw_data.times.min() or upper_temp > self.raw_data.times.max():
                self.warning(
                    "The lower and upper value must be within {} and {}".format(self.raw_data.times.min() * 1000.0,
                                                                                self.raw_data.times.max() * 1000.0))
                return

            if self.raw_data is not None:
                self.raw_data.apply_baseline(baseline=(lower_temp, upper_temp))
        except ValueError:
            self.error("Values must be numbers only.")

        self.Outputs.raw_data.send(self.raw_data)
