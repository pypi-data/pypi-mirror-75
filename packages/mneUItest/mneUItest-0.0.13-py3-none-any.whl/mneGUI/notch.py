import mne

# notch filter only works for raw data
# - error handling for this is implemented in the MainWindow so that return
#   can be used to leave the run_preprocessing function

def n_filter_func(data, process_params):
        data_notched = data.copy().notch_filter(freqs=process_params["freqs"])  # works with/without comma eg both freqs = (50) & (50,) are fine
        return data_notched


# ---- test -----------------------------------------------------

# import os
# sample_data_folder = mne.datasets.sample.data_path()
# sample_data_raw_file = os.path.join(sample_data_folder, "MEG", "sample", "sample_audvis_raw.fif")
#
# raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True, verbose=False)
# process_params = {"freqs": (50, 100)}
# output = n_filter_func(raw, process_params)
# if output:
#     output.plot_psd()
