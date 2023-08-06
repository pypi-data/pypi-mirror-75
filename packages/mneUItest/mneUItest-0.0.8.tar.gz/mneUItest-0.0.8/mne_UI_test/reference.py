import mne


def set_reference_func(data, process_params):

    data_ref_to_av = data.copy().set_eeg_reference(ref_channels=process_params["ref_channels"], projection=False)

    return data_ref_to_av

# ---- test -----------------------------------------------------
#
# import os
#
# sample_data_folder = mne.datasets.sample.data_path()
# sample_data_raw_file = os.path.join(sample_data_folder, "MEG", "sample", "sample_audvis_raw.fif")
#
# raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True, verbose=False)
# events = mne.find_events(raw, stim_channel='STI 014', verbose=False)
# epochs = mne.Epochs(raw, events, verbose=False)
# evoked = epochs.average()
#
# process_params = {"ref_channels": "average"}
# from mne.io.pick import get_channel_type_constants
# channel_types = [k.upper() for k in get_channel_type_constants().keys()]
# if "EEG" in channel_types:
#     output = set_reference_func(evoked, process_params)
#     print(output.info)
#     print(type(output))
# else:
#     print("Error: No EEG channel data found")
#
