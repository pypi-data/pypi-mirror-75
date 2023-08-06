
import mne
from PyQt5.QtWidgets import *

from mne.io.pick import channel_type, get_channel_type_constants


def options_dialog_cancel(QWidget, main_window):
    buttonReply = QMessageBox.question(QWidget, 'PyQt5 message',
                                       "Are you sure you want to close this window? Any unsaved changes will not be saved",
                                       QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
    if buttonReply == QMessageBox.Ok:
        QWidget.close()
        print(main_window.pipeline)
    if buttonReply == QMessageBox.Cancel:
        return

class FilterOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(FilterOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        # Then set up the layout
        self.setWindowTitle("Filter Options")

        self.method_lbl = QLabel("Filter type/method:")
        self.fir_rbtn = QRadioButton("FIR")
        self.iir_rbtn = QRadioButton("IIR")

        self.l_input_lbl = QLabel("Low cutoff frequency(Hz):")
        self.l_input = QLineEdit(self)
        self.h_input_lbl = QLabel("High cutoff frequency(Hz):")
        self.h_input = QLineEdit(self)

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
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


        layout = QVBoxLayout()
        layout.addWidget(self.method_lbl)
        layout.addWidget(self.fir_rbtn)
        layout.addWidget(self.iir_rbtn)
        layout.addWidget(self.l_input_lbl)
        layout.addWidget(self.l_input)
        layout.addWidget(self.h_input_lbl)
        layout.addWidget(self.h_input)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.cancel_btn)
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
                alert = QMessageBox()
                alert.setText("High cutoff frequency must be an integer")
                alert.exec_()
                self.l_input.clear()
                return

        if self.h_input.text() == "":
            h_cutoff = None
        else:
            try:
                h_cutoff = int(self.h_input.text())
            except ValueError:
                alert = QMessageBox()
                alert.setText("High cutoff frequency must be an integer")
                alert.exec_()
                self.h_input.clear()
                return


        process_name = "filter"
        process_params = {"l_freq": l_cutoff, "h_freq": h_cutoff, "method": method}
        self.main_window.update_pipeline(self.process_idx, process_name, process_params)

        alert = QMessageBox()
        alert.setText("Filter settings updated")
        alert.exec_()
        self.close()

class ResampleOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(ResampleOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        self.setWindowTitle("Resample Options")

        self.sfreq_spinbox_lbl = QLabel("New sampling frequency (Hz):")
        self.sfreq_spinbox = QSpinBox(self)
        self.sfreq_spinbox.setMaximum(9999)

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
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        layout = QVBoxLayout()
        layout.addWidget(self.sfreq_spinbox_lbl)
        layout.addWidget(self.sfreq_spinbox)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.cancel_btn)
        self.setLayout(layout)

    def update(self):

        process_name = "resample"
        process_params = {"sfreq": int(self.sfreq_spinbox.value())}
        self.main_window.update_pipeline(self.process_idx, process_name, process_params)

        alert = QMessageBox()
        alert.setText("Resampling settings updated")
        alert.exec_()
        self.close()

class LineNoiseOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(LineNoiseOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        # Then set up the layout
        self.setWindowTitle("Line Noise Filter Options")

        self.method_lbl = QLabel("Filter type/method:")
        self.fir_rbtn = QRadioButton("FIR")
        self.iir_rbtn = QRadioButton("IIR")

        self.l_noise_lbl1 = QLabel("Line noise frequency(Hz):")
        self.l_noise_lbl2 = QLabel("Harmonics can be included eg 50, 100, 150")
        self.l_noise_input = QLineEdit(self)

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
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        layout = QVBoxLayout()
        layout.addWidget(self.method_lbl)
        layout.addWidget(self.fir_rbtn)
        layout.addWidget(self.iir_rbtn)
        layout.addWidget(self.l_noise_lbl1)
        layout.addWidget(self.l_noise_lbl2)
        layout.addWidget(self.l_noise_input)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.cancel_btn)
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
            alert = QMessageBox()
            alert.setText("Enter one or more integer values eg 50, 100, 150")
            alert.exec_()
            self.l_noise_input.clear()
            return

        freqs = tuple(freqs_lst)
        process_name = "line_noise"
        process_params = {"freqs": freqs, "method": method}
        self.main_window.update_pipeline(self.process_idx, process_name, process_params)

        alert = QMessageBox()
        alert.setText("Line noise removal settings updated")
        alert.exec_()
        self.close()

class EpochOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(EpochOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        self.setWindowTitle("Epoch Options")

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

        self.autoreject_check = QCheckBox("Drop bad segments and epochs using Autoreject thresholds")

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
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        layout = QVBoxLayout()
        layout.addWidget(self.fixed_length_rbtn)
        layout.addWidget(self.tstep_lbl)
        layout.addWidget(self.tstep_input)

        layout.addWidget(self.events_rbtn)
        layout.addWidget(self.tmin_lbl)
        layout.addWidget(self.tmin_input)
        layout.addWidget(self.tmax_lbl)
        layout.addWidget(self.tmax_input)

        layout.addWidget(self.autoreject_check)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.cancel_btn)
        self.setLayout(layout)

    def update(self):

        # error check for trying to epoch data with no events/stim channel around events
        if self.main_window.resting_r_btn.isChecked() & self.events_rbtn.isChecked():
            QMessageBox.warning(self, "Error", "Stim channel must be selected to epoch around events")
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

        alert = QMessageBox()
        alert.setText("Epoch settings updated")
        alert.exec_()
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

        self.setWindowTitle("Bad Channel Options")

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
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        layout = QVBoxLayout()
        layout.addWidget(self.channels_view)
        layout.addWidget(self.interp_check)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.cancel_btn)
        self.setLayout(layout)

    def update(self):

        bads = []
        for item in self.channels_view.selectedItems():
            ch_name = item.text().split("   ")[0]
            bads.append(ch_name)

        process_name = "channels"
        process_params = {"bads": bads, "interpolate": self.interp_check.isChecked()}
        self.main_window.update_pipeline(self.process_idx, process_name, process_params)

        alert = QMessageBox()
        alert.setText("Bad channel settings updated")
        alert.exec_()
        self.close()

class BaseLineOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(BaseLineOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        self.setWindowTitle("Baseline Options")

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
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        layout = QVBoxLayout()
        layout.addWidget(self.baseline_lbl)
        layout.addWidget(self.a_lbl)
        layout.addWidget(self.a_input)
        layout.addWidget(self.b_lbl)
        layout.addWidget(self.b_input)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.cancel_btn)
        self.setLayout(layout)

    def update(self):

        process_name = "baseline"
        process_params = {"interval": (self.a_input.value(), self.b_input.value())}
        self.main_window.update_pipeline(self.process_idx, process_name, process_params)

        alert = QMessageBox()
        alert.setText("Baseline settings updated")
        alert.exec_()
        self.close()

class ICAOptionsDialog(QWidget):
    def __init__(self, main_window, idx):
        super(ICAOptionsDialog, self).__init__()

        self.main_window = main_window
        self.process_idx = idx

        self.setWindowTitle("ICA Options")

        ica_methods = ["FastICA", "Infomax", "Picard"]
        picks = mne.pick_types(self.main_window.data.info, meg=True, eeg=True, eog=False, ecg=False)
        # print(len(picks))
        num_eeg_and_meg_chs = len(picks)
        # --- the following code is taken from the mnelab sourcecode runicadialog.py---#

        vbox = QVBoxLayout(self)

        grid = QGridLayout()
        grid.addWidget(QLabel("Method:"), 0, 0)
        self.method_select = QComboBox()
        self.method_select.addItems(ica_methods)
        self.method_select.currentIndexChanged.connect(self.toggle_method_options)
        grid.addWidget(self.method_select, 0, 1)

        self.extended_label = QLabel("Extended:")
        grid.addWidget(self.extended_label, 1, 0)
        self.extended = QCheckBox()
        grid.addWidget(self.extended, 1, 1)

        grid.addWidget(QLabel("Set number of components by:"), 3, 0)

        self.n_components_r_btn = QRadioButton("Number of components:")
        self.n_components_r_btn.clicked.connect(self.toggle_n_comp_options)
        grid.addWidget(self.n_components_r_btn, 4, 0)

        self.n_components = QSpinBox()
        self.n_components.setRange(1, num_eeg_and_meg_chs)
        grid.addWidget(self.n_components, 4, 1)

        self.n_components_var_r_btn = QRadioButton("Cumulative explained variance:")
        self.n_components_var_r_btn.clicked.connect(self.toggle_n_comp_options)
        grid.addWidget(self.n_components_var_r_btn, 5, 0)

        self.n_components_var = QDoubleSpinBox()
        self.n_components_var.setRange(0.01, 0.99)
        self.n_components_var.setSingleStep(0.01)
        grid.addWidget(self.n_components_var, 5, 1)

        self.n_comps_btns = QButtonGroup()
        self.n_comps_btns.addButton(self.n_components_r_btn)
        self.n_comps_btns.addButton(self.n_components_var_r_btn)

        grid.addWidget(QLabel("Exclude bad segments\n (determined by Autoreject threshold):"), 6, 0)
        self.exclude_bad_segments = QCheckBox()
        grid.addWidget(self.exclude_bad_segments, 6, 1)

        self.rejection_method_lbl = QLabel("Method for selecting ICA components to reject")
        self.manual_rbtn = QRadioButton("Manually")
        self.ecg_eog_rbtn = QRadioButton("Automatically using EOG and ECG channels")

        self.exclusion_methods_btns = QButtonGroup()
        self.exclusion_methods_btns.addButton(self.manual_rbtn)
        self.exclusion_methods_btns.addButton(self.ecg_eog_rbtn)

        grid.addWidget(self.rejection_method_lbl, 7, 0, 1, 2)
        grid.addWidget(self.manual_rbtn, 8, 0)
        grid.addWidget(self.ecg_eog_rbtn, 9, 0)

        vbox.addLayout(grid)

        vbox.setSizeConstraint(QVBoxLayout.SetFixedSize)

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

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.clicked.connect(self.update)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

        vbox.addWidget(self.update_btn)
        vbox.addWidget(self.cancel_btn)

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

        alert = QMessageBox()
        alert.setText("ICA settings updated")
        alert.exec_()
        self.close()

# code for window for excluding IC options - no longer needed
# class ExcludeWindow(QWidget):
#     def __init__(self, n_components):
#         super(ExcludeWindow, self).__init__()
#
#         self.n_comps= n_components
#
#         v_layout = QVBoxLayout()
#         self.excludes_lbl = QLabel("Enter IC components to exclude eg 0, 1: ")
#         self.excludes = QLineEdit()
#         self.ok_btn = QPushButton("Okay")
#         self.ok_btn.clicked.connect(self.exclude_components)
#         v_layout.addWidget(self.excludes_lbl)
#         v_layout.addWidget(self.excludes)
#         v_layout.addWidget(self.ok_btn)
#         self.setLayout(v_layout)
#
#     def exclude_components(self):
#
#         comps_lst = []  # empty list to hold all components to be removed
#
#         try:
#             if ", " in self.excludes.text():
#                 split = self.excludes.text().split(", ")
#                 for value in split:
#                     comps_lst.append(int(value))
#
#             else:
#                 comps_lst.append(int(self.excludes.text()))
#
#            # check that all components are within valid range
#             for comp in comps_lst:
#                 if comp > self.n_comps:
#                     raise ValueError
#
#             main_window.ica.exclude += comps_lst
#             print(main_window.ica.exclude)
#
#         except ValueError:
#             alert = QMessageBox()
#             alert.setText("Enter one or more integer values eg 0, 1 corresponding to the plotted components")
#             alert.exec_()
#             self.excludes.clear()
#             return
#
#         alert = QMessageBox()
#         alert.setText("Components selected to exclude")
#         alert.exec_()
#         self.close()



