import mne
import numpy
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout, QGroupBox
from orangewidget.utils.signals import Input, Output

from Utils.UiHelper import UiHelper
from Utils.Utils import Utils


class Averaging(widget.OWWidget):
    name = "EEG Averaging"
    description = "Allows averaging of the epochs over the selected stimuli."
    icon = "icons/averaging.png"
    priority = 10
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        epochs = Input("Epochs", (mne.io.BaseRaw, mne.Epochs, mne.Evoked))

    # Outputs of the widget
    class Outputs:
        evoked = Output("Evoked", mne.Evoked)

    # Widget initialization
    def __init__(self):
        self.layout = None
        self.epochs = None
        self.found_channels_label = None
        self.checkboxes = []

        self.events = None
        self.event_ids = None
        self.event_ids_count = None

        self.create_ui()

    @Inputs.epochs
    def set_epochs(self, epochs):
        self.clear_messages()

        if isinstance(type(epochs), mne.io.BaseRaw) or isinstance(type(epochs), mne.Evoked):
            self.warning("Averaging works only with Epochs")
            return

        if epochs is not None:
            self.epochs = epochs.copy()
            self.load_stimuli()
        else:
            self.epochs = None

    def load_stimuli(self):
        self.event_ids = self.epochs.event_id.copy()
        self.events = self.epochs.events.copy()
        self.event_ids_count = Utils.find_count(self.events, self.event_ids)

        self.update_ui()

    def update(self):
        try:
            epochs_copy = self.epochs.copy()

            stimuli_to_drop = []
            for checkbox in self.checkboxes:
                if not checkbox.isChecked():
                    stimuli_to_drop.append(self.event_ids[checkbox.objectName()])

            average_function = lambda epochs: self.average_function(epochs, self.events.copy(), stimuli_to_drop)
            averaged = epochs_copy.average(method=average_function)

            self.Outputs.evoked.send(averaged)
        except Exception as err:
            self.error("An error has occurred when averaging the epochs. " + str(err))

    def average_function(self, epochs_array, events, stimuli_to_drop):
        events_count = epochs_array.shape[0]
        size = epochs_array.shape[1]
        data_length = epochs_array.shape[2]

        averaged = numpy.zeros((size, data_length))

        for e_index in range(events_count):
            event_id = events[e_index][2]

            if event_id not in stimuli_to_drop:
                values = epochs_array[e_index]

                for i in range(len(values)):
                    for j in range(len(values[i])):
                        averaged[i][j] += values[i][j]

        for i in range(len(averaged)):
            for j in range(len(averaged[i])):
                averaged[i][j] /= events_count

        return averaged

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        self.layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=self.layout).setMinimumWidth(250)

        found_stimuli = UiHelper.create_label("Found stimuli:")

        confirm_button = UiHelper.create_button(text="Confirm settings",
                                                stylesheet=UiHelper.BUTTON_STYLES['btn_success'],
                                                callback=self.update)
        self.layout.addWidget(found_stimuli, 1, 0)
        self.layout.addWidget(confirm_button, 2, 1)

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

        self.layout.addWidget(group_box, 1, 1)
