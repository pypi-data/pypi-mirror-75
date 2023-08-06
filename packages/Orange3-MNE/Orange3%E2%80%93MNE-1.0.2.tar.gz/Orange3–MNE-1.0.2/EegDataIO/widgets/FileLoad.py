import os

import mne
from Orange.widgets import widget
from orangewidget.utils.signals import Output

from EegDataIO.widgets.AbstractReader import AbstractReader
from Utils.Utils import Utils


class FileLoad(widget.OWWidget, AbstractReader):
    name = "EEG Fif Reader"
    description = "Reader for the .fif file format. Works for Raw (-raw.fif), Epochs (-epo.fif), and Evokeds(-ave.fif)."
    icon = "icons/fif-reader.png"
    priority = 10
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        pass

    # Outputs of the widget
    class Outputs:
        output = Output("Raw EEG data", (mne.io.Raw, mne.Epochs, mne.Evoked))

    # Widget initialization
    def __init__(self):
        self.file_extensions = [".fif Files (*.fif)"]
        self.load_button_text = ".fif file"

        self.create_ui(self.controlArea)

    def load_data(self):
        self.clear_messages()
        self.text.setText(self.file_name)

        if self.file_name != "":
            if not os.path.exists(self.file_name):
                self.warning("File was not found.")
                return

            try:
                if Utils.FIF_RAW_EXTENSION in self.file_name:
                    self.raw_data = mne.io.read_raw_fif(self.file_name, preload=True)
                elif Utils.FIF_EPOCHS_EXTENSION in self.file_name:
                    self.raw_data = mne.read_epochs(self.file_name, preload=True)
                elif Utils.FIF_EVOKEDS_EXTENSION in self.file_name:
                    self.raw_data = mne.read_evokeds(self.file_name)[0]

                if self.montage_type is not None and not isinstance(self.raw_data, mne.Evoked):
                    try:
                        montage = mne.channels.make_standard_montage(kind=self.montage_type)
                        self.raw_data.set_montage(montage, match_case=False)
                    except ValueError as err:
                        self.warning("File was loaded successfully, but montage was not loaded.")

                self.Outputs.output.send(self.raw_data)
            except Exception as error:
                self.error(f"An error has occurred when loading .fif file. {error}")
