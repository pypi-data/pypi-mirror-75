from Orange.widgets import settings, gui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QGridLayout

from Utils.UiHelper import UiHelper
from Utils.Utils import Utils


class AbstractReader:
    file_name = settings.Setting("", schema_only=True)
    montage_type = settings.Setting("standard_1020", schema_only=True)

    label_montage_detail = None
    montage_combo = None

    file_extensions = []
    load_button_text = ""

    control_area = None

    raw_data = None

    def __init__(self):
        self.text = None

    def browse_file(self):
        file_name = UiHelper.file_dialog(self.file_extensions)
        self.file_name = file_name
        self.load_data()

    def load_data(self):
        raise Exception("NotImplementedException")

    def montage_changed(self, value):
        self.montage_type = value
        self.label_montage_detail.setText(Utils.MONTAGE_TYPES[value])

        self.load_data()

    def create_ui(self, control_area):
        layout = QGridLayout()
        gui.widgetBox(control_area, margin=0, orientation=layout).setMinimumSize(QSize(400, 100))

        self.text = UiHelper.create_line_edit(text=self.file_name, read_only=True)
        button = UiHelper.create_button(self.load_button_text, callback=self.browse_file)

        # Input to show selected file path and button to select VHDR file
        layout.addWidget(self.text, 0, 0)
        layout.addWidget(button, 0, 1)

        self.label_montage_detail = UiHelper.create_label(text=Utils.MONTAGE_TYPES[self.montage_type],
                                                          stylesheet=UiHelper.LABEL_SECONDARY)
        self.label_montage_detail.setWordWrap(True)

        label_montage = UiHelper.create_label("Montage type:")
        self.montage_combo = UiHelper.create_combo_box(Utils.MONTAGE_TYPES)
        self.montage_combo.currentTextChanged.connect(self.montage_changed)
        self.montage_combo.setCurrentIndex(self.montage_combo.findText(self.montage_type))

        layout.addWidget(label_montage, 1, 0)
        layout.addWidget(self.montage_combo, 1, 1)
        layout.addWidget(self.label_montage_detail, 2, 0, 1, 2)
