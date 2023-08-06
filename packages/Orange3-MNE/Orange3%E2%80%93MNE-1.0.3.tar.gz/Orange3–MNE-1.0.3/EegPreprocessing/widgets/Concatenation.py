import mne
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget.utils.signals import Input, Output

from Utils.UiHelper import UiHelper


class Concatenation(widget.OWWidget):
    name = "EEG Inputs Concatenation"
    description = ""
    icon = "icons/concatenation.png"
    priority = 10
    want_main_area = False

    # Inputs of the widget
    class Inputs:
        raw_data = Input("EEG data", (mne.io.Raw, mne.Epochs, mne.Evoked), multiple=True)

    # Outputs of the widget
    class Outputs:
        raw_data = Output("EEG data", (mne.io.Raw, mne.Epochs, mne.Evoked))

    # Widget initialization
    def __init__(self):

        self.raw_data_list = {}

        self.create_ui()

    @Inputs.raw_data
    def set_data(self, data, id):
        self.clear_messages()

        if data is not None:
            if issubclass(type(data), mne.Evoked):
                self.warning("Concatenation is not supported for the Evokeds.")
                return
            elif not self.raw_data_list:
                # The list is empty -> we can add data to concatenate
                self.raw_data_list[str(id[0])] = data.copy()
            elif isinstance(self.raw_data_list[next(iter(self.raw_data_list))], type(data)):
                # Check if new data are the same type as the first item in the dictionary, to prevent mixing types
                self.raw_data_list[str(id[0])] = data.copy()
            else:
                # Incompatible types -> show error message
                self.error(f"Inputs must have the same data type.")
                return
        else:
            del self.raw_data_list[str(id[0])]

        self.information("Ready to concatenate.")

    def update(self):
        self.clear_messages()
        try:
            data_list = []
            first_item = self.raw_data_list[next(iter(self.raw_data_list))]

            first_item_backup = None  # When concatenating, first instance is always modified, so we need a backup

            count = 0
            for k, v in self.raw_data_list.items():
                data_list.append(v)
                if count == 0:
                    first_item_backup = [k, v.copy()]
                count += 1

            if issubclass(type(first_item), mne.io.BaseRaw):
                self.Outputs.raw_data.send(mne.concatenate_raws(data_list, preload=True))
            else:
                self.Outputs.raw_data.send(mne.concatenate_epochs(data_list))

            self.raw_data_list[first_item_backup[0]] = first_item_backup[1]  # Restore from backup
            self.information("All done.")

        except Exception as ex:
            self.error(f"An error has occured when concatenating files. {str(ex)}")

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label = UiHelper.create_label(text="Widget concatenates multiple Epochs or Raw inputs into a one.\n"
                                           "Note: All inputs MUST have the same number of channels.",
                                      stylesheet=UiHelper.LABEL_SECONDARY)
        layout.addWidget(label)

        confirm_btn = UiHelper.create_button("Concatenate Files", callback=self.update,
                                             stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        layout.addWidget(confirm_btn)
