import os

import mne
from Orange.widgets import widget
from orangewidget.utils.signals import Output

from EegDataIO.widgets.AbstractReader import AbstractReader


class EegLabReader(widget.OWWidget, AbstractReader):
    """
    Widgets that loads .set files from EEG lab and outputs them as a mne.io.Raw
    """
    name = "EEGLAB reader"
    description = "Reads EEGLAB set files"
    icon = "icons/eeglab.png"
    priority = 10
    want_main_area = False

    class Outputs:
        output = Output("Raw EEG data", mne.io.Raw)

    def __init__(self):
        self.file_extensions = ["EEGLAB .set Files (*.set)"]
        self.load_button_text = ".set file"

        self.create_ui(self.controlArea)
        self.update()

    def load_data(self):
        self.clear_messages()
        self.text.setText(self.file_name)

        if self.file_name != "":
            if not os.path.exists(self.file_name):
                self.warning("File was not found.")
                return

            try:
                self.raw_data = mne.io.eeglab.read_raw_eeglab(self.file_name, preload=True)

                if self.montage_type is not None:
                    try:
                        montage = mne.channels.make_standard_montage(kind=self.montage_type)
                        self.raw_data.set_montage(montage, match_case=False)
                    except ValueError as err:
                        self.warning("File was loaded successfully, but montage was not loaded.")

                self.Outputs.output.send(self.raw_data)
            except:
                self.error("An error has occurred when loading .set file.")
