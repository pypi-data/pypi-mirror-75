import mne
from Orange.widgets import widget, gui, settings
from PyQt5.QtWidgets import QGridLayout, QGroupBox
from orangewidget.utils.signals import Input, Output

from Utils.UiHelper import UiHelper
from Utils.Utils import Utils


class EpochExtraction(widget.OWWidget):
    name = "EEG Epoch Extraction"
    description = "Widget for epoch extraction from RAW EEG data"
    icon = "icons/epoch-extraction.png"
    priority = 10
    want_main_area = False

    pre_stimulus_time = settings.Setting("0", schema_only=True)
    post_stimulus_time = settings.Setting("0", schema_only=True)

    # Inputs of the widget
    class Inputs:
        # Works only with mne.io.Raw, but Filter and Channel Select works with tuple of data types on the output.
        # If the input data type was set only to mne.io.Raw, this widget wouldn't be able to receive data from those
        # widgets.
        data = Input("Raw EEG data", (mne.io.Raw, mne.Epochs, mne.Evoked))

    # Outputs of the widget
    class Outputs:
        epochs = Output("Epochs", mne.Epochs)

    # Widget initialization
    def __init__(self):
        self.raw_data = None
        self.layout = None
        self.checkboxes = []
        self.confirm_button = None

        self.events = None
        self.event_ids = []
        self.event_ids_count = {}

        self.tmin_input = None
        self.tmax_input = None

        self.create_ui()

    @Inputs.data
    def set_data(self, data):
        self.clear_messages()
        self.confirm_button.setDisabled(False)

        if not issubclass(type(data), mne.io.BaseRaw):
            self.warning(f"Epoch extraction works only with mne.io.BaseRaw, got {type(data).__name__} instead.")
            self.confirm_button.setDisabled(True)
            return

        if data is not None:
            self.raw_data = data.copy()
            self.events, self.event_ids, self.event_ids_count = Utils.find_events_and_count(self.raw_data)
            self.update_ui()

    def calculate_epochs(self):
        self.clear_messages()
        event_ids = self.event_ids.copy()

        for checkbox in self.checkboxes:
            if not checkbox.isChecked():
                event_ids.pop(checkbox.objectName())

        try:
            self.pre_stimulus_time = self.tmin_input.text()
            self.post_stimulus_time = self.tmax_input.text()

            tmin = float(self.pre_stimulus_time) / 1000.0
            tmax = float(self.post_stimulus_time) / 1000.0

            if len(self.events) > 0:
                epochs = mne.Epochs(self.raw_data, self.events, tmin=tmin, tmax=tmax, preload=True,
                                    event_id=event_ids)
                self.Outputs.epochs.send(epochs)
        except ValueError:
            self.error("Values must be numbers only, and interval must be greater than 0.")

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        self.layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=self.layout)

        label_tmin = UiHelper.create_label("Pre-stimulus time (ms)")
        self.tmin_input = UiHelper.create_line_edit(self.pre_stimulus_time)

        label_tmax = UiHelper.create_label("Post-stimulus time (ms)")
        self.tmax_input = UiHelper.create_line_edit(self.post_stimulus_time)

        self.layout.addWidget(label_tmin, 0, 0)
        self.layout.addWidget(self.tmin_input, 0, 1)

        self.layout.addWidget(label_tmax, 1, 0)
        self.layout.addWidget(self.tmax_input, 1, 1)

        label = UiHelper.create_label("Found annotations:")
        self.layout.addWidget(label, 2, 0)

        self.confirm_button = UiHelper.create_button("Confirm settings",
                                                     stylesheet=UiHelper.BUTTON_STYLES['btn_success'],
                                                     callback=self.calculate_epochs)

        self.layout.addWidget(self.confirm_button, 3, 1)

    def update_ui(self):
        for checkbox in self.checkboxes:
            checkbox.setParent(None)
        self.checkboxes.clear()

        grid = QGridLayout()
        group_box = QGroupBox()

        for index in self.event_ids:
            checkbox = UiHelper.create_checkbox(Utils.format_annotation(index, self.event_ids, self.event_ids_count),
                                                name=index)
            self.checkboxes.append(checkbox)
            grid.addWidget(checkbox)

        group_box.setLayout(grid)

        self.layout.addWidget(group_box, 2, 1)
