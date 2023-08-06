import os

import scipy.io
from Orange.widgets import widget, gui, settings
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Output

from Utils.UiHelper import UiHelper


class MatReader(widget.OWWidget):
    name = "Matlab File Reader"
    description = "Reader for the Matlab .mat file format."
    icon = "icons/matlab.png"
    priority = 10
    want_main_area = False

    file_name = settings.Setting("", schema_only=True)

    # Inputs of the widget
    class Inputs:
        pass

    # Outputs of the widget
    class Outputs:
        matlab_data = Output("Matlab Dict", dict)

    # Widget initialization
    def __init__(self):
        self.filename_input = None
        self.data = None

        self.create_ui()
        self.load_data()

    def load_data(self):
        self.clear_messages()
        self.filename_input.setText(self.file_name)

        if self.file_name != "":
            if not os.path.exists(self.file_name):
                self.warning("File was not found.")
                return

            try:
                self.data = scipy.io.loadmat(self.file_name)
                self.Outputs.matlab_data.send(self.data)
            except:
                self.error("An error has occurred when loading .mat data.")

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout).setMinimumSize(QSize(400, 100))

        self.filename_input = UiHelper.create_line_edit(self.file_name, read_only=True)

        browse_button = UiHelper.create_button(text=".mat file",
                                               callback=self.browse_file)

        layout.addWidget(self.filename_input, 0, 0)
        layout.addWidget(browse_button, 0, 1)

    def browse_file(self):
        file_name = UiHelper.file_dialog(['.mat (*.mat)'])
        self.file_name = file_name
        self.load_data()
