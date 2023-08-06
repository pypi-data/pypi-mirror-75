import mne

def mark_bad_chs(data, process_params):
    data_bads = data.copy()
    # clear bads of any existing channels to avoid duplicates
    data_bads.info["bads"] = []
    for ch in process_params["bads"]:
        data_bads.info["bads"].append(ch)

    return data_bads

def interp_bad_chs(data):
    print("channels to interpolate: ", data.info["bads"])
    data_bads_interp = data.copy().interpolate_bads(reset_bads=False, verbose=True)
    return data_bads_interp

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
# process_params = {"bads": ['MEG 2443', 'EEG 053'], "interpolate": True}
#
# def test(data, process_params):
#     data_bad_chs = mark_bad_chs(data, process_params)
#     if process_params["interpolate"]:
#         data_bads_interp = interp_bad_chs(data_bad_chs)
#         print("bad channels interpolation finished")
#         return(data_bads_interp)
#
#     else:
#         print("bad channels finished")
#         return data_bad_chs
#
#
# output = test(raw, process_params)
# print("bads: ", output.info["bads"])
# print(output.info["ch_names"])
# print(type(output))

# to test interpolation for raw data:
# raw.plot(butterfly=True, color='#00000022', bad_color='r')
# output.plot(butterfly=True, color='#00000022', bad_color='r', block=True)

