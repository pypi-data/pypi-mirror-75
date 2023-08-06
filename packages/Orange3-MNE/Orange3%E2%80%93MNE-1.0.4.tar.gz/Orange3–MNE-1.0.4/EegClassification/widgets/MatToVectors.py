from Orange.widgets import widget, gui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input, Output

from Utils.UiHelper import UiHelper


class MatToVectors(widget.OWWidget):
    name = "[TESTING ONLY] Split Matlab into vectors"
    description = "[TESTING ONLY] Splits Matlab file from CNNforGTN into a target and non-target vectors. " \
                  "This is a widget for a specific matlab file to verify functionality of other widgets."
    icon = "icons/testing.png"
    priority = 12
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        dict = Input("Matlab Dict", dict)

    # Outputs of the widget
    class Outputs:
        target = Output("Target Vector", dict)
        non_target = Output("Non-target Vector", dict)

    # Widget initialization
    def __init__(self):
        self.dict = None

        self.create_ui()

    def update(self):
        target_dict = {'data': self.dict['allTargetData'], 'sfreq': 1000, 'ch_names': ['Cz', 'Fz', 'Pz']}
        non_target_dict = {'data': self.dict['allNonTargetData'], 'sfreq': 1000, 'ch_names': ['Cz', 'Fz', 'Pz']}
        self.Outputs.target.send(target_dict)
        self.Outputs.non_target.send(non_target_dict)

    @Inputs.dict
    def set_dict(self, dict):
        self.dict = dict
        self.update()

    #
    # GUI Functions and Callbacks
    #
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout).setMinimumSize(QSize(300, 100))

        label = UiHelper.create_label(
            "[TESTING ONLY] Splits Matlab file from CNNforGTN into a target and non-target vectors. " \
            "This is a widget for a specific matlab file to verify functionality of other widgets.")
        label.setWordWrap(True)
        layout.addWidget(label)
