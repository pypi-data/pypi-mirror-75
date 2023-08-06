import mne
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input, Output

from Utils.UiHelper import UiHelper


class GrandAverage(widget.OWWidget):
    name = "EEG Grand Average"
    description = ""
    icon = "icons/grand-average.png"
    priority = 10
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        evoked = Input("Evoked", mne.Evoked, multiple=True)

    # Outputs of the widget
    class Outputs:
        evoked = Output("Evoked", mne.Evoked)

    # Widget initialization
    def __init__(self):
        self.evoked_list = {}

        self.create_ui()

    @Inputs.evoked
    def set_evoked(self, evoked, id):
        self.evoked_list[id] = evoked
        self.update()

    def update(self):
        ev = []
        for evoked in self.evoked_list:
            ev.append(self.evoked_list[evoked])

        self.Outputs.evoked.send(mne.grand_average(ev))

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label(text="This widgets creates a grand average from multiple provided averages.",
                                      stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(label)
