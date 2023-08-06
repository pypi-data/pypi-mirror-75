import mne
from Orange.widgets import widget, gui, settings
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input

from Utils.UiHelper import UiHelper


class PeakLatency(widget.OWWidget):
    name = "EEG Peak Latency"
    description = ""
    icon = "icons/peak-latency.png"
    priority = 10
    want_main_area = False

    # Modes of peak finding
    modes = {"Positive": "pos", "Negative": "neg", "Absolute": "abs"}

    # Settings
    t_min = settings.Setting("", schema_only=True)
    t_max = settings.Setting("", schema_only=True)
    mode = settings.Setting("Positive", schema_only=True)

    # Inputs of the widget
    class Inputs:
        evoked = Input("Evoked", mne.Evoked)

    # Outputs of the widget
    class Outputs:
        pass

    # Widget initialization
    def __init__(self):
        self.evoked = None

        self.peak_label = None
        self.label_info = None

        self.t_min_input = None
        self.t_max_input = None

        self.mode_combo = None

        self.create_ui()

    @Inputs.evoked
    def set_evoked(self, evoked):
        self.evoked = evoked.copy()

        if self.evoked is not None:
            self.label_info.setText(
                "The tMin and tMax must be within {} and {}".format(self.evoked.times.min() * 1000.0,
                                                                    self.evoked.times.max() * 1000.0))

    def update(self):
        self.clear_messages()

        if self.evoked is not None:
            t_min = None
            t_max = None

            self.mode = self.mode_combo.currentText()
            mode = self.modes[self.mode_combo.currentText()]

            self.t_min = self.t_min_input.text()
            self.t_max = self.t_max_input.text()

            try:
                if self.t_min != "":
                    t_min = float(self.t_min) / 1000.0
                if self.t_max != "":
                    t_max = float(self.t_max) / 1000.0

                if (t_min is not None and t_min < self.evoked.times.min()) or \
                        (t_max is not None and t_max > self.evoked.times.max()):
                    self.warning("The tMin and tMax must be within {} and {}".format(self.evoked.times.min() * 1000.0,
                                                                                     self.evoked.times.max() * 1000.0))
                    return
            except ValueError as error:
                self.error("Values must be numbers only.")

            ch_name, latency, amplitude = self.evoked.get_peak(return_amplitude=True, tmin=t_min, tmax=t_max, mode=mode)
            self.peak_label.setText(f"{amplitude}V, {latency}ms")

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        peak_label_description = UiHelper.create_label("Peak amplitude and latency:")
        self.peak_label = UiHelper.create_label("?")

        layout.addWidget(peak_label_description, 1, 0)
        layout.addWidget(self.peak_label, 1, 1)

        self.label_info = UiHelper.create_label("The tMin and tMax must be within ? and ?",
                                                stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(self.label_info, 2, 0)

        t_min_label = UiHelper.create_label("tMin (ms)")
        self.t_min_input = UiHelper.create_line_edit(text=self.t_min)

        t_max_label = UiHelper.create_label("tMax (ms)")
        self.t_max_input = UiHelper.create_line_edit(text=self.t_max)

        layout.addWidget(t_min_label, 3, 0)
        layout.addWidget(self.t_min_input, 3, 1)

        layout.addWidget(t_max_label, 4, 0)
        layout.addWidget(self.t_max_input, 4, 1)

        mode_label = UiHelper.create_label("Mode:")
        self.mode_combo = UiHelper.create_combo_box(self.modes)
        self.mode_combo.setCurrentIndex(self.mode_combo.findText(self.mode))

        layout.addWidget(mode_label, 5, 0)
        layout.addWidget(self.mode_combo, 5, 1)

        confirm_button = UiHelper.create_button(text="Confirm settings",
                                                stylesheet=UiHelper.BUTTON_STYLES['btn_success'],
                                                callback=self.update)

        layout.addWidget(confirm_button, 6, 1)
