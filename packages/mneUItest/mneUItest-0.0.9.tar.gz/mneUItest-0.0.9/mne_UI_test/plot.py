
import mne
from PyQt5.QtWidgets import *
from matplotlib import pyplot as plt
from mne.io.pick import get_channel_type_constants, channel_type

from .load_data import *
from .plot_func_dialog_classes import *

class PlotWindow(QWidget):
    def __init__(self, main_window):
        super(PlotWindow, self).__init__()

        self.main_window = main_window

        # initialise lists to hold tuples of data and data names here, populate later in load_in_data function
        self.data_list = [(),()] # to hold data as read in
        self.picks_data_list = [(),()] # to hold data once channels have been selected
        #self.data1 = ""
        #self.data2 = ""

        self.setWindowTitle("Plot Options")
        self.title_lbl = QLabel("Select up to two FIF files to visualise.\n \n"
                                "Both files must contain the same channels and events,\n"
                                " e.g. the results of two different preprocessing pipelines \n"
                                "run on the same raw data. \n \n"
                                "If you only wish to visualise one file, please \n"
                                "select it as File 1, not File 2. \n \n")

        self.open1_btn = QPushButton("Load 1st Data File")
        self.open1_btn.clicked.connect(lambda: self.load_in_data(1))
        self.file1_lbl = QLabel("File 1: No file loaded yet ")

        self.open2_btn = QPushButton("Load 2nd Data File")
        self.open2_btn.clicked.connect(lambda: self.load_in_data(2))
        self.file2_lbl = QLabel("File 2: No file loaded yet")

        self.select_chs_lbl = QLabel("Select channels to plot:")
        self.select_chs_cbox = QComboBox()
        self.select_chs_cbox.addItems(["All data channels", "MEG only", "EEG only", "Pick channels"])
        self.select_chs_cbox.activated[str].connect(self.update_channels)

        #self.select_plot_lbl = QLabel("Select type of plot:")
        #self.select_plot_cbox = QComboBox()
        #self.select_plot_cbox.addItems(["Time series", "Pattern spectral density"])

        #self.plot_btn = QPushButton('Plot', self)
        #self.plot_btn.clicked.connect(self.plot)

        self.time_series_tab = TimeSeriesTab(self)
        self.psd_tab = PSDTab(self)
        self.topo_epoch_image_tab = TopoEpochsImagesTab(self)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.time_series_tab, "Time Series")
        self.tabs.addTab(self.psd_tab, "PSD")
        self.tabs.addTab(self.topo_epoch_image_tab, "Topographical Epoch Images")

        layout = QGridLayout()
        layout.addWidget(self.title_lbl, 1, 0, 1, 3)

        layout.addWidget(self.open1_btn, 2, 0)
        layout.addWidget(self.file1_lbl, 3, 0, 1, 3)
        layout.addWidget(self.open2_btn, 4, 0)
        layout.addWidget(self.file2_lbl, 5, 0, 1, 3)
        layout.addWidget(self.select_chs_lbl, 6, 0)
        layout.addWidget(self.select_chs_cbox, 6, 1)
        #layout.addWidget(self.select_plot_lbl, 7, 0)
        #layout.addWidget(self.select_plot_cbox, 7, 1)
        layout.addWidget(self.tabs, 8, 0, 1, 3)
        #layout.addWidget(self.plot_btn, 8, 1)
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
                QMessageBox.warning(self, "Error", "Error reading file in to MNE. Check file type is supported")
                return

    def populate_data_and_widgets(self, data, filename, data_num):
        if data_num == 1:
            self.data_list[0] = (data, filename)
            self.file1_lbl.setText("File 1: " + filename)

            if isinstance(data, mne.BaseEpochs):
                # populate topo_epoch_images_tab combobox with keys from event_id dict
                # both sets of data should have the same events (if they are the results of different
                # pipelines run on the same data, so just take the event ids from the first set of data
                event_dict = data.event_id
                event_ids = [i for i in event_dict.keys()]
                self.topo_epoch_image_tab.populate_cbox(event_ids)

        elif data_num == 2:
            self.data_list[1] = (data, filename)
            self.file2_lbl.setText("File 2: " + filename)

    def update_channels(self):

        if len(self.data_list[0]) == 0:  # if the first data file has not been loaded
            QMessageBox.warning(self, "Error", "Ensure a data file has been selected for File 1")
            return

        else:
            for i in range(len(self.data_list)):
                if len(self.data_list[i]) != 0: # if data has been loaded
                    data = self.data_list[i][0]
                    if self.select_chs_cbox.currentText() == "All data channels":
                        self.picks_data_list[i] = data.load_data().copy().pick_types(meg=True, eeg=True, stim=False, eog=False)

                    elif self.select_chs_cbox.currentText() == "MEG only":
                        self.picks_data_list[i] = data.load_data().copy().pick_types(meg=True, eeg=False, stim=False, eog=False)

                    elif self.select_chs_cbox.currentText() == "EEG only":
                        self.picks_data_list[i] = data.load_data().copy().pick_types(meg=False, eeg=True, stim=False, eog=False)

            if self.select_chs_cbox.currentText() == "Pick channels":
            # If picking specific channels to include.
            # Needs to be called outside the for loop so it is only called once, as the picked channels are applied to both data sets
            # Gets picks (using data set 1) in the following window. Once picks are selected,
            # the window calls update_channels_for_picks to update both data items in the picks_data_list.
                pick_channels_dialog = PickChannelsDialog(self)
                pick_channels_dialog.show()

    def update_channels_for_picks(self):

        for i in range(len(self.data_list)):
            if len(self.data_list[i]) != 0:
                data = self.data_list[i][0]
                self.picks_data_list[i] = data.load_data().copy().pick_types(meg=False, eeg=False, stim=False, eog=False, include=self.picks)

    def plot(self):

        fig1 = self.pick_data1.plot_psd(show=False)
        fig2 = self.pick_data2.plot_psd(show=False)

        fig1.canvas.set_window_title(self.data1_name)
        fig2.canvas.set_window_title(self.data2_name)

        plt.show()


# ---- test ---------------------------------------------------------------
# import sys
# app = QApplication(sys.argv)
# main_window = QWidget()
# main_window.show()
# dialog = PlotWindow(main_window)
# dialog.show()
# sys.exit(app.exec_())

