import mne
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from matplotlib import pyplot as plt

from mne.io.pick import channel_type, get_channel_type_constants

from mneprep.prep_func_dialog_classes import options_dialog_cancel

class PickChannelsDialog(QWidget):
    def __init__(self, plot_window):
        super(PickChannelsDialog, self).__init__()

        self.plot_window = plot_window

        self.setWindowTitle("Pick Channels to Plot")

        info = self.plot_window.data_list[0][0].info

        channel_types = [k.upper() for k in get_channel_type_constants().keys()]

        self.channels_view = QListWidget()
        self.channels_view.setSpacing(7)
        self.channels_view.setSelectionMode(QListWidget.ExtendedSelection)

        for index, ch in enumerate(info["chs"]):
            kind = channel_type(info, index).upper()
            name = ch["ch_name"]
            item = QListWidgetItem(name + "    " + kind)
            self.channels_view.addItem(item)

            # if channel have already been picked, highlight them
            # Like 'saving' previously picked channels
            if hasattr(plot_window, "picks"):
                if name in plot_window.picks:
                    item.setSelected(True)

        self.update_btn = QPushButton('Update', self)
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.plot_window))

        layout = QVBoxLayout()
        layout.addWidget(self.channels_view)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.cancel_btn)
        self.setLayout(layout)

    def update(self):

        picks = []
        for item in self.channels_view.selectedItems():
            ch_name = item.text().split("   ")[0]
            picks.append(ch_name)

        if len(picks) > 0:
            self.plot_window.picks = picks
            #self.plot_window.update_channels_for_picks()
            self.close()
        else:
            QMessageBox.warning(self, "No Channels Selected", "Please select at least one channel")


class TimeSeriesTab(QWidget):
    def __init__(self, plot_window):
        super(TimeSeriesTab, self).__init__()

        self.plot_window = plot_window

        self.plot_btn = QPushButton("Plot time series")
        self.plot_btn.clicked.connect(self.plot)

        layout = QVBoxLayout()
        layout.addWidget(self.plot_btn)
        self.setLayout(layout)

    def plot(self):

        if len(self.plot_window.data_list[0]) == 0:  # if the first data file has not been loaded
            QMessageBox.warning(self, "File 1 Required", "Ensure a data file has been selected for File 1")
            return

        else:

            try:
                self.plot_data_list = self.plot_window.get_data_updated_chs() # gets data to plot (updated/selected channels)

                for i in range(len(self.plot_data_list)):
                    plot_data = self.plot_data_list[i]
                    data_name = self.plot_window.data_list[i][1]
                    fig = plot_data.plot(show=False)
                    fig.canvas.set_window_title(data_name)

                plt.show()

            except ValueError:  # if channel type present in file/data 1 but not file/data 2
                QMessageBox.warning(self, "Channel Error", "Selected channels not present in both data files")
                self.plot_window.select_chs_cbox.setCurrentIndex(0)  # reset to "all channels"
                return


class PSDTab(QWidget):
    def __init__(self, plot_window):
        super(PSDTab, self).__init__()

        self.plot_window = plot_window

        self.average_check = QCheckBox("Plot average of channels")

        self.plot_btn = QPushButton("Plot pattern spectral density")
        self.plot_btn.clicked.connect(self.plot)

        layout = QVBoxLayout()
        layout.addWidget(self.average_check)
        layout.addWidget(self.plot_btn)
        self.setLayout(layout)

    def plot(self):

        if len(self.plot_window.data_list[0]) == 0:  # if the first data file has not been loaded
            QMessageBox.warning(self, "File 1 Required", "Ensure a data file has been selected for File 1")
            return

        else:

            average = self.average_check.isChecked()

            try:
                self.plot_data_list = self.plot_window.get_data_updated_chs()  # gets data to plot (updated/selected channels)

                for i in range(len(self.plot_data_list)):
                    plot_data = self.plot_data_list[i]
                    data_name = self.plot_window.data_list[i][1]
                    fig = plot_data.plot_psd(show=False, average=average)
                    fig.canvas.set_window_title(data_name)

                plt.show()

            except ValueError:  # if channel type present in file/data 1 but not file/data 2
                QMessageBox.warning(self, "Channel Error", "Selected channels not present in both data files")
                self.plot_window.select_chs_cbox.setCurrentIndex(0)  # reset to "all channels"
                return


class TopoEpochsEvokedTab(QWidget):
    def __init__(self, plot_window):
        super(TopoEpochsEvokedTab, self).__init__()

        self.plot_window = plot_window

        self.event_select = QComboBox()
        self.event_select_lbl1 = QLabel("Select event ID")
        self.event_select_lbl2 = QLabel("Only epochs/evoked responses containing this event \nwill be plotted")

        # bold font to use for titles:
        bold_font = QFont()
        bold_font.setBold(True)

        self.plot_epochs_title_lbl = QLabel("Epochs Image Map")
        self.plot_epochs_title_lbl.setFont(bold_font)
        self.plot_epochs_info_lbl = QLabel("A topographical map showing one image for each sensor.\n"
                                           "Each image shows all the epochs for that sensor, with each\n"
                                           "row of pixels representing a single epoch and colour scale\n"
                                           "respresenting the signal value at each time point.")
        self.plot_epochs_btn = QPushButton("Plot epoch images")
        self.plot_epochs_btn.clicked.connect(self.plot_epochs)

        self.plot_evoked_title_lbl = QLabel("Evoked Responses Map")
        self.plot_evoked_title_lbl.setFont(bold_font)
        self.plot_evoked_info_lbl = QLabel("A topographical map showing one image for each sensor.\n"
                                           "Each image shows the evoked response at that sensor.\n"
                                           "If two data files have been loaded,their equivalent\n"
                                           "evoked responses are compared on each plot.\n"
                                           "Note: plotting with 'All channels' or 'MEG only' selected\n "
                                           "will plot MEG channels. Select 'EEG only' to plot EEG channels")
        self.plot_evoked_btn = QPushButton("Plot evoked responses")
        self.plot_evoked_btn.clicked.connect(self.plot_evoked)

        layout = QGridLayout()
        layout.addWidget(self.event_select_lbl1, 0, 0)
        layout.addWidget(self.event_select, 0, 1, Qt.AlignLeft)
        layout.addWidget(self.event_select_lbl2, 1, 0, 1, 2)
        layout.addWidget(self.plot_epochs_title_lbl, 2, 0, 1, 2)
        layout.addWidget(self.plot_epochs_info_lbl, 3, 0, 1, 2)
        layout.addWidget(self.plot_epochs_btn, 4, 0, 1, 2)
        layout.addWidget(self.plot_evoked_title_lbl, 5, 0, 1, 2)
        layout.addWidget(self.plot_evoked_info_lbl, 6, 0, 1, 2)
        layout.addWidget(self.plot_evoked_btn, 7, 0, 1, 2)
        self.setLayout(layout)

    def populate_cbox(self, id_lst):
        self.event_select.clear()
        self.event_select.addItems(id_lst)

    def plot_epochs(self):

        if len(self.plot_window.data_list[0]) == 0:  # if the first data file has not been loaded
            QMessageBox.warning(self, "File 1 Required", "Ensure a data file has been selected for File 1")
            return

        else:

            try:
                event_id = self.event_select.currentText()

                self.plot_data_list = self.plot_window.get_data_updated_chs()  # gets data to plot (updated/selected channels)

                for i in range(len(self.plot_data_list)):
                    plot_data = self.plot_data_list[i]
                    data_name = self.plot_window.data_list[i][1]

                    if "mag" in plot_data:
                        layout = mne.channels.find_layout(plot_data.info, ch_type='mag')
                        title = data_name + ": Magnetometers, Event ID: " + event_id
                        fig = plot_data[event_id].plot_topo_image(layout=layout, fig_facecolor='w',
                                                               font_color='k', sigma=1, title=title, show=False)
                        fig.canvas.set_window_title(data_name)

                    if "grad" in plot_data:
                        layout = mne.channels.find_layout(plot_data.info, ch_type='grad')
                        title = data_name + ": Gradiometers, Event ID: " + event_id
                        fig = plot_data[event_id].plot_topo_image(layout=layout, fig_facecolor='w',
                                                              font_color='k', sigma=1, title=title, show=False)
                        fig.canvas.set_window_title(data_name)

                    if "eeg" in plot_data:
                        layout = mne.channels.find_layout(plot_data.info, ch_type='eeg')
                        title = data_name + ": Electrodes, Event ID: " + event_id
                        fig = plot_data[event_id].plot_topo_image(layout=layout, fig_facecolor='w',
                                                              font_color='k', sigma=1, title=title, show=False)
                        fig.canvas.set_window_title(data_name)

                plt.show()

            except KeyError: # if event_id is not present in data2
                QMessageBox.warning(self, "Event Error", "Selected event is not present in both data files")
                return

            except ValueError:  # if channel type is not present in data2
                QMessageBox.warning(self, "Channel Error", "Selected channels not present in both data files")
                self.plot_window.select_chs_cbox.setCurrentIndex(0)  # reset to "all channels"
                return

    def plot_evoked(self):

        if len(self.plot_window.data_list[0]) == 0:  # if the first data file has not been loaded
            QMessageBox.warning(self, "File 1 Required", "Ensure a data file has been selected for File 1")
            return

        else:
            event_id = self.event_select.currentText()
            evokeds = []  # empty list - populate with evoked data to plot

            try:
                self.plot_data_list = self.plot_window.get_data_updated_chs()  # gets data to plot (updated/selected channels)

                for i in range(len(self.plot_data_list)):
                    plot_data = self.plot_data_list[i]
                    data_name = self.plot_window.data_list[i][1]

                    #evoked = plot_data.average()
                    #evoked.comment = data_name + " - Event ID " + event_id
                    #evokeds.append(evoked)

                    event_dict = plot_data.event_id
                    data_ids = [i for i in event_dict.keys()]

                    if event_id in data_ids: # check that the event ID is present in each data file

                        evoked = plot_data[event_id].average()
                        evoked.comment = data_name + " - Event ID " + event_id
                        evokeds.append(evoked)

                    else:
                        QMessageBox.warning(self, "Event Error", "Selected event is not present in both data files")
                        return

                mne.viz.plot_evoked_topo(evokeds)

            except KeyError: # if event_id is not present in data2
                QMessageBox.warning(self, "Event Error", "Selected event is not present in both data files")
                return

            # except ValueError:  # if the two datas do not contain the same channels
            #     QMessageBox.warning(self, "Channel Error", "Both data files must contain exactly the same channels")
            #     self.plot_window.select_chs_cbox.setCurrentIndex(0)  # reset to "all channels"
            #     return



