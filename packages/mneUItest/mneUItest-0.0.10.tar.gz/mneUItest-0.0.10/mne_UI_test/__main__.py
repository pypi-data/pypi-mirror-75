import sys
import mne
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from matplotlib import pyplot as plt

from .plot import PlotWindow
from .prep_func_dialog_classes import *

from .save_data import get_valid_save_name, write_fif
from .load_data import get_open_file_name, read_raw

from .filter import filter_func
from .resample import resample_func, resample_data_and_events_func
from .notch import n_filter_func
from .reference import set_reference_func
from .baseline import baseline_func
from .epochs import epoch_func, drop_bad_epochs_func
from .bad_chs import mark_bad_chs, interp_bad_chs
from .check_channel_types import check_for_ch_type
from .ica import generate_ica, fit_ica_no_autoreject, fit_ica_with_autoreject, reject_eog_eeg_comps, apply_ica

from .pipeline_dicts import get_preset_pipeline

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.pipeline = [["", {}] for i in range(10)] # initialise

        self.options_windows = [QWidget for i in range(10)]

        process_names = ["None", "Filter", "Resample", "Remove Line Noise", "Set Reference (to Average)", "ICA",
                        "Mark Bad Channels", "Epoch", "Baseline Correct Epochs"] #, "Average Epochs"]

        self.btns = [QPushButton("Options", self) for i in range(10)]
        self.cBoxes = [QComboBox(self) for i in range(10)]

        for i in range(10):
            self.btns[i].setDisabled(True)
            self.cBoxes[i].setDisabled(True)

        for i in range(10):
            self.cBoxes[i].addItems(process_names)
            #self.cBoxes[i].activated[str].connect(lambda: self.open_options(self.cBoxes[i].currentText(), i))

        self.cBoxes[0].activated[str].connect(lambda: self.open_options(self.cBoxes[0].currentText(), 0))
        self.cBoxes[1].activated[str].connect(lambda: self.open_options(self.cBoxes[1].currentText(), 1))
        self.cBoxes[2].activated[str].connect(lambda: self.open_options(self.cBoxes[2].currentText(), 2))
        self.cBoxes[3].activated[str].connect(lambda: self.open_options(self.cBoxes[3].currentText(), 3))
        self.cBoxes[4].activated[str].connect(lambda: self.open_options(self.cBoxes[4].currentText(), 4))
        self.cBoxes[5].activated[str].connect(lambda: self.open_options(self.cBoxes[5].currentText(), 5))
        self.cBoxes[6].activated[str].connect(lambda: self.open_options(self.cBoxes[6].currentText(), 6))
        self.cBoxes[7].activated[str].connect(lambda: self.open_options(self.cBoxes[7].currentText(), 7))
        self.cBoxes[8].activated[str].connect(lambda: self.open_options(self.cBoxes[8].currentText(), 8))
        self.cBoxes[9].activated[str].connect(lambda: self.open_options(self.cBoxes[9].currentText(), 9))


        self.btns[0].clicked.connect(lambda: self.open_options(self.cBoxes[0].currentText(), 0))
        self.btns[1].clicked.connect(lambda: self.open_options(self.cBoxes[1].currentText(), 1))
        self.btns[2].clicked.connect(lambda: self.open_options(self.cBoxes[2].currentText(), 2))
        self.btns[3].clicked.connect(lambda: self.open_options(self.cBoxes[3].currentText(), 3))
        self.btns[4].clicked.connect(lambda: self.open_options(self.cBoxes[4].currentText(), 4))
        self.btns[5].clicked.connect(lambda: self.open_options(self.cBoxes[5].currentText(), 5))
        self.btns[6].clicked.connect(lambda: self.open_options(self.cBoxes[6].currentText(), 6))
        self.btns[7].clicked.connect(lambda: self.open_options(self.cBoxes[7].currentText(), 7))
        self.btns[8].clicked.connect(lambda: self.open_options(self.cBoxes[8].currentText(), 8))
        self.btns[9].clicked.connect(lambda: self.open_options(self.cBoxes[9].currentText(), 9))

        self.fname_lbl = QLabel("Data file:")
        self.fname_lbl.setWordWrap(True)

        self.resting_r_btn = QRadioButton("No stimulus channel")
        self.resting_r_btn.clicked.connect(self.toggle_options)
        self.resting_r_btn.setDisabled(True)

        self.erp_r_btn = QRadioButton("Select stimulus channel")
        self.erp_r_btn.clicked.connect(self.toggle_options)
        self.erp_r_btn.setDisabled(True)

        #self.stim_chan_lbl = QLabel("Select stimulus channel")
        self.stim_chan_select = QComboBox(self)
        self.stim_chan_select.activated[str].connect(lambda: self.get_stim_ch_and_events(self.data))
        self.stim_chan_select.setDisabled(True)

        self.confirm_btn = QPushButton("Run pipeline and save results", self)
        self.confirm_btn.clicked.connect(self.run_preprocessing)
        self.confirm_btn.setDisabled(True)


        grid_layout = QGridLayout()

        grid_layout.addWidget(self.fname_lbl, 0, 0, 1, 2)
        grid_layout.addWidget(self.resting_r_btn, 1, 0)
        grid_layout.addWidget(self.erp_r_btn, 2, 0)
        #grid_layout.addWidget(self.stim_chan_lbl, 1, 0)
        grid_layout.addWidget(self.stim_chan_select, 2, 1)

        for i in range(10):
            grid_layout.addWidget(self.cBoxes[i], i+3, 0)
            grid_layout.addWidget(self.btns[i], i+3, 1)
        grid_layout.addWidget(self.confirm_btn,14, 0)

        #--------------------------

        openAct = QAction(QIcon('open.png'), '&Open...', self)
        openAct.triggered.connect(self.load_in_data)

        plotAct = QAction('&Plot', self)
        plotAct.triggered.connect(self.plot_data)

        self.ex_pipelineAct = QAction('&Example ERP Pipeline', self)
        self.ex_pipelineAct.triggered.connect(lambda: self.load_preset_pipeline("example"))
        self.ex_pipelineAct.setDisabled(True)
        self.g_pipelineAct = QAction('&Gramfort ERP Pipeline', self)
        self.g_pipelineAct.triggered.connect(lambda: self.load_preset_pipeline("gramfort"))
        self.g_pipelineAct.setDisabled(True)
        self.m_pipelineAct = QAction('&Makoto ERP Pipeline', self)
        self.m_pipelineAct.triggered.connect(lambda: self.load_preset_pipeline("makoto"))
        self.m_pipelineAct.setDisabled(True)
        self.l_pipelineAct = QAction('&Luck ERP Pipeline', self)
        self.l_pipelineAct.triggered.connect(lambda: self.load_preset_pipeline("luck"))
        self.l_pipelineAct.setDisabled(True)
        self.r_pipelineAct = QAction('&Resting State Pipeline', self)
        self.r_pipelineAct.triggered.connect(lambda: self.load_preset_pipeline("resting"))
        self.r_pipelineAct.setDisabled(True)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAct)
        plotMenu = menubar.addMenu("&Plot")
        plotMenu.addAction(plotAct)
        pipelineMenu = menubar.addMenu("&Load Pipeline")
        pipelineMenu.addAction(self.ex_pipelineAct)
        pipelineMenu.addAction(self.g_pipelineAct)
        pipelineMenu.addAction(self.m_pipelineAct)
        pipelineMenu.addAction(self.l_pipelineAct)
        pipelineMenu.addAction(self.r_pipelineAct)

        widget = QWidget()
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)
        self.setWindowTitle("Preprocessing Window")

    def load_in_data(self):
        try:
            fileName = get_open_file_name(self)
        except TypeError: # occurs if a file is double clicked rather than clicked on then "open" button clicked
            QMessageBox.warning(self, "Warning",
                            "Please select file then click open, rather than opening file by double clicking")
            return

        if fileName != "":
            self.fileName = fileName
            try:
                # load data
                self.data = read_raw(self.fileName)

                # set label to reflect opened file
                fname = fileName.split("/")[-1]
                self.fname_lbl.setText("Data File: " + fname)

                # enable radio buttons for erp  vs resting data
                self.erp_r_btn.setDisabled(False)
                self.resting_r_btn.setDisabled(False)

            except ValueError:
                QMessageBox.warning(self, "Error", "Error reading file in to MNE. Check that file contains raw data only and that file type is supported")
                return

    def get_stim_ch_and_events(self, data):

        data.stim_channel = self.stim_chan_select.currentText()
        print(data.stim_channel)
        data.events = mne.find_events(data, stim_channel=data.stim_channel)
        if len(data.events) == 0:  # channel chosen from stim channel does not contain events
            QMessageBox.warning(self, "Error", "Selected stim channel does not contain any events")
            return

        # once events have been successfully loaded, make rest of GUI live
        for i in range(10):
            self.btns[i].setDisabled(False)
            self.cBoxes[i].setDisabled(False)
        self.confirm_btn.setDisabled(False)
        self.ex_pipelineAct.setDisabled(False)
        self.g_pipelineAct.setDisabled(False)
        self.m_pipelineAct.setDisabled(False)
        self.l_pipelineAct.setDisabled(False)
        self.r_pipelineAct.setDisabled(False)

    def toggle_options(self):

        if self.erp_r_btn.isChecked():
            # enable the combobox to select stim channel and populate it with channel names
            # so that stim channel and events can be got
            self.stim_chan_select.setDisabled(False)
            self.stim_chan_select.clear()
            self.stim_chan_select.addItems(self.data.info["ch_names"])

            # disable the rest of the GUI until events are successfully loaded
            for i in range(10):
                self.btns[i].setDisabled(True)
                self.cBoxes[i].setDisabled(True)
            self.confirm_btn.setDisabled(True)
            self.r_pipelineAct.setDisabled(True)

        if self.resting_r_btn.isChecked():
            # resting state data, therefore set stim_channel and events to empty list
            self.stim_chan_select.setDisabled(True)
            self.data.stim_channel = None
            self.data.events = []

            # disable ERP preset pipelines
            self.ex_pipelineAct.setDisabled(True)
            self.g_pipelineAct.setDisabled(True)
            self.m_pipelineAct.setDisabled(True)
            self.l_pipelineAct.setDisabled(True)

            # make rest of GUI live
            for i in range(10):
                self.btns[i].setDisabled(False)
                self.cBoxes[i].setDisabled(False)
            self.confirm_btn.setDisabled(False)
            self.r_pipelineAct.setDisabled(False) # enable resting state preset pipeline

    def open_options(self, str, idx):
        if str == "None":
            self.pipeline[idx] = ["", {}] # reset in case a process was chosen then reset to None
            alert = QMessageBox()
            alert.setText("No options")
            alert.exec_()
            print(self.pipeline)
            return
        elif str == "Filter":
            self.options_windows[idx] = FilterOptionsDialog(self, idx)
        elif str == "Resample":
            self.options_windows[idx] = ResampleOptionsDialog(self, idx)
        elif str == "Mark Bad Channels": # remove/interpolate
            self.options_windows[idx] = ChannelOptionsDialog(self, idx)
        elif str == "Set Reference (to Average)":
            # No options therefore no options window needed
            self.pipeline[idx] = ["set_reference", {"ref_channels": "average"}]
            alert = QMessageBox()
            alert.setText("No options required for this process")
            alert.exec_()
            return
        elif str == "Remove Line Noise":
            self.options_windows[idx] = LineNoiseOptionsDialog(self, idx)
        elif str == "Epoch":
            self.options_windows[idx] = EpochOptionsDialog(self, idx)
        elif str == "ICA":
            self.options_windows[idx] = ICAOptionsDialog(self, idx)
        elif str == "Baseline Correct Epochs":
            self.options_windows[idx] = BaseLineOptionsDialog(self, idx)
        self.options_windows[idx].show()

    def load_preset_pipeline(self, pipeline_name):

        self.pipeline = get_preset_pipeline(pipeline_name, self.data)

        process_list_idx_lookup = {
            "": 0, #
            "filter": 1, #
            "resample": 2, #
            "line_noise": 3, #
            "set_reference": 4, #
            "ICA": 5,
            "channels": 6, #
            "epoch": 7, # but still needs testing, doesn't always work (memory))
            "baseline": 8 #
        }
        for i in range(len(self.pipeline)):
            process_idx = process_list_idx_lookup[self.pipeline[i][0]] # look up process name
            self.cBoxes[i].setCurrentIndex(process_idx)
            #
            if self.pipeline[i][0] == "channels":
                # to get bad chs before running the pipeline
                # all other params are supplied by the params dict or by default values
                self.open_options(self.cBoxes[i].currentText(), i)

    def update_pipeline(self, idx, process, process_params):
        self.pipeline[idx][0] = process
        self.pipeline[idx][1] = process_params
        print(self.pipeline)

    def get_pipeline_process_name(self, idx):
        return self.pipeline[idx][0]

    def get_pipeline_process_params(self, idx):
        return self.pipeline[idx][1]

    def run_preprocessing(self):

        print(self.pipeline)

        # # get filename to save file once processing is done
        save_name = get_valid_save_name(self)
        if save_name == -1: # if no valid save name
            return

        # if valid save name, do preprocessing

        # at this point, if the data is ERP data the events have been saved as raw.events
        # if the data does not have events/a stim channel, raw.events will be an empty list

        #################################
        # DON'T FORGET TO TAKE THE CROP OUT ONCE FINSHED TESTING!!
        ################################
        #processes_list = [raw] # hold the resulting data after each process/step, so that each step can access the most recently processed data
        data = self.data.copy() # start with direct copy, overwrite it at each step (preserves more memory than keeping all th individual steps in a list)
        for i in range(len(self.pipeline)):

            if self.pipeline[i] != ["", {}]:
                #data = processes_list[-1]]
                if isinstance(data, mne.io.BaseRaw) or isinstance(data, mne.BaseEpochs):
                    data.load_data() # error if trying to load evoked data(?)
                process_name = self.get_pipeline_process_name(i)
                process_params = self.get_pipeline_process_params(i)
                if process_name == "filter":
                    #data_filtered = data.copy().filter(l_freq = process_params["l_freq"], h_freq = process_params["h_freq"], method=process_params["method"])
                    data_filtered = filter_func(data, process_params)
                    data = data_filtered # overwrite
                    del data_filtered # delete to free up RAM
                    #processes_list.append(data_filtered)
                    print("filtering finished")
                    print()
                elif process_name == "resample":
                    #data_resampled = data.copy().resample(sfreq=process_params["sfreq"])
                    if len(data.events) == 0: # no events/stim channel
                        data_resampled = resample_func(data, process_params)
                    else: # events need to be resampled as well as data
                        data_resampled, events_resampled = resample_data_and_events_func(data, process_params)
                        data_resampled.events = events_resampled # overwrite existing events
                    #processes_list.append(data_resampled)
                    data = data_resampled # overwrite
                    del data_resampled # delete to free up RAM
                    print("resampling finished")
                    print()
                elif process_name == "line_noise":
                    if isinstance(data, mne.io.BaseRaw):
                    #data_notched = data.copy().notch_filter(freqs=process_params["freqs"]) # works with/without comma eg both freqs = (50) & (50,) are fine
                        data_notched = n_filter_func(data, process_params)
                        #processes_list.append(data_notched)
                        data = data_notched  # overwrite
                        del data_notched  # delete to free up RAM
                        print("notch filter finished")
                        print()
                    else:
                        QMessageBox.warning(self, "Error", "Notch filter can only be applied to raw data")
                        return
                elif process_name == "set_reference":
                    # check that data actually has EEG channels
                    if check_for_ch_type(data, ["EEG"]):
                        #data_ref_to_av = data.copy().set_eeg_reference(ref_channels=process_params["ref_channels"], projection=False)
                        data_ref_to_av = set_reference_func(data, process_params)
                        #processes_list.append(data_ref_to_av)
                        data = data_ref_to_av  # overwrite
                        del data_ref_to_av  # delete to free up RAM
                        print("set reference finished")
                        print()

                    else:
                        QMessageBox.warning(self, "Error", "No EEG channels found")
                        return
                elif process_name == "channels":
                    data_bad_chs = mark_bad_chs(data, process_params)
                    if process_params["interpolate"]:
                        #data.plot(block=True) # plots to check that the channels (in raw data) have been interpolated
                        data_bads_interp = interp_bad_chs(data_bad_chs)
                        #data_bads_interp.plot(block=True) # plots to check that the channels have been interpolated
                        print("bad channels interpolation finished. interpolated:  ", data_bads_interp.info["bads"])
                        # processes_list.append(data_bads_interp)
                        data = data_bads_interp  # overwrite
                        del data_bads_interp  # delete to free up RAM
                    else:
                        #processes_list.append(data_bad_chs)
                        print("bad channels finished: ", data_bad_chs.info["bads"])
                        data = data_bad_chs  # overwrite
                    del data_bad_chs  # delete to free up RAM
                elif process_name == "epoch":

                    if isinstance(data, mne.io.BaseRaw):
                        #try:
                        if process_params["autoreject"]:
                            epochs_drop_bad = drop_bad_epochs_func(data, process_params)
                            # processes_list.append(epochs_drop_bad)
                            data = epochs_drop_bad  # overwrite
                            del epochs_drop_bad  # delete to free up RAM
                        else: # if no autoreject
                            epochs = epoch_func(data, process_params)
                            #processes_list.append(epochs)
                            data = epochs  # overwrite
                            del epochs  # delete to free up RAM
                        # except ValueError as VE: # channel chosen from stim channel does not contain events
                        #     QMessageBox.warning(self, "Error", "Selected stim channel does not contain any events")
                        #     return
                        # except AttributeError as AE: # Stim channel has not been selected from combobox
                        #     QMessageBox.warning(self, "Error", "Select stim channel")
                        #     return
                        print("epoching finished")
                        print()
                    else:
                        QMessageBox.warning(self, "Error", "Epoching can only be applied to raw data")
                        return
                elif process_name == "baseline":
                    try:
                        # epochs_baselined = data.copy().apply_baseline(process_params["interval"])
                        epochs_baselined = baseline_func(data, process_params)
                    except ValueError as VE: # if baseline interval is outside of epoch interval limits
                        QMessageBox.warning(self, "Error", str(VE))
                        return
                    except AttributeError as AE: # if data other than epoch or evoked
                        QMessageBox.warning(self, "Error", "Baseline can only be applied to epoched or evoked data")
                        return
                    #processes_list.append(epochs_baselined)
                    data = epochs_baselined  # overwrite
                    del epochs_baselined  # delete to free up RAM
                    print("baselining finished")
                    print()
                elif process_name == "ICA":
                    if isinstance(data, mne.io.BaseRaw) or isinstance(data, mne.BaseEpochs):

                        # 1) generate ICA
                        self.ica = generate_ica(data, process_params, self)

                        # 2) fit ICA
                        if process_params["autoreject"]:
                            fit_ica_with_autoreject(self.ica, data)
                        else:
                            fit_ica_no_autoreject(self.ica, data)

                        # 3) exclude components
                        if process_params["rejection_method"] == "ecg_eog":
                            # check that data actually has EOG and ECG/MEG channels
                            if check_for_ch_type(data, ["ECG", "EOG"]) \
                                    or check_for_ch_type(data, ["MAG", "EOG"]) \
                                    or check_for_ch_type(data, ["GRAD", "EOG"]):
                                reject_eog_eeg_comps(self.ica, data)
                            else:
                                QMessageBox.warning(self, "Error",
                                                    "EOG and/or ECG channels not found. Defaulting to manual rejection")
                        else: # if manual exclusion
                            # cannot use reject_comps_manual function here because
                            # the plot does not show when called in another module
                            print()
                            print("------------------ REJECTING COMPONENTS MANUALLY ---------------")
                            print()
                            print(self.ica.exclude)



                            fig = self.ica.plot_sources(data)  # plot time series of components
                            fig.subplots_adjust(top=0.9)
                            plt.suptitle("1) Select components to be removed by clicking on their time series. \n"
                                         "Clicking on the name of each component will show its topographic plot. \n"
                                         "2) To continue, press enter or close the plot", fontsize=12)

                            #fig.canvas.manager.window.move(600, 0)

                            # keep the figure open for selection of components to remove,
                            # until the plot is exited or enter is pressed

                            self.ica.finished = False

                            def press(event):
                                print('press', event.key)
                                sys.stdout.flush()
                                if event.key == 'enter':
                                    self.ica.finished = True

                            fig.canvas.mpl_connect('key_press_event', press)

                            while self.ica.finished != True & plt.fignum_exists(fig.number):
                                plt.pause(0.1)
                            plt.close()

                            # the following works to have the plot pause until it is exited, but not if enter is pressed
                            # (Keeping the press enter to continue as it is more intuitive for users)
                            # while plt.fignum_exists(fig.number):
                            #   plt.pause(0.1)

                            print(self.ica.exclude)

                            #
                            #self.ica.plot_overlay(data, exclude=self.ica.exclude, picks="eeg")
                            #self.ica.plot_overlay(data, exclude=self.ica.exclude, picks="mag")

                        # 4) apply ICA
                        reconst_data = apply_ica(self.ica, data)


                        # 5) save results
                        #processes_list.append(reconst_data)
                        data = reconst_data  # overwrite
                        del reconst_data  # delete to free up RAM
                        print("ICA finished")
                        print()

                    else:
                        QMessageBox.warning(self, "Error", "ICA is currently only available for raw or epoched data types.")
                        return

        print("Saving...")
        #saved = write_fif(processes_list[-1], save_name)
        saved = write_fif(data, save_name)
        if saved:
            alert = QMessageBox()
            alert.setText("Pipeline run and data saved successfully")
            alert.exec_()
        else:
            alert = QMessageBox()
            alert.setText("Problem saving file.")
            alert.exec_()

    def plot_data(self):

        plot_dialog = PlotWindow(self)
        plot_dialog.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QWidget()
    #main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

