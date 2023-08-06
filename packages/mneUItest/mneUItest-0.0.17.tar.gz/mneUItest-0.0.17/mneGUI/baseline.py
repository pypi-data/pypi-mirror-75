def baseline_func(data, process_params):
    epochs_baselined = data.copy().apply_baseline(process_params["interval"])
    return epochs_baselined


# ---- test -----------------------------------------------------
#
# import os
# sample_data_folder = mne.datasets.sample.data_path()
# sample_data_raw_file = os.path.join(sample_data_folder, "MEG", "sample", "sample_audvis_raw.fif")
#
# raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True, verbose=False)
# events = mne.find_events(raw, stim_channel='STI 014', verbose=False)
# epochs = mne.Epochs(raw, events, verbose=False)
# # evoked = epochs.average() # even though a baseline was not applied (and should be None by default), there was no difference between the epochs.average() with and without the baseline
#
# # read in evoked data that has not been baselined
# sample_data_evk_file = os.path.join(sample_data_folder, 'MEG', 'sample',
#                                     'sample_audvis-ave.fif')
# right_vis = mne.read_evokeds(sample_data_evk_file, condition='Right visual')
#
#
# process_params = {"interval": (-0.1, 0.0)}
#
# try:
#     output = baseline_func(epochs, process_params)
#     print(output.info)
#     print(type(output))
# except ValueError as VE:
#     print("Error: ", str(VE))
# except AttributeError as AE:
#     print("Error: Baseline can only be applied to epoched or evoked data")
#
# print("baselining finished")
#
# right_vis.plot()
# output.average().plot()
#



