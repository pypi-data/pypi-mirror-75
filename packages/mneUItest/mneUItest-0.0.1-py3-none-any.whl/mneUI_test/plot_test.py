import mne
from matplotlib import pyplot as plt

#event_dict = {'auditory/left': 1, 'auditory/right': 2, 'visual/left': 3,
  #            'visual/right': 4, 'smiley': 5, 'buttonpress': 32}

raw = mne.io.read_raw_fif("ExampleData/sample_audvis_raw.fif", preload=True)
events =  mne.find_events(raw, stim_channel="STI 014")
#epochs = mne.Epochs(raw, events=events, event_id=event_dict, tmin=-0.2, tmax=0.5)
epochs = mne.Epochs(raw, events=events, tmin=-0.2, tmax=0.5)

aud_epochs = epochs["1"]
aud_evoked = aud_epochs.average()

picks_epochs = epochs.copy().load_data().pick_types(meg=False, eeg=False, stim=False, eog=False, include=["EEG 050", "EEG 051", "EEG 052", "EEG 053"])
picks_aud_epochs = picks_epochs["1"]
picks_aud_evoked = picks_aud_epochs.average()

#fig1 = aud_epochs.plot_image(picks=["EEG 050", "EEG 051", "EEG 052"], show=False)
#fig1 = aud_epochs.plot_image(picks=["EEG 050", "EEG 051", "EEG 052"], combine="mean", show=False)
#fig2 = picks_aud_epochs.plot_image(combine="mean", show=False)
#fig2 = mne.viz.plot_compare_evokeds(picks_aud_evoked, combine="mean", show_sensors='upper right', show=False)

#plt.show()

# plot topo image (epochs)
# for ch_type, title in dict(mag='Magnetometers', grad='Gradiometers').items():
#     layout = mne.channels.find_layout(aud_epochs.info, ch_type=ch_type)
#     aud_epochs['1'].plot_topo_image(layout=layout, fig_facecolor='w',
#                                             font_color='k', title=title)
#

print(epochs.event_id)



