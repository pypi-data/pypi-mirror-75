import mne
from PyQt5.QtWidgets import *

from mne.io.pick import channel_type, get_channel_type_constants

from .prep_func_dialog_classes import options_dialog_cancel

from matplotlib import pyplot as plt


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
        self.cancel_btn.clicked.connect(lambda: options_dialog_cancel(self, self.main_window))

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

        self.plot_window.picks = picks
        self.close()
        self.plot_window.update_channels_for_picks()

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

        for i in range(len(self.plot_window.picks_data_list)):

            data = self.plot_window.picks_data_list[i]
            data_name = self.plot_window.data_list[i][1]
            fig = data.plot(show=False)
            fig.canvas.set_window_title(data_name)

        plt.show()

        #fig1 = self.plot_window.pick_data1.plot(show=False)
        #fig2 = self.plot_window.pick_data2.plot(show=False)
        #fig1.canvas.set_window_title(self.plot_window.data1_name)
        #fig2.canvas.set_window_title(self.plot_window.data2_name)


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

        average = self.average_check.isChecked()

        for i in range(len(self.plot_window.picks_data_list)):

            data = self.plot_window.picks_data_list[i]
            data_name = self.plot_window.data_list[i][1]
            fig = data.plot_psd(show=False, average=average)
            fig.canvas.set_window_title(data_name)

        plt.show()

        #fig1 = self.plot_window.pick_data1.plot_psd(show=False, average=average)
        #fig2 = self.plot_window.pick_data2.plot_psd(show=False, average=average)

        #fig1.canvas.set_window_title(self.plot_window.data1_name)
        #fig2.canvas.set_window_title(self.plot_window.data2_name)


class TopoEpochsImagesTab(QWidget):
    def __init__(self, plot_window):
        super(TopoEpochsImagesTab, self).__init__()

        self.plot_window = plot_window

        self.event_select = QComboBox()
        self.event_select_lbl1 = QLabel("Select event ID")
        self.event_select_lbl2 = QLabel("Only epochs containing this event \nwill be selected/plotted")

        self.plot_btn = QPushButton("Plot topographical epoch images")
        self.plot_btn.clicked.connect(self.plot)

        layout = QVBoxLayout()
        layout.addWidget(self.event_select_lbl1)
        layout.addWidget(self.event_select)
        layout.addWidget(self.event_select_lbl2)
        layout.addWidget(self.plot_btn)
        self.setLayout(layout)

    def populate_cbox(self, id_lst):
        self.event_select.clear()
        self.event_select.addItems(id_lst)

    def plot(self):

        event_id = self.event_select.currentText()

        for i in range(len(self.plot_window.picks_data_list)):

            data = self.plot_window.picks_data_list[i]
            data_name = self.plot_window.data_list[i][1]

        #for data_item in data_list:

            #data = data_item[0]
            #data_name = data_item[1]

            if "mag" in data:
                layout = mne.channels.find_layout(data.info, ch_type='mag')
                title = data_name + ": Magnetometers"
                fig = data[event_id].plot_topo_image(layout=layout, fig_facecolor='w',
                                                       font_color='k', sigma=1, title=title, show=False)
                fig.canvas.set_window_title(data_name)

            if "grad" in data:
                layout = mne.channels.find_layout(data.info, ch_type='grad')
                title = data_name + ": Gradiometers"
                fig = data[event_id].plot_topo_image(layout=layout, fig_facecolor='w',
                                                      font_color='k', sigma=1, title=title, show=False)
                fig.canvas.set_window_title(data_name)
            if "eeg" in data:
                layout = mne.channels.find_layout(data.info, ch_type='eeg')
                title = data_name + ": Electrodes"
                fig = data[event_id].plot_topo_image(layout=layout, fig_facecolor='w',
                                                      font_color='k', sigma=1, title=title, show=False)
                fig.canvas.set_window_title(data_name)

        # fig1 = self.plot_window.pick_data1.plot_psd(show=False, average=average)
        # fig2 = self.plot_window.pick_data2.plot_psd(show=False, average=average)
        #
        # fig1.canvas.set_window_title(self.plot_window.data1_name)
        # fig2.canvas.set_window_title(self.plot_window.data2_name)

        plt.show()

