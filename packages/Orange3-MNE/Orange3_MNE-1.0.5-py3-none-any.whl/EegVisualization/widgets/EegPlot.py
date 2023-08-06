import mne
from Orange.widgets import widget, gui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input

from Utils.UiHelper import UiHelper


class EegPlot(widget.OWWidget):
    name = "EEG Plot"
    description = "Visualization of the raw EEG data using MNE"
    icon = "icons/simple-plot.png"
    priority = 10
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        raw_data = Input("EEG data", (mne.io.Raw, mne.Epochs, mne.Evoked))

    # Outputs of the widget
    class Outputs:
        pass

    # Widget initialization
    def __init__(self):
        self.no_highcut_found = None
        self.highcut_input = None

        self.no_data_label = None
        self.raw_data = None
        self.show_button = None

        self.use_highcut = False

        self.create_ui()

    @Inputs.raw_data
    def set_raw_data(self, raw_data):
        self.show_warning(False)
        self.clear_messages()
        self.use_highcut = False
        self.raw_data = raw_data.copy()

        # Hack, if vhdr doesn't contain information about lowpass, we need to avoid Division by zero
        if self.raw_data.info.get("lowpass") == 0:
            self.warning("No High Cutoff was found in .vhdr file.")
            self.raw_data.info["lowpass"] = 250
            self.show_warning()
            self.use_highcut = True

        self.update()

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        wbox = gui.widgetBox(self.controlArea, margin=0, orientation=layout)
        wbox.setMinimumSize(QSize(400, 75))

        self.show_button = UiHelper.create_button("Show simple plot", callback=self.show_data)
        self.show_button.setDisabled(True)

        self.no_data_label = UiHelper.create_label("No data were loaded.")

        self.no_highcut_found = UiHelper.create_label(
            "No High Cutoff was found in .vhdr file. You have to enter it manually. Meanwhile, default value 250 is used.")
        self.no_highcut_found.setWordWrap(True)
        self.no_highcut_found.hide()

        self.highcut_input = UiHelper.create_line_edit("250")
        self.highcut_input.hide()

        layout.addWidget(self.no_data_label, 0, 0)
        layout.addWidget(self.no_highcut_found, 1, 0)
        layout.addWidget(self.highcut_input, 2, 0)
        layout.addWidget(self.show_button, 3, 0)

    def show_warning(self, show: bool = True):
        if show:
            self.no_highcut_found.show()
            self.highcut_input.show()
        else:
            self.no_highcut_found.hide()
            self.highcut_input.hide()

    def update(self):
        if self.raw_data is None:
            self.show_button.setDisabled(True)
            self.no_data_label.show()
        else:
            self.show_button.setDisabled(False)
            self.no_data_label.hide()

    def show_data(self):
        # Hack pt.2 Electric Boogaloo
        if self.use_highcut:
            self.raw_data.info["lowpass"] = float(self.highcut_input.text())

        self.raw_data.plot()
