import mne
from mne.io.pick import get_channel_type_constants, channel_type


def check_for_ch_type(data, required_chs):
    # takes an mne data object and a list of channel types eg ["MEG", "ECG"]
    # returns True if all specified channels are present in the data object
    # otherwise returns False

    all_channel_types = [k.upper() for k in get_channel_type_constants().keys()]

    # find all channel types that exist in data
    ch_types_in_data = []
    for index, ch in enumerate(data.info["chs"]):
        kind = channel_type(data.info, index).upper()
        if kind not in ch_types_in_data:
            ch_types_in_data.append(kind)

    # if all specified channel types are present in the list:
    if all(ch_type in all_channel_types for ch_type in required_chs):
        return True
    else:
        return False
