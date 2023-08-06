import os

import mne
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input

from Utils.UiHelper import UiHelper
from Utils.Utils import Utils


class FileSave(widget.OWWidget):
    name = "EEG Fif File Save"
    description = "Saves data into a .fif file format. Works for Raw, Epochs, and Evokeds."
    icon = "icons/fif-save.png"
    priority = 10
    want_main_area = False

    file_extensions = [".fif (*.fif)"]

    # Inputs of the widget
    class Inputs:
        raw_data = Input("Raw EEG data", (mne.io.Raw, mne.Epochs, mne.Evoked))

    # Outputs of the widget
    class Outputs:
        pass

    # Widget initialization
    def __init__(self):
        self.raw_data = None

        self.create_ui()

    @Inputs.raw_data
    def set_data(self, raw_data):
        self.raw_data = raw_data

    def save_data(self):
        self.clear_messages()
        file_name = UiHelper.file_dialog(is_save_dialog=True, extensions=self.file_extensions)

        try:
            if file_name != "":
                file_name = os.path.splitext(file_name)[0]

                if isinstance(self.raw_data, mne.io.BaseRaw):
                    file_name += Utils.FIF_RAW_EXTENSION
                elif isinstance(self.raw_data, mne.Epochs):
                    file_name += Utils.FIF_EPOCHS_EXTENSION
                elif isinstance(self.raw_data, mne.Evoked):
                    file_name += Utils.FIF_EVOKEDS_EXTENSION

                self.raw_data.save(fname=file_name)
        except Exception as error:
            self.error(f"An error has occurred when saving the data. {error}")

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        save_button = UiHelper.create_button(text="Save data",
                                             stylesheet=UiHelper.BUTTON_STYLES['btn_success'],
                                             callback=self.save_data)

        layout.addWidget(save_button)
