import mne

def resample_func(data, process_params):
    data_resampled = data.copy().resample(sfreq=process_params["sfreq"])
    #print(data_resampled.info)
    return data_resampled

def resample_data_and_events_func(data, process_params):
    data_resampled, events_resampled = data.copy().resample(sfreq=process_params["sfreq"], events=data.events)
    #print(data_resampled.info)
    return data_resampled, events_resampled



# ---- test -----------------------------------------------------
#
# import os
# sample_data_folder = mne.datasets.sample.data_path()
# sample_data_raw_file = os.path.join(sample_data_folder, "MEG", "sample", "sample_audvis_raw.fif")
#
# raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True, verbose=False)
# events = mne.find_events(raw, stim_channel='STI 014', verbose=False)
# epochs = mne.Epochs(raw, events, verbose=False)
# evoked = epochs.average()
#
# process_params = {"sfreq": 250}
#
# output = resample_func(raw, process_params)
# print(raw.info)
# print(output.info)
# print(type(output))
