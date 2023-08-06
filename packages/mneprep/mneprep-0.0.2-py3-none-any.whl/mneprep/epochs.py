import mne
from autoreject import get_rejection_threshold


def epoch_func(data, process_params):
    if len(data.events) != 0: # events in data
        epochs = mne.Epochs(data, events=data.events, tmin=process_params["tmin"], tmax=process_params["tmax"])
    else: # no events in data
        events = mne.make_fixed_length_events(data, duration=process_params["tstep"])
        epochs = mne.Epochs(data, events=events, tmin=0.0, tmax=process_params["tstep"], baseline=(0, 0))
    return epochs


def drop_bad_epochs_func(data, process_params):

    include = []
    picks = mne.pick_types(data.info, meg=True, eeg=True, stim=False,
                           eog=True, include=include, exclude='bads')

    if len(data.events) != 0: # events in data

        events = data.events
        # Create epochs as advised in the autoreject docs to get thresholds.
        # (Note that detrending is applied and bads are excluded)
        threshold_epochs = mne.Epochs(data, events=events, tmin=process_params["tmin"],
                                      tmax=process_params["tmax"],
                                      picks=picks, baseline=(None, 0), preload=True,
                                      reject=None, verbose=True, detrend=1)
        # create actual epochs
        epochs = mne.Epochs(data, events=data.events, tmin=process_params["tmin"], tmax=process_params["tmax"])


    else: # no events in data

        # create events
        events = mne.make_fixed_length_events(data, duration=process_params["tstep"])
        # Create epochs as advised in the autoreject docs to get thresholds.
        threshold_epochs = mne.Epochs(data, events=events, tmin=0.0,
                                      tmax=process_params["tstep"],
                                      picks=picks, baseline=(0, 0), preload=True,
                                      reject=None, verbose=True, detrend=1)
        # create actual epochs
        epochs = mne.Epochs(data, events=events, tmin=0.0, tmax=process_params["tstep"], baseline=(0, 0))

    # get rejection thresholds based on recommended epochs (bad channels excluded)
    reject = get_rejection_threshold(threshold_epochs)  # removed decim=2 as RuntimeWarning: could cause aliasing artifacts

    # apply rejection thresholds to data with bad channels included
    epochs_drop_bad = epochs.copy().drop_bad(reject=reject)

    return epochs_drop_bad


# ---- test -----------------------------------------------------

# import os
# sample_data_folder = mne.datasets.sample.data_path()
# sample_data_raw_file = os.path.join(sample_data_folder, "MEG", "sample", "sample_audvis_raw.fif")
#
# raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True, verbose=False)
# raw.events = []
# #raw.events = mne.find_events(raw, stim_channel='STI 014', verbose=False)
# #epochs = mne.Epochs(raw, raw.events, verbose=False)
# #evoked = epochs.average()
#
# def test(data):
#
#     process_params = {"tmin":None,
#                       "tmax": None,
#                       "tstep": 5.0,
#                       "autoreject": True}
#     data.stim_channel = None
#
#     if isinstance(data, mne.io.BaseRaw):
#         try:
#             if process_params["autoreject"]:
#                 epochs_drop_bad = drop_bad_epochs_func(data, process_params)
#                 epochs_drop_bad.plot()
#                 print("epochs_drop_bad")
#                 print(type(epochs_drop_bad))
#                 print(epochs_drop_bad.info["ch_names"])
#             else:
#                 epochs = epoch_func(data, process_params)
#                 epochs.plot()
#                 print("epochs")
#                 print(type(epochs))
#                 print(epochs.info["ch_names"])
#         except AttributeError as AE:
#             print("Error", "No stim channel selected")
#             return
#         except ValueError as VE:
#             print("Error: ", str(VE))
#             return
#     else:
#        print("Error: ", "Epoching can only be applied to raw data")
#
# test(raw)