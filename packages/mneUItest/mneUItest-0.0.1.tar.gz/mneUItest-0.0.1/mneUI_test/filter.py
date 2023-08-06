import mne

def filter_func(data, process_params):
    data_filtered = data.copy().filter(l_freq=process_params["l_freq"],
                                       h_freq=process_params["h_freq"],
                                       method=process_params["method"])
    return data_filtered


# ---- test -----------------------------------------------------

# import os
# sample_data_folder = mne.datasets.sample.data_path()
# sample_data_raw_file = os.path.join(sample_data_folder, "MEG", "sample", "sample_audvis_raw.fif")
#
# raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True, verbose=False)
# events = mne.find_events(raw, stim_channel='STI 014', verbose=False)
# epochs = mne.Epochs(raw, events, verbose=False)
# evoked = epochs.average()
#
# process_params = {"l_freq": 10, "h_freq":70, "method": "fir"}
#
# output = filter_func(raw, process_params)
# print(output.info)
# print(type(output))
