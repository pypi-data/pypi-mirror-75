import mne
from Orange.widgets import widget, gui, settings
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input, Output

from Utils.UiHelper import UiHelper


class ChannelSelect(widget.OWWidget):
    name = "EEG Channel Select"
    description = "Allows to select specific channels from raw data."
    icon = "icons/channel-select.png"
    priority = 10
    want_main_area = False

    selected_channels = settings.Setting("", schema_only=True)

    # Inputs of the widget
    class Inputs:
        raw_data = Input("Raw EEG data", (mne.io.Raw, mne.Epochs, mne.Evoked))

    # Outputs of the widget
    class Outputs:
        raw_data = Output("Raw EEG data", (mne.io.Raw, mne.Epochs, mne.Evoked))

    # Widget initialization
    def __init__(self):
        self.raw_data = None
        self.raw_data_copy = None
        self.found_channels_label = None
        self.user_line_edit = None

        self.create_ui()

    @Inputs.raw_data
    def set_data(self, raw_data):
        self.raw_data = raw_data

        if raw_data is not None:
            self.found_channels_label.setText(", ".join(raw_data.ch_names))
        else:
            self.found_channels_label.setText("Raw data file does not have any channels.")

    def update(self):
        if self.raw_data_copy is not None:
            self.Outputs.raw_data.send(self.raw_data_copy)
        else:
            self.Outputs.raw_data.send(None)

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout).setMinimumSize(QSize(500, 150))

        found_channels_description = UiHelper.create_label("Found channels:")

        self.found_channels_label = UiHelper.create_label("No channels found.", stylesheet=UiHelper.LABEL_SECONDARY)
        self.found_channels_label.setFixedWidth(400)
        self.found_channels_label.setWordWrap(True)

        line_edit_label = UiHelper.create_label("Channels to select:")
        self.user_line_edit = UiHelper.create_line_edit(
            text=self.selected_channels,
            placeholder="Write the names of the channels to select, comma separated")

        confirm_button = UiHelper.create_button("Confirm settings", self.confirm_callback,
                                                stylesheet=UiHelper.BUTTON_STYLES['btn_success'])

        layout.addWidget(found_channels_description, 0, 0)
        layout.addWidget(self.found_channels_label, 0, 1, 1, 2)

        layout.addWidget(line_edit_label, 1, 0)
        layout.addWidget(self.user_line_edit, 1, 1)

        layout.addWidget(confirm_button, 2, 1)

    def confirm_callback(self):
        self.clear_messages()
        self.raw_data_copy = self.raw_data.copy()

        all_channels = self.raw_data.ch_names.copy()

        self.selected_channels = self.user_line_edit.text()
        if self.selected_channels == "":
            self.warning(
                "You have to select at least one channel. If no channel is selected, all channels are sent to Output")
            self.update()
        else:
            for channel in self.selected_channels.split(","):
                channel = channel.strip(" ")
                if channel in all_channels:
                    all_channels.remove(channel)

            self.raw_data_copy.drop_channels(all_channels)
            self.update()
