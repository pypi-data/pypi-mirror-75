import numpy as np
from Orange.widgets import widget, gui
from PyQt5.QtWidgets import QGridLayout
from orangewidget import settings
from orangewidget.utils.signals import Input, Output
from sklearn import preprocessing

from EegClassification.structs.ClassificationStruct import ClassificationStruct
from Utils.UiHelper import UiHelper


class WindowedMeans(widget.OWWidget):
    name = "Windowed Means"
    description = "Averages selected time intervals"
    icon = "icons/windowed-means.png"
    priority = 4
    want_main_area = False

    min_latency = settings.Setting(300, schema_only=True)
    max_latency = settings.Setting(1000, schema_only=True)
    steps = settings.Setting(21, schema_only=True)
    pre_epoch = settings.Setting(-200, schema_only=True)
    sampling_frequency = settings.Setting(1000, schema_only=True)

    # Inputs of the widget
    class Inputs:
        struct = Input("Classification Struct", ClassificationStruct)

    # Outputs of the widget
    class Outputs:
        struct = Output("Classification Struct", ClassificationStruct)

    # Widget initialization
    def __init__(self):
        self.struct = None
        self.struct_original = None

        self.intervals = None
        self.min_latency_input = None
        self.max_latency_input = None
        self.steps_input = None
        self.pre_epoch_input = None
        self.sampling_frequency_input = None
        self.confirm_button = None

        self.create_ui()

    @Inputs.struct
    def set_struct(self, struct):
        if struct is not None:
            self.struct = struct.copy()
            self.struct_original = struct.copy()
            self.confirm_button.setDisabled(False)
            self.sampling_frequency_input.setText(str(self.struct.get_sfreq()))
        else:
            self.struct = None
            self.struct_original = None
            self.confirm_button.setDisabled(True)

    def update(self):
        try:
            self.clear_messages()
            self.save_values()
            self.calculate_intervals()
            self.windowed_means()
            self.Outputs.struct.send(self.struct)
        except ValueError as err:
            self.error("Values must be numbers only.")

    def windowed_means(self):
        """
        Function code taken over from original source code:
        https://bitbucket.org/lvareka/cnnforgtn/src/eb1327b165c02b8cb1dce6059df163117086a357/main/pre_processing.py#lines-8

        :return: void
        """
        output_features = []
        out_features = self.struct_original.get_features()

        for i in range(out_features.shape[0]):
            feature = []
            # for all EEG channels
            for j in range(out_features.shape[1]):
                time_course = out_features[i][j]
                for k in range(self.intervals.shape[0]):
                    borders = self.intervals[k] * self.sampling_frequency
                    feature.append(np.average(time_course[int(borders[0] - 1):int(borders[1] - 1)]))
            output_features.append(feature)
        self.struct.set_features(preprocessing.scale(np.array(output_features), axis=1))

    def calculate_intervals(self):
        """
        Function code taken over from the original source code:
        https://bitbucket.org/lvareka/cnnforgtn/src/eb1327b165c02b8cb1dce6059df163117086a357/main/param.py#lines-42

        :return:
        """
        min_latency = self.min_latency / 1000.0
        max_latency = self.max_latency / 1000.0

        temp_wnd = np.linspace(min_latency, max_latency, self.steps)
        self.intervals = np.zeros((self.steps - 1, 2))

        for i in range(0, temp_wnd.shape[0] - 1):
            self.intervals[i, 0] = temp_wnd[i]
            self.intervals[i, 1] = temp_wnd[i + 1]
        self.intervals = self.intervals - (self.pre_epoch / 1000.0)

    def save_values(self):
        self.min_latency = float(self.min_latency_input.text())
        self.max_latency = float(self.max_latency_input.text())
        self.steps = int(self.steps_input.text())
        self.pre_epoch = float(self.pre_epoch_input.text())

        if float(self.sampling_frequency_input.text()) > self.struct.get_sfreq():
            self.warning(f"Sampling frequency is greater than in recorded data. Using default value {self.struct.get_sfreq()}.")
            self.sampling_frequency = self.struct.get_sfreq()
        else:
            self.sampling_frequency = float(self.sampling_frequency_input.text())

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        layout = QGridLayout()
        gui.widgetBox(self.controlArea, margin=0, orientation=layout)

        label_min_latency = UiHelper.create_label("Min. latency (ms):")
        self.min_latency_input = UiHelper.create_line_edit(text=str(self.min_latency))
        layout.addWidget(label_min_latency, 0, 0)
        layout.addWidget(self.min_latency_input, 0, 1)

        label_max_latency = UiHelper.create_label("Max. latency (ms):")
        self.max_latency_input = UiHelper.create_line_edit(text=str(self.max_latency))
        layout.addWidget(label_max_latency, 1, 0)
        layout.addWidget(self.max_latency_input, 1, 1)

        label_steps = UiHelper.create_label("Number of steps:")
        self.steps_input = UiHelper.create_line_edit(text=str(self.steps))
        layout.addWidget(label_steps, 2, 0)
        layout.addWidget(self.steps_input, 2, 1)

        label_pre_epoch = UiHelper.create_label("Pre-epoch (ms):")
        self.pre_epoch_input = UiHelper.create_line_edit(text=str(self.pre_epoch))
        layout.addWidget(label_pre_epoch, 3, 0)
        layout.addWidget(self.pre_epoch_input, 3, 1)

        label_sampling_frequency = UiHelper.create_label("Sampling Frequency (Hz):")
        self.sampling_frequency_input = UiHelper.create_line_edit(text=str(self.sampling_frequency))
        layout.addWidget(label_sampling_frequency, 4, 0)
        layout.addWidget(self.sampling_frequency_input, 4, 1)

        self.confirm_button = UiHelper.create_button(text="Confirm settings",
                                                callback=self.update,
                                                stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        self.confirm_button.setDisabled(True)
        layout.addWidget(self.confirm_button, 5, 1)
