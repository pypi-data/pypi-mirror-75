import mne
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input, Output

from Utils.UiHelper import UiHelper


class EpochsToVector(widget.OWWidget):
    name = "EEG Epochs to Vector"
    description = "Creates feature vector from the extracted epochs. This vector is used in classificators."
    icon = "icons/epochs-to-vector.png"
    priority = 10
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        epochs = Input("Epochs", (mne.io.BaseRaw, mne.Epochs, mne.Evoked))

    # Outputs of the widget
    class Outputs:
        epochs_vector = Output("EEG Epochs Vector", dict)

    # Widget initialization
    def __init__(self):
        self.epochs = None
        self.information_label = UiHelper.create_label("Waiting for input data.")

        self.create_ui()

    @Inputs.epochs
    def set_epochs(self, epochs):
        self.clear_messages()

        if not issubclass(type(epochs), mne.BaseEpochs):
            self.warning("Input must be Epochs only.")
            return

        self.epochs = epochs

        if epochs is not None:
            self.update()

    def update(self):
        data_dict = {'data': self.epochs.get_data(),
                     'sfreq': self.epochs.info.get('sfreq'),
                     'stimuli': self.epochs.event_id.values(),
                     'ch_names': self.epochs.ch_names}
        self.Outputs.epochs_vector.send(data_dict)

        self.information_label.setText(f"Successfuly converted {self.epochs.get_data().shape[0]} epochs.")

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label("This widget converts Epochs to a vector (numpy array).",
                                      stylesheet=UiHelper.LABEL_SECONDARY)

        layout.addWidget(label)
        layout.addWidget(self.information_label)
