
import mne
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from mne.io.pick import channel_type, get_channel_type_constants

from mneprep.msgbxs import alert_msg


def options_dialog_cancel(dialog_window, main_window):
    reply = QMessageBox.question(dialog_window, 'Confirm',
                                       "Are you sure you want to close this window? Any unsaved changes will be lost",
                                       QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
    if reply == QMessageBox.Ok:
        dialog_window.close()
    else: # reply == QMessageBox.Cancel
        return

class FilterOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(FilterOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        # Then set up the layout
        self.setWindowTitle("Filter")

        self.method_lbl = QLabel("Filter type/method:")
        self.fir_rbtn = QRadioButton("FIR")
        self.iir_rbtn = QRadioButton("IIR")

        self.filter_info_lbl = QLabel("For a band-pass filter, enter both a high and low cutoff. "
                                      "For a high-pass or low-pass filter, enter the appropriate "
                                      "cutoff and leave the other blank.")
        self.filter_info_lbl.setWordWrap(True)

        self.l_input_lbl = QLabel("Low cutoff frequency(Hz):")
        self.l_input = QLineEdit(self)
        self.l_input.setFixedWidth(60)
        self.h_input_lbl = QLabel("High cutoff frequency(Hz):")
        self.h_input = QLineEdit(self)
        self.h_input.setFixedWidth(60)

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.setFixedWidth(150)
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.setFixedWidth(150)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        # if filter options have already been selected for this idx,
        # set the widgets to the values in the process_params dict
        # Like 'saving' the options you selected

        process_name = main_window.pipeline[idx][0]
        process_params = main_window.pipeline[idx][1]

        if process_name == "filter":
            if process_params["method"] == "fir":
                self.fir_rbtn.setChecked(True)
                self.iir_rbtn.setChecked(False)
            elif process_params["method"] == "iir":
                self.fir_rbtn.setChecked(False)
                self.iir_rbtn.setChecked(True)
            if process_params["l_freq"] == None:
                self.l_input.setText("")
            else:
                self.l_input.setText(str(process_params["l_freq"]))
            if process_params["h_freq"] == None:
                self.h_input.setText("")
            else:
                self.h_input.setText(str(process_params["h_freq"]))
        else: # if setting filter options for the first time
            self.fir_rbtn.setChecked(True) # default value


        layout = QGridLayout()
        layout.addWidget(self.method_lbl, 0, 0, 1, 2)
        layout.addWidget(self.fir_rbtn, 1, 0)
        layout.addWidget(self.iir_rbtn, 2, 0)
        layout.addWidget(self.filter_info_lbl, 3, 0, 1, 2)
        layout.addWidget(self.l_input_lbl, 4, 0)
        layout.addWidget(self.l_input, 4, 1)
        layout.addWidget(self.h_input_lbl, 5, 0)
        layout.addWidget(self.h_input, 5, 1)
        layout.addWidget(self.update_btn, 6, 0, 1, 2, Qt.AlignHCenter)
        layout.addWidget(self.cancel_btn, 7, 0, 1, 2, Qt.AlignHCenter)
        self.setLayout(layout)

    def update(self):

        for r_btn in [self.fir_rbtn, self.iir_rbtn]:
            if r_btn.isChecked():
                method = r_btn.text().lower()

        if self.l_input.text() == "":
            l_cutoff = None
        else:
            try:
                l_cutoff = int(self.l_input.text())
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Low cutoff frequency must be an integer")
                self.l_input.clear()
                return

        if self.h_input.text() == "":
            h_cutoff = None
        else:
            try:
                h_cutoff = int(self.h_input.text())
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "High cutoff frequency must be an integer")
                self.h_input.clear()
                return


        process_name = "filter"
        process_params = {"l_freq": l_cutoff, "h_freq": h_cutoff, "method": method}
        self.main_window.update_pipeline(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful","Filter settings updated")
        self.close()

class ResampleOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(ResampleOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        self.setWindowTitle("Resample")

        self.sfreq_spinbox_lbl = QLabel("New sampling frequency (Hz):")
        self.sfreq_spinbox = QSpinBox(self)
        self.sfreq_spinbox.setMaximum(9999)
        self.sfreq_spinbox.setFixedWidth(60)

        # if resample options have already been selected for this idx,
        # set the widgets to the values in the process_params dict
        # Like 'saving' the options you selected

        process_name = main_window.pipeline[idx][0]
        process_params = main_window.pipeline[idx][1]

        if process_name == "resample":
            self.sfreq_spinbox.setValue(process_params["sfreq"])
        else: # if setting filter options for the first time
            self.sfreq_spinbox.setValue(250)  # default value

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.clicked.connect(self.update)
        self.update_btn.setFixedWidth(150)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.setFixedWidth(150)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        layout = QGridLayout()
        layout.addWidget(self.sfreq_spinbox_lbl, 0, 0)
        layout.addWidget(self.sfreq_spinbox, 0, 1)
        layout.addWidget(self.update_btn, 1, 0, 1, 2, Qt.AlignHCenter)
        layout.addWidget(self.cancel_btn, 2, 0, 1, 2, Qt.AlignHCenter)
        self.setLayout(layout)

    def update(self):

        process_name = "resample"
        process_params = {"sfreq": int(self.sfreq_spinbox.value())}
        self.main_window.update_pipeline(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "Resampling settings updated")

        self.close()

class LineNoiseOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(LineNoiseOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        # Then set up the layout
        self.setWindowTitle("Remove Line Noise")

        self.method_lbl = QLabel("Notch filter type/method:")
        self.fir_rbtn = QRadioButton("FIR")
        self.iir_rbtn = QRadioButton("IIR")

        self.l_noise_lbl1 = QLabel("Line noise frequency(Hz):")
        self.l_noise_lbl2 = QLabel("(Harmonics can be included\neg 50, 100, 150)")
        self.l_noise_input = QLineEdit(self)
        self.l_noise_input.setFixedWidth(100)

        # if notch filter options have already been selected for this idx,
        # set the widgets to the values in the process_params dict
        # Like 'saving' the options you selected

        process_name = main_window.pipeline[idx][0]
        process_params = main_window.pipeline[idx][1]

        if process_name == "line_noise":
            if process_params["method"] == "fir":
                self.fir_rbtn.setChecked(True)
                self.iir_rbtn.setChecked(False)
            elif process_params["method"] == "iir":
                self.fir_rbtn.setChecked(False)
                self.iir_rbtn.setChecked(True)
            if process_params["freqs"] == None:
                self.l_input.setText("")
            else:
                if type(process_params["freqs"]) == int: # just one value eg 50
                    freqs_str = str(process_params["freqs"])
                else: # tuple eg (50, 100)
                    freqs_str = str(process_params["freqs"])[1:-1] # [1:-1] to get rid of the tuple brackets
                self.l_noise_input.setText(freqs_str)
        else:  # if setting options for the first time (default values)
            self.fir_rbtn.setChecked(True)
            self.iir_rbtn.setChecked(False)
            self.l_noise_input.setText("50")

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.setFixedWidth(150)
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.setFixedWidth(150)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        layout = QGridLayout()
        layout.addWidget(self.method_lbl, 0, 0, 1, 2)
        layout.addWidget(self.fir_rbtn, 1, 0)
        layout.addWidget(self.iir_rbtn, 2, 0)
        layout.addWidget(self.l_noise_lbl1, 3, 0)
        layout.addWidget(self.l_noise_input, 3, 1)
        layout.addWidget(self.l_noise_lbl2, 4, 0, 1, 2)
        layout.addWidget(self.update_btn, 5, 0, 1, 2, Qt.AlignHCenter)
        layout.addWidget(self.cancel_btn, 6, 0, 1, 2, Qt.AlignHCenter)

        # layout = QVBoxLayout()
        # layout.addWidget(self.method_lbl)
        # layout.addWidget(self.fir_rbtn)
        # layout.addWidget(self.iir_rbtn)
        # layout.addWidget(self.l_noise_lbl1)
        # layout.addWidget(self.l_noise_lbl2)
        # layout.addWidget(self.l_noise_input)
        # layout.addWidget(self.update_btn)
        # layout.addWidget(self.cancel_btn)
        self.setLayout(layout)

    def update(self):

        for r_btn in [self.fir_rbtn, self.iir_rbtn]:
            if r_btn.isChecked():
                method = r_btn.text().lower()

        freqs_lst = []  # empty list to hold all frequencies to be removed with notch filter

        try:
            if ", " in self.l_noise_input.text():
                split = self.l_noise_input.text().split(", ")
                for value in split:
                    freqs_lst.append(int(value))

            else:
                freqs_lst.append(int(self.l_noise_input.text()))

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Enter one or more integer values eg 50, 100, 150")
            self.l_noise_input.clear()
            return

        freqs = tuple(freqs_lst)
        process_name = "line_noise"
        process_params = {"freqs": freqs, "method": method}
        self.main_window.update_pipeline(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "Line noise removal settings updated")

        self.close()

class EpochOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(EpochOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        self.setWindowTitle("Epoch")

        self.fixed_length_rbtn = QRadioButton("Fixed length epochs")
        self.fixed_length_rbtn.clicked.connect(self.toggle_options)

        self.tstep_lbl = QLabel("Epoch interval")
        self.tstep_input = QDoubleSpinBox()
        self.tstep_input.setMinimum(0.1)
        self.tstep_input.setSingleStep(0.1)

        self.events_rbtn = QRadioButton("Epoch around events")
        self.events_rbtn.clicked.connect(self.toggle_options)

        self.tmin_lbl = QLabel("Tmin")
        self.tmin_input = QDoubleSpinBox()
        self.tmin_input.setMinimum(-10000)
        self.tmin_input.setSingleStep(0.1)

        self.tmax_lbl = QLabel("Tmax")
        self.tmax_input = QDoubleSpinBox()
        self.tmax_input.setMinimum(-10000)
        self.tmax_input.setSingleStep(0.1)

        self.autoreject_check = QCheckBox("Drop bad segments and epochs\nusing Autoreject thresholds")
        # if filter options have already been selected for this idx,
        # set the widgets to the values in the process_params dict
        # Like 'saving' the options you selected

        process_name = main_window.pipeline[idx][0]
        process_params = main_window.pipeline[idx][1]

        if process_name == "epoch":

            if process_params["tmin"] != None: # ie if events data
                self.events_rbtn.setChecked(True)
                self.fixed_length_rbtn.setChecked(False)
                self.tmin_input.setValue(process_params["tmin"])
                self.tmax_input.setValue(process_params["tmax"])
                self.tstep_input.setValue(5.0) # default value

            elif process_params["tstep"] != None: # ie if resting state data
                self.events_rbtn.setChecked(False)
                self.fixed_length_rbtn.setChecked(True)
                self.tstep_input.setValue(process_params["tstep"])
                self.tmin_input.setValue(-0.2) # default value
                self.tmax_input.setValue(0.5) # default value

            self.toggle_options()

            self.autoreject_check.setChecked(process_params["autoreject"])

        else:# set default values
            self.tstep_input.setValue(5.0)
            self.tmin_input.setValue(-0.2)
            self.tmax_input.setValue(0.5)

            if self.main_window.resting_r_btn.isChecked():
                self.fixed_length_rbtn.setChecked(True)
                self.events_rbtn.setChecked(False)
            elif self.main_window.erp_r_btn.isChecked():
                self.fixed_length_rbtn.setChecked(False)
                self.events_rbtn.setChecked(True)
            self.toggle_options()

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.setFixedWidth(150)
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.setFixedWidth(150)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        layout = QGridLayout()
        layout.addWidget(self.fixed_length_rbtn, 0, 0, 1, 2)
        layout.addWidget(self.tstep_lbl, 1, 0)
        layout.addWidget(self.tstep_input, 1, 1)

        layout.addWidget(self.events_rbtn, 2, 0, 1, 2)
        layout.addWidget(self.tmin_lbl, 3, 0)
        layout.addWidget(self.tmin_input, 3, 1)
        layout.addWidget(self.tmax_lbl, 4, 0)
        layout.addWidget(self.tmax_input, 4, 1)

        layout.addWidget(self.autoreject_check, 5, 0, 1, 2)
        layout.addWidget(self.update_btn, 6, 0, 1, 2, Qt.AlignHCenter)
        layout.addWidget(self.cancel_btn, 7, 0, 1, 2, Qt.AlignHCenter)
        self.setLayout(layout)

    def update(self):

        # error check for trying to epoch data with no events/stim channel around events
        if self.main_window.resting_r_btn.isChecked() & self.events_rbtn.isChecked():
            QMessageBox.warning(self, "No Stim Channel Selected", "Stim channel must be selected in order to epoch around events")
            return

        if self.events_rbtn.isChecked():
            tmin = self.tmin_input.value()
            tmax=self.tmax_input.value()
            tstep = None
        elif self.fixed_length_rbtn.isChecked():
            tmin = None
            tmax = None
            tstep = self.tstep_input.value()

        process_name = "epoch"
        process_params = {"tmin": tmin,
                          "tmax": tmax,
                          "tstep": tstep,
                          "autoreject": self.autoreject_check.isChecked()}
        self.main_window.update_pipeline(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "Epoch settings updated")

        self.close()

    def toggle_options(self):
        if self.events_rbtn.isChecked():
            self.tmin_input.setDisabled(False)
            self.tmax_input.setDisabled(False)
            self.tstep_input.setDisabled(True)
        elif self.fixed_length_rbtn.isChecked():
            self.tmin_input.setDisabled(True)
            self.tmax_input.setDisabled(True)
            self.tstep_input.setDisabled(False)

class ChannelOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(ChannelOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        self.setWindowTitle("Bad Channels")

        info = main_window.data.info
        channel_types = [k.upper() for k in get_channel_type_constants().keys()]

        self.channels_view = QListWidget()
        self.channels_view.setSpacing(7)
        self.channels_view.setSelectionMode(QListWidget.ExtendedSelection)

        for index, ch in enumerate(info["chs"]):
            kind = channel_type(info, index).upper()
            name = ch["ch_name"]
            item = QListWidgetItem(name + "    " + kind)
            self.channels_view.addItem(item)
            if name in info["bads"]:
                item.setSelected(True)

        self.interp_check = QCheckBox("Interpolate bad channels")

        # if channel options have already been selected for this idx,
        # set interp channel checkbox to the value in the process_params dict
        # Like 'saving' the option you selected

        process_name = main_window.pipeline[idx][0]
        process_params = main_window.pipeline[idx][1]

        if process_name == "channels":
            if process_params["interpolate"] == True:
                self.interp_check.setChecked(True)
            elif process_params["interpolate"] == False:
                self.interp_check.setChecked(False)
        else:  # if setting options for the first time (default values)
            self.interp_check.setChecked(True)

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.setFixedWidth(150)
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.setFixedWidth(150)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        layout = QVBoxLayout()
        layout.addWidget(self.channels_view)
        layout.addWidget(self.interp_check)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.cancel_btn)
        layout.setAlignment(self.update_btn, Qt.AlignHCenter)
        layout.setAlignment(self.cancel_btn, Qt.AlignHCenter)
        self.setLayout(layout)

    def update(self):

        bads = []
        for item in self.channels_view.selectedItems():
            ch_name = item.text().split("   ")[0]
            bads.append(ch_name)

        process_name = "channels"
        process_params = {"bads": bads, "interpolate": self.interp_check.isChecked()}
        self.main_window.update_pipeline(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "Bad channel settings updated")

        self.close()

class BaseLineOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(BaseLineOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        self.setWindowTitle("Baseline")

        self.baseline_lbl = QLabel("Interval over which to baseline:")
        self.a_lbl = QLabel("Start")
        self.a_input = QDoubleSpinBox()
        self.a_input.setMinimum(-10000)
        self.a_input.setSingleStep(0.1)
        self.b_lbl = QLabel("End")
        self.b_input = QDoubleSpinBox()
        self.b_input.setMinimum(-10000)
        self.b_input.setSingleStep(0.1)

        # if filter options have already been selected for this idx,
        # set the widgets to the values in the process_params dict
        # Like 'saving' the options you selected

        process_name = main_window.pipeline[idx][0]
        process_params = main_window.pipeline[idx][1]

        if process_name == "baseline":
            interval = process_params["interval"] # eg (a, b)
            self.a_input.setValue(interval[0])
            self.b_input.setValue(interval[1])
        else:  # if setting filter options for the first time
            self.a_input.setValue(-0.2) # default value
            self.b_input.setValue(0)  # default value

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.setFixedWidth(150)
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.setFixedWidth(150)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        layout = QGridLayout()
        layout.addWidget(self.baseline_lbl, 0, 0, 1, 2)
        layout.addWidget(self.a_lbl, 1, 0)
        layout.addWidget(self.a_input, 1, 1)
        layout.addWidget(self.b_lbl, 2, 0)
        layout.addWidget(self.b_input, 2, 1)
        layout.addWidget(self.update_btn, 3, 0, 1, 2, Qt.AlignHCenter)
        layout.addWidget(self.cancel_btn, 4, 0, 1, 2, Qt.AlignHCenter)
        self.setLayout(layout)

    def update(self):

        process_name = "baseline"
        process_params = {"interval": (self.a_input.value(), self.b_input.value())}
        self.main_window.update_pipeline(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "Baseline settings updated")

        self.close()

class ICAOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(ICAOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        self.setWindowTitle("ICA")

        ica_methods = ["FastICA", "Infomax", "Picard"]
        picks = mne.pick_types(self.main_window.data.info, meg=True, eeg=True, eog=False, ecg=False)
        # print(len(picks))
        num_eeg_and_meg_chs = len(picks)

        # --- the following code is taken from the mnelab sourcecode runicadialog.py---#

        self.method_select = QComboBox()
        self.method_select.addItems(ica_methods)
        self.method_select.currentIndexChanged.connect(self.toggle_method_options)

        self.extended_label = QLabel("Extended:")
        self.extended = QCheckBox()

        self.n_comps_lbl = QLabel("Set number of components by:")

        self.n_components_r_btn = QRadioButton("Number of components:")
        self.n_components_r_btn.clicked.connect(self.toggle_n_comp_options)

        self.n_components = QSpinBox()
        self.n_components.setRange(1, num_eeg_and_meg_chs)

        self.n_components_var_r_btn = QRadioButton("Cumulative explained variance:")
        self.n_components_var_r_btn.clicked.connect(self.toggle_n_comp_options)

        self.n_components_var = QDoubleSpinBox()
        self.n_components_var.setRange(0.01, 0.99)
        self.n_components_var.setSingleStep(0.01)

        self.n_comps_btns = QButtonGroup()
        self.n_comps_btns.addButton(self.n_components_r_btn)
        self.n_comps_btns.addButton(self.n_components_var_r_btn)

        self.exclude_bad_segments_lbl = QLabel("Exclude bad segments\n (determined by Autoreject threshold):")
        self.exclude_bad_segments = QCheckBox()

        self.rejection_method_lbl = QLabel("Method for rejecting ICA components:")
        self.manual_rbtn = QRadioButton("Manually")
        self.ecg_eog_rbtn = QRadioButton("Automatically using EOG and ECG")

        self.exclusion_methods_btns = QButtonGroup()
        self.exclusion_methods_btns.addButton(self.manual_rbtn)
        self.exclusion_methods_btns.addButton(self.ecg_eog_rbtn)

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.setFixedWidth(150)
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.setFixedWidth(150)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        grid = QGridLayout()
        grid.addWidget(QLabel("Method:"), 0, 0)
        grid.addWidget(self.method_select, 0, 1)
        grid.addWidget(self.extended_label, 1, 0)
        grid.addWidget(self.extended, 1, 1)
        grid.addWidget(self.n_comps_lbl, 3, 0)
        grid.addWidget(self.n_components_r_btn, 4, 0)
        grid.addWidget(self.n_components, 4, 1)
        grid.addWidget(self.n_components_var_r_btn, 5, 0)
        grid.addWidget(self.n_components_var, 5, 1)
        grid.addWidget(self.exclude_bad_segments_lbl, 6, 0)
        grid.addWidget(self.exclude_bad_segments, 6, 1)
        grid.addWidget(self.rejection_method_lbl, 7, 0, 1, 2)
        grid.addWidget(self.manual_rbtn, 8, 0)
        grid.addWidget(self.ecg_eog_rbtn, 9, 0, 1, 2)
        grid.addWidget(self.update_btn, 10, 0, 1, 2, Qt.AlignHCenter)
        grid.addWidget(self.cancel_btn, 11, 0, 1, 2, Qt.AlignHCenter)
        self.setLayout(grid)

        self.toggle_method_options()

        # --- end of referenced code ---#

        # if filter options have already been selected for this idx,
        # set the widgets to the values in the process_params dict
        # Like 'saving' the options you selected

        process_name = main_window.pipeline[idx][0]
        process_params = main_window.pipeline[idx][1]

        if process_name == "ICA":
            # set method
            for i in range(len(ica_methods)):
                if process_params["ica_method"] == ica_methods[i].lower():
                    self.method_select.setCurrentIndex(i)
            # set "extended"
            self.extended.setChecked(process_params["extended"])
            # set n_components

            if process_params["n_components"] >= 1: # ie if num components
                self.n_components_r_btn.setChecked(True)
                self.n_components.setDisabled(False)
                self.n_components.setValue(process_params["n_components"])
                self.n_components_var_r_btn.setChecked(False)
                self.n_components_var.setValue(0.95)# default value
                self.n_components_var.setDisabled(True)

            elif process_params["n_components"] < 1:  # ie if variance explained
                self.n_components_var_r_btn.setChecked(True)
                self.n_components_var.setDisabled(False)
                self.n_components_var.setValue(process_params["n_components"])
                self.n_components.setDisabled(True)
                self.n_components.setValue(num_eeg_and_meg_chs) # default value
                self.n_components_r_btn.setChecked(False)

            self.toggle_n_comp_options()
            # set autoreject
            self.exclude_bad_segments.setChecked(process_params["autoreject"])
            # set rejection method
            if process_params["rejection_method"] == "manual":
                self.manual_rbtn.setChecked(True)
                self.ecg_eog_rbtn.setChecked(False)
            elif process_params["rejection_method"] == "ecg_eog":
                self.manual_rbtn.setChecked(False)
                self.ecg_eog_rbtn.setChecked(True)

        else: # set default values (if selecting options for the first time)
            self.method_select.setCurrentIndex(0)
            self.extended.setChecked(False)
            self.n_components_r_btn.setChecked(True)
            self.n_components.setValue(num_eeg_and_meg_chs)
            self.n_components_var.setDisabled(True)
            self.n_components_var.setValue(0.95)
            self.exclude_bad_segments.setChecked(True)
            self.manual_rbtn.setChecked(True)
            self.ecg_eog_rbtn.setChecked(False)

    def toggle_method_options(self):
        # --- this function is taken from the mnelab sourcecode runicadialog.py---#
        """Toggle extended options."""
        if self.method_select.currentText() == "Picard":  # enable extended and ortho
            self.extended_label.setEnabled(True)
            self.extended.setEnabled(True)

        elif self.method_select.currentText() == "Infomax":  # enable extended
            self.extended_label.setEnabled(True)
            self.extended.setEnabled(True)
        else:
            self.extended_label.setEnabled(False)
            self.extended.setChecked(False)
            self.extended.setEnabled(False)

    def toggle_n_comp_options(self):

        if self.n_components_r_btn.isChecked():
            self.n_components.setDisabled(False)
            self.n_components_var.setDisabled(True)

        elif self.n_components_var_r_btn.isChecked():
            self.n_components.setDisabled(True)
            self.n_components_var.setDisabled(False)

    def update(self):

        if self.manual_rbtn.isChecked():
            rej_method = "manual"
        elif self.ecg_eog_rbtn.isChecked():
            rej_method = "ecg_eog"

        if self.n_components_r_btn.isChecked():
            n_components = self.n_components.value()
        elif self.n_components_var_r_btn.isChecked():
            n_components = self.n_components_var.value()

        process_name = "ICA"
        process_params = {"n_components": n_components,
                          "ica_method": self.method_select.currentText().lower(),
                          "extended": self.extended.isChecked(),
                          "autoreject": self.exclude_bad_segments.isChecked(),
                          "rejection_method": rej_method}
        self.main_window.update_pipeline(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "ICA settings updated")

        self.close()



