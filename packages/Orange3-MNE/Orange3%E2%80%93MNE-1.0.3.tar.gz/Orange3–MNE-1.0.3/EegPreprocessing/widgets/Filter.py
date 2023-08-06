import mne
from Orange.widgets import widget, gui, settings
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QLineEdit, QComboBox, QCheckBox
from orangewidget.utils.signals import Input, Output

from Utils.UiHelper import UiHelper


class Filter(widget.OWWidget):
    name = "EEG Filter"
    description = "Performs IIR or FIR based on the settings and parameters"
    icon = "icons/filter.png"
    priority = 10
    want_main_area = False

    IIR = "iir"
    FIR = "fir"

    IIR_F_TYPES = ["butter", "cheby1", "cheby2", "ellip", "bessel"]
    IIR_RS_RP = ["cheby1", "cheby2", "ellip"]

    FIR_WINDOWS = ["hamming", "hann", "blackman"]
    FIR_PHASES = ["zero", "zero-double", "minimum"]

    # Common settings
    method = settings.Setting("iir", schema_only=True)
    l_freq = settings.Setting(0.1, schema_only=True)
    h_freq = settings.Setting(38.0, schema_only=True)

    # IIR settings
    use_sos = settings.Setting(False, schema_only=True)
    order = settings.Setting("4", schema_only=True)
    f_type = settings.Setting("butter", schema_only=True)
    max_ripple = settings.Setting("", schema_only=True)
    max_atten = settings.Setting("", schema_only=True)

    # FIR settings
    filter_length = settings.Setting("", schema_only=True)
    fir_window = settings.Setting("hamming", schema_only=True)
    phase = settings.Setting("zero", schema_only=True)

    # Inputs of the widget
    class Inputs:
        raw_data = Input("EEG data", (mne.io.Raw, mne.Epochs, mne.Evoked))

    # Outputs of the widget
    class Outputs:
        raw_data = Output("EEG data", (mne.io.Raw, mne.Epochs, mne.Evoked))

    # Widget initialization
    def __init__(self):
        self.raw_data = None

        self.layout = None
        self.method_combo_box = None
        self.filter_group = None

        self.l_freq_input = None
        self.h_freq_input = None

        # Filter FIR
        self.filter_length = None

        # Filter settings were updated
        self.filter_confirmed = False

        self.create_ui()

    @Inputs.raw_data
    def set_data(self, raw_data):
        if raw_data is None:
            self.raw_data = None
        else:
            self.raw_data = raw_data.copy()

            # If filter was setup once, we can immediately apply filter and send to output
            if self.filter_confirmed:
                self.update()

    def update(self):
        """
        Updates the output based on the channel selected
        :return: void
        """
        self.clear_messages()
        self.method = method = self.method_combo_box.currentText()

        self.l_freq = self.l_freq_input.value()
        self.h_freq = self.h_freq_input.value()

        l_freq = self.l_freq_input.value()
        h_freq = self.h_freq_input.value()

        filtered_data = self.raw_data.copy()
        self.filter_confirmed = True

        # Settings for the IIR method
        if method == self.IIR:
            iir_params = dict()

            second_order = self.filter_group.findChild(QCheckBox, "second_order")
            if second_order is not None and second_order.isChecked():
                iir_params["output"] = "sos"
                self.use_sos = True

            order_text = self.filter_group.findChild(QLineEdit, "order").text()
            if order_text == "":
                self.error("You have to set the filter order")
                return
            iir_params["order"] = int(order_text)
            self.order = order_text

            self.f_type = f_type = self.filter_group.findChild(QComboBox, "ftype").currentText()
            iir_params["ftype"] = f_type

            if iir_params["ftype"] in self.IIR_RS_RP:
                self.max_ripple = rs = self.filter_group.findChild(QLineEdit, "rs").text()
                self.max_atten = rp = self.filter_group.findChild(QLineEdit, "rp").text()

                iir_params["rs"] = float(rs)
                iir_params["rp"] = float(rp)

                if iir_params["rs"] == "" or iir_params["rp"] == "":
                    self.error("You have to set attenuation and ripple for selected filter type")
                    return

            f_pass = h_freq
            if l_freq != 0:
                f_pass = [l_freq, h_freq]

            try:
                filtered_data.filter(l_freq=l_freq, h_freq=h_freq, method=method, iir_params=iir_params)
                self.Outputs.raw_data.send(filtered_data)
            except Exception as error:
                self.error(f"An error has occurred when filtering the data. {str(error)}")

        elif method == self.FIR:
            fir_window = self.filter_group.findChild(QComboBox, "fir_window").currentText()

            filter_length = self.filter_group.findChild(QLineEdit, "filter_length").text()
            if filter_length == "":
                self.warning("Filter length was not set, using default 'auto' value.")
                filter_length = "auto"

            phase = self.filter_group.findChild(QComboBox, "phase").currentText()

            try:
                filtered_data.filter(l_freq=l_freq, h_freq=h_freq, method=method, fir_window=fir_window,
                                     filter_length=filter_length, phase=phase)
                self.Outputs.raw_data.send(filtered_data)
            except ValueError as error:
                self.error(str(error))
            except Exception as error:
                self.error(f"An error has occurred when filtering the data. {str(error)}")

    ############################################################################################
    #
    # GUI Functions and Callbacks
    #
    ############################################################################################
    def create_ui(self):
        """
        Creates the GUI
        :return: void
        """
        self.layout = QGridLayout()
        widget_box = gui.widgetBox(self.controlArea, margin=0, orientation=self.layout)
        widget_box.setMinimumWidth(600)

        self.add_method_selection()
        self.add_filter_settings()

        grid = self.get_iir_group_settings()
        self.filter_group = QGroupBox()
        self.filter_group.setLayout(grid)
        group_label = UiHelper.create_label("Filter settings")

        self.layout.addWidget(group_label, 3, 0)
        self.layout.addWidget(self.filter_group, 3, 1)

        confirm_button = UiHelper.create_button("Confirm settings", callback=self.update,
                                                stylesheet=UiHelper.BUTTON_STYLES['btn_success'])
        self.layout.addWidget(confirm_button, 4, 1)

    def add_method_selection(self):
        """
        Adds method selection to the GUI
        :return: void
        """

        combo_label = UiHelper.create_label("Method:")
        self.method_combo_box = UiHelper.create_combo_box([self.IIR, self.FIR])
        print(self.method_combo_box.findText(self.method))
        self.method_combo_box.setCurrentIndex(self.method_combo_box.findText(self.method))
        self.method_combo_box.currentTextChanged.connect(self.method_changed)

        self.layout.addWidget(combo_label, 0, 0)
        self.layout.addWidget(self.method_combo_box, 0, 1)

    def method_changed(self, value):
        """
        Callback for the filter method selection
        :param value: selected value
        :return:
        """
        self.filter_group.setParent(None)
        self.filter_group = QGroupBox()

        if value == "iir":
            self.filter_group.setLayout(self.get_iir_group_settings())
        else:
            self.filter_group.setLayout(self.get_fir_group_settings())

        self.layout.addWidget(self.filter_group, 3, 1)

    def get_iir_group_settings(self) -> QGridLayout:
        """
        Creates a grid with the settings for the IIR filter
        :return:
        """
        grid = QGridLayout()
        sos_combo = UiHelper.create_checkbox("Second-order sections", name="second_order")
        sos_combo.setChecked(self.use_sos)
        grid.addWidget(sos_combo, 1, 0, 1, 2)

        label_order = UiHelper.create_label("Order and type:")
        order = UiHelper.create_line_edit(text=self.order, name="order")
        ftype_combo = UiHelper.create_combo_box(self.IIR_F_TYPES, name="ftype")
        ftype_combo.setCurrentIndex(ftype_combo.findText(self.f_type))

        grid.addWidget(label_order, 2, 0)
        grid.addWidget(order, 2, 1)
        grid.addWidget(ftype_combo, 2, 2)

        label_info = UiHelper.create_label("Settings for elliptic filters or Chebyshev only:")
        label_rp = UiHelper.create_label("Maximum ripple (dB)")
        rp_line_edit = UiHelper.create_line_edit(name="rp", text=self.max_ripple)
        label_rs = UiHelper.create_label("Maximum attenuation (dB)")
        rs_line_edit = UiHelper.create_line_edit(name="rs", text=self.max_atten)

        grid.addWidget(label_info, 3, 0, 1, 2)

        grid.addWidget(label_rp, 4, 0)
        grid.addWidget(rp_line_edit, 4, 1)

        grid.addWidget(label_rs, 5, 0)
        grid.addWidget(rs_line_edit, 5, 1)

        return grid

    def get_fir_group_settings(self) -> QGridLayout:
        """
        Creates a grid with the settings for the FIR filter
        :return: QGridLayout
        """
        grid = QGridLayout()

        label_filter_length = UiHelper.create_label("Filter length")
        filter_length = UiHelper.create_line_edit(placeholder="e.g., auto, 10s, 5500ms, ...", name="filter_length",
                                                  text=self.filter_length)

        grid.addWidget(label_filter_length, 2, 0)
        grid.addWidget(filter_length, 2, 1)

        label_window = UiHelper.create_label("FIR Window")
        window_combo = UiHelper.create_combo_box(self.FIR_WINDOWS, name="fir_window")
        window_combo.setCurrentIndex(window_combo.findText(self.fir_window))

        grid.addWidget(label_window, 3, 0)
        grid.addWidget(window_combo, 3, 1)

        label_phase = UiHelper.create_label("Phase")
        phase_combo = UiHelper.create_combo_box(self.FIR_PHASES, name="phase")
        phase_combo.setCurrentIndex(phase_combo.findText(self.phase))

        grid.addWidget(label_phase, 4, 0)
        grid.addWidget(phase_combo, 4, 1)

        return grid

    def add_filter_settings(self):
        """
        Adds the filter settings to the GUI
        :return: void
        """

        l_freq_label = UiHelper.create_label("Lower pass-band edge for FIR\nLower cutoff freq. for IIR")
        self.l_freq_input = UiHelper.create_spin_box(0, 1000, is_double=True, value=self.l_freq)

        self.layout.addWidget(l_freq_label, 1, 0)
        self.layout.addWidget(self.l_freq_input, 1, 1)

        h_freq_label = UiHelper.create_label("Upper pass-band edge for FIR\nUpper cutoff freq. for IIR")
        self.h_freq_input = UiHelper.create_spin_box(0, 1000, is_double=True, value=self.h_freq)

        self.layout.addWidget(h_freq_label, 2, 0)
        self.layout.addWidget(self.h_freq_input, 2, 1)
