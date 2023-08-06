import mne
from PyQt5.QtWidgets import QMessageBox
from autoreject import get_rejection_threshold
from mne.preprocessing import ICA


# generation of ICA is the same process for raw and epoch
from mneGUI.check_channel_types import check_for_ch_type


def generate_ica(data, process_params, parent_window):

    print()
    print("------------------GENERATING ICA ---------------")
    print()

    # Set max_pca_components to the lesser value of its given argument or the rank
    # of the data, to avoid artifacts from incorrect data dimensionality
    n_components = process_params["n_components"]
    data_rank_dict = mne.compute_rank(data, info=data.info, verbose=False)
    data_rank = sum(data_rank_dict.values())
    max_pca_components = data_rank
    if n_components > max_pca_components:
        QMessageBox.warning(parent_window, "Updating Number of Components", "Number of components is greater than rank of data. Calculated rank (" + str(
            data_rank) + ") will be used as number of components instead")
        # print("Number of components is greater than rank of data. Calculated rank (" + str(
        #     data_rank) + ") will be used as max number of components")
        n_components = max_pca_components

    print()
    print("n components: ", n_components)
    ()

    # generate ICA
    method = process_params["ica_method"]
    fit_params = None
    if process_params["extended"]:
        fit_params = dict(extended=True)
    ica = mne.preprocessing.ICA(n_components=n_components, max_pca_components=max_pca_components, random_state=97,
                                method=method, fit_params=fit_params)
    return ica

def fit_ica_with_autoreject(ica, data):

    print()
    print("------------------FITTING ICA WITH AUTOREJECT---------------")
    print()

    if isinstance(data, mne.io.BaseRaw):
        # Autoreject only works on epoched data, so these steps are needed for raw data:
        # see autoreject docs for details: https://autoreject.github.io/faq.html
        tstep = 1.0
        events = mne.make_fixed_length_events(data, duration=tstep)
        epochs = mne.Epochs(data, events=events, tmin=0.0, tmax=tstep, baseline=(0, 0))
        reject = get_rejection_threshold(epochs)
        ica.fit(epochs, reject=reject, tstep=tstep)

    elif isinstance(data, mne.BaseEpochs):
        # drop bad channels to calculate rejection thresholds
        epochs_no_bads = data.copy().drop_channels(data.info["bads"])
        reject = get_rejection_threshold(epochs_no_bads)
        # fit ica with rejection thresholds to data with all channels
        ica.fit(data, reject=reject)

def fit_ica_no_autoreject(ica, data):

    print()
    print("------------------FITTING ICA ---------------")
    print()

    reject = None
    ica.fit(data, reject=reject)

def reject_eog_eeg_comps(ica, data):

    print()
    print("------------------ REJECTING ECG AND EOG COMPONENTS ---------------")
    print()

    # Select and remove components that match the EOG and ECG channels (ie blink and ECG artifact removal)
    ica.exclude = []
    eog_indices, eog_scores = ica.find_bads_eog(data)  # find which ICs match the EOG pattern
    ecg_indices, ecg_scores = ica.find_bads_ecg(data, method='correlation')

    ica.exclude += eog_indices
    ica.exclude += ecg_indices

    print("ica.exclude= ", ica.exclude)

def reject_comps_manual(ica, data):

    print()
    print("------------------ REJECTING COMPONENTS MANUALLY ---------------")
    print()

    print(ica.exclude)
    ica.plot_sources(data, block=True)  # plot time series of components - click on components to select them for exclusion at this point
    print(ica.exclude)

def apply_ica(ica, data):

    print()
    print("------------------ APPLYING ICA ---------------")
    print()

    reconst_data = data.copy()
    ica.apply(reconst_data)
    return reconst_data


# ---- test ------------------------------------------------------------------
#
# from PyQt5.QtWidgets import QMessageBox, QWidget, QApplication
# import sys
# app = QApplication(sys.argv)
# window = QWidget()
#
# import os
# sample_data_folder = mne.datasets.sample.data_path()
# sample_data_raw_file = os.path.join(sample_data_folder, "MEG", "sample", "sample_audvis_raw.fif")
#
# raw = mne.io.read_raw_fif(sample_data_raw_file, preload=True, verbose=False)
# # events = mne.find_events(raw, stim_channel='STI 014', verbose=False)
# # epochs = mne.Epochs(raw, events, verbose=False)
# data = raw
#
#
#
# process_params = {"n_components": 0.50,
#                   "ica_method": "fastica",
#                   "extended": False,
#                   #"ortho": self.ortho.isChecked(),
#                   "autoreject": False,
#                   #"rejection_method": "ecg_eog"}
#                   "rejection_method": "manual"}
#
#
# # only give the function for raw and epochs
# if isinstance(data, mne.io.BaseRaw) or isinstance(data, mne.BaseEpochs):
#
#     # 2) generate ICA
#     ica = generate_ica(data, process_params, window)
#
#     # 3) fit ICA (load data needed if epochs & dropping channels in autoreject)
#     #data.load_data()
#     if process_params["autoreject"]:
#         fit_ica_with_autoreject(ica, data)
#     else:
#         fit_ica_no_autoreject(ica, data)
#
#     # 4) Exclude components
#     if process_params["rejection_method"] == "manual":
#         reject_comps_manual(ica, data)
#
#     else: # if process_params["rejection_method"] == "ecg_eog"
#         # check that data actually has EOG and ECG/MEG channels
#         if check_for_ch_type(data, ["ECG", "EOG"]) \
#                 or check_for_ch_type(data, ["MAG", "EOG"]) \
#                 or check_for_ch_type(data, ["GRAD", "EOG"]):
#             reject_eog_eeg_comps(ica, data)
#         else:
#             print("Error: ", "EOG and/or ECG channels not found. Defaulting to manual rejection")
#             reject_comps_manual(ica, data)
#
#     # 5) Apply ICA
#     reconst_data = apply_ica(ica, data)
#
#     # 6) Plot data to check it
#
#     #raw - with and without ICA
#     ica.plot_sources(data)
#     ica.plot_overlay(data, exclude=ica.exclude, picks="eeg")
#     ica.plot_overlay(data, exclude=ica.exclude, picks="mag")

#     #epochs
#     # ica.plot_sources(data.average())
#     # ica.plot_overlay(data.average(), exclude=ica.exclude)
#
#
#
# #window.show()
# sys.exit(app.exec_())