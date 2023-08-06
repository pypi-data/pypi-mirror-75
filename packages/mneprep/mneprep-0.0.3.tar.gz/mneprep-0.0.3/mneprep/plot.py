
import mne
from PyQt5.QtWidgets import *
from matplotlib import pyplot as plt
from mne.io.pick import get_channel_type_constants, channel_type

from mneprep.plot_func_dialog_classes import *

class PlotWindow(QWidget):
    def __init__(self, main_window):
        super(PlotWindow, self).__init__()

        self.main_window = main_window

        # initialise lists to hold tuples of data and data names here, populate later in load_in_data function
        self.data_list = [(),()] # to hold data as read in
        #self.picks_data_list = [(),()] # to hold data once channels have been selected
        #self.data1 = ""
        #self.data2 = ""

        self.setWindowTitle("Plot Options")
        self.title_lbl = QLabel("Select up to two FIF files to visualise.\n \n"
                                "Both files must contain the same channels and events,\n"
                                " e.g. the results of two different preprocessing pipelines \n"
                                "run on the same raw data. \n \n"
                                "If you only wish to visualise one file, please \n"
                                "select it as File 1, not File 2. \n")

        self.open1_btn = QPushButton("Load 1st Data File")
        self.open1_btn.clicked.connect(lambda: self.load_in_data(1))
        self.file1_lbl = QLabel("File 1: No file loaded yet ")

        self.open2_btn = QPushButton("Load 2nd Data File")
        self.open2_btn.clicked.connect(lambda: self.load_in_data(2))
        self.file2_lbl = QLabel("File 2: No file loaded yet")

        self.select_chs_lbl = QLabel("Select channels to plot:")
        self.select_chs_cbox = QComboBox()
        self.select_chs_cbox.activated[str].connect(self.pick_channels)
        self.select_chs_cbox.setFixedWidth(150)

        self.time_series_tab = TimeSeriesTab(self)
        self.psd_tab = PSDTab(self)
        self.topo_epoch_evoked_tab = TopoEpochsEvokedTab(self)
        self.topo_epoch_evoked_tab.setDisabled(True)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.time_series_tab, "Time Series")
        self.tabs.addTab(self.psd_tab, "PSD")
        self.tabs.addTab(self.topo_epoch_evoked_tab, "Epochs and Evoked Responses")

        layout = QGridLayout()
        layout.addWidget(self.title_lbl, 1, 0, 1, 3)

        layout.addWidget(self.open1_btn, 2, 0)
        layout.addWidget(self.file1_lbl, 3, 0, 1, 3)
        layout.addWidget(self.open2_btn, 4, 0)
        layout.addWidget(self.file2_lbl, 5, 0, 1, 3)
        layout.addWidget(self.select_chs_lbl, 6, 0)
        layout.addWidget(self.select_chs_cbox, 6, 1)
        layout.addWidget(self.tabs, 8, 0, 1, 3)
        self.setLayout(layout)

    def load_in_data(self, data_num):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open...", "",
                                                  "(*.fif)", options=options)

        if fileName != "":
            try:
                fname = fileName.split("/")[-1]
                # load data
                if fileName.endswith("raw.fif"):
                    data = mne.io.read_raw_fif(fileName)
                    self.populate_data_and_widgets(data, fname, data_num)
                elif fileName.endswith("epo.fif"):
                    data = mne.read_epochs(fileName)
                    self.populate_data_and_widgets(data, fname, data_num)

            except ValueError:
                QMessageBox.warning(self, "Error", "Problem reading file in to MNE. Check file type is supported")
                return

    def populate_data_and_widgets(self, data, filename, data_num):
        if data_num == 1:
            self.data_list[0] = (data, filename)
            self.file1_lbl.setText("File 1: " + filename)
            #self.picks_data_list[0] = data # set picks data as the data as/
            # it is as default, then overwrite later if a subsection of channels are picked

            self.select_chs_cbox.clear()
            self.select_chs_cbox.addItems(["All data channels", "Pick channels"])
            if "eeg" in data:
                self.select_chs_cbox.addItem("EEG only")
            if "meg" in data:
                self.select_chs_cbox.addItem("MEG only")

            if isinstance(data, mne.BaseEpochs):
                # populate topo_epoch_evoked_tab combobox with keys from event_id dict
                # both sets of data should have the same events if they are the results of different
                # pipelines run on the same data, so just take the event ids from the first set of data
                event_dict = data.event_id
                event_ids = [i for i in event_dict.keys()]
                self.topo_epoch_evoked_tab.populate_cbox(event_ids)

        elif data_num == 2:
            self.data_list[1] = (data, filename)
            self.file2_lbl.setText("File 2: " + filename)

        self.toggle_enabled_plots()

    def get_data_updated_chs(self):

        if len(self.data_list[0]) == 0:  # if the first data file has not been loaded
            QMessageBox.warning(self, "File 1 Required", "Ensure a data file has been selected for File 1")
            return

        else:

            plot_data_list = [] # empty list to populate with the data to be plotted
                                # (ie the data with the channels selected)

            for i in range(len(self.data_list)):

                if len(self.data_list[i]) != 0:  # if data has been loaded
                    data = self.data_list[i][0]

                    if self.select_chs_cbox.currentText() == "All data channels":
                        plot_data = data.load_data().copy().pick_types(meg=True, eeg=True, stim=False, eog=False)
                        plot_data_list.append(plot_data)

                    elif self.select_chs_cbox.currentText() == "MEG only":
                        plot_data = data.load_data().copy().pick_types(meg=True, eeg=False, stim=False, eog=False)
                        plot_data_list.append(plot_data)

                    elif self.select_chs_cbox.currentText() == "EEG only":
                        plot_data = data.load_data().copy().pick_types(meg=False, eeg=True, stim=False, eog=False)
                        plot_data_list.append(plot_data)

                    elif self.select_chs_cbox.currentText() == "Pick channels":
                        plot_data = data.load_data().copy().pick_types(meg=False, eeg=False, stim=False, eog=False,
                                                                       include=self.picks)
                        plot_data_list.append(plot_data)

            return plot_data_list

    # this function checks that file 1 has been loaded, then gets the selected channels if "pick channels" is chosen
    def pick_channels(self):

        if len(self.data_list[0]) == 0:  # if the first data file has not been loaded
            QMessageBox.warning(self, "File 1 Required", "Ensure a data file has been selected for File 1")
            return

        if self.select_chs_cbox.currentText() == "Pick channels":
            pick_channels_dialog = PickChannelsDialog(self)
            pick_channels_dialog.show()

    def toggle_enabled_plots(self):
        # enable the epoch_and_evoked tab/plot functions if:
        # 1) only file 1 is loaded and it is epoched data
        # 2) both files are loaded and both files are epoched data
        data_item1 = self.data_list[0]
        data_item2 = self.data_list[1]

        # if only data one is loaded and it is epoched data
        if len(data_item1) != 0 and isinstance(data_item1[0], mne.BaseEpochs) and len(data_item2) == 0:
            self.topo_epoch_evoked_tab.setDisabled(False)
        # if both data are epochs
        elif len(data_item1) != 0 and len(data_item2) != 0 and isinstance(data_item1[0], mne.BaseEpochs) and isinstance(
                data_item2[0], mne.BaseEpochs):
            self.topo_epoch_evoked_tab.setDisabled(False)
        else:
            self.topo_epoch_evoked_tab.setDisabled(True)

# ---- test ---------------------------------------------------------------
# import sys
# app = QApplication(sys.argv)
# main_window = QWidget()
# main_window.show()
# dialog = PlotWindow(main_window)
# dialog.show()
# sys.exit(app.exec_())

