import mne
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input

from Utils.UiHelper import UiHelper


class CompareEvokedsPlot(widget.OWWidget):
    name = "EEG Compare Evokeds Plot"
    description = "Plots multiple Evokeds for better comparison."
    icon = "icons/compare-evokeds.png"
    priority = 10
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        evoked = Input("Evoked", mne.Evoked, multiple=True)

    # Outputs of the widget
    class Outputs:
        pass

    # Widget initialization
    def __init__(self):
        self.confirm_button = None
        self.evoked_dict = {}

        self.create_ui()

    @Inputs.evoked
    def set_evoked(self, evoked, id):
        if evoked is not None:
            self.evoked_dict[str(id[0])] = evoked
        else:
            del self.evoked_dict[str(id[0])]

        if len(self.evoked_dict) > 0:
            self.confirm_button.setDisabled(False)
        else:
            self.confirm_button.setDisabled(True)

    def show_plot(self):
        mne.viz.plot_compare_evokeds(self.evoked_dict)

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        self.confirm_button = UiHelper.create_button(text="Show Compare Plot", callback=self.show_plot)
        self.confirm_button.setDisabled(True)
        layout.addWidget(self.confirm_button)
