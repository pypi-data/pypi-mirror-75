import mne


def get_preset_pipeline(pipeline_name, data):

    # Need to get bads before running the pipeline
    example_pipeline = [    ["filter", {"l_freq": 1, "h_freq": 40, "method": "fir"}],
                            ["resample", {"sfreq": 500}],
                            ["line_noise", {"freqs": (50, 100), "method": "iir"}],
                            ["channels", {"bads": [], "interpolate": True}],
                            ["ICA", {"n_components": 20,
                                     "ica_method": "fastica",
                                     "extended": False,
                                     "autoreject": True,
                                     "rejection_method": "manual"}],
                            ["epoch", {"tmin": -0.2, "tmax": 0.5, "autoreject": True}],
                            ["baseline", {"interval": (-0.2, 0)}],
                            ["", {}],
                            ["", {}],
                            ["", {}]
                        ]

    # Need to get bads before running the pipeline
    gramfort_pipeline = [   ["", {}], # Spare one at the start for optional step eg resampling to be applied before pipeline is run
                            ["filter", {"l_freq": 1, "h_freq": 40, "method": "fir"}],
                            ["channels", {"bads": [], "interpolate": True}],
                            ["ICA", {"n_components": 0.99,
                                      "ica_method": "fastica",
                                      "extended": False,
                                      "autoreject": True,
                                      "rejection_method": "manual"}],
                            ["epoch", {"tmin": -0.2, "tmax": 0.5, "tstep": None, "autoreject": True}],
                            ["baseline", {"interval": (-0.2, 0)}],
                            ["", {}],
                            ["", {}],
                            ["", {}],
                            ["", {}]
                        ]

    if pipeline_name == "example":
        return example_pipeline
    elif pipeline_name == "gramfort":
        return gramfort_pipeline

    # following pipelines require rank to be calculated
    #rank_dict = mne.compute_rank(data, info=data.info, verbose=False)
    #rank = sum(rank_dict.values())

    # alternatively, just use number of channels - quicker to calculate, and chances are by the time some processing has been done
    # the rank will have reduced from what it was for the original raw data so it will have to be redone anyway
    picks = mne.pick_types(data.info, meg=True, eeg=True, eog=False, ecg=False)
    # print(len(picks))
    num_chs = len(picks)

    # Need to get bads and rank/num of chs before running the pipeline
    makoto_pipeline = [["filter", {"l_freq": 1, "h_freq": None, "method": "fir"}],
                       ["resample", {"sfreq": 250}],
                       ["channels", {"bads": [], "interpolate": True}],
                       ["set_reference", {"ref_channels": "average"}],
                       ["line_noise", {"freqs": (50), "method": "fir"}],
                       ["epoch", {"tmin": -0.2, "tmax": 0.5, "tstep": None, "autoreject": True}],
                       ["ICA", {"n_components": num_chs,
                                "ica_method": "infomax",
                                "extended": False,
                                "autoreject": False,
                                "rejection_method": "manual"}],
                       ["", {}],
                       ["", {}],
                       ["", {}]
                       ]

    # Need to get bads and rank/num of chs before running the pipeline
    luck_pipeline = [["", {}],  # blank for optional resampling
                     ["filter", {"l_freq": 0.1, "h_freq": None, "method": "fir"}],
                     ["line_noise", {"freqs": (50), "method": "fir"}],
                     ["channels", {"bads": [], "interpolate": True}],
                     ["ICA", {"n_components": num_chs,
                              "ica_method": "fastica",
                              "extended": False,
                              "autoreject": False,
                              "rejection_method": "manual"}],
                     ["set_reference", {"ref_channels": "average"}],
                     ["epoch", {"tmin": -0.2, "tmax": 0.5, "tstep": None, "autoreject": True}],
                     ["baseline", {"interval": (-0.2, 0)}],
                     ["", {}],
                     ["", {}]
                     ]

    # Need to get bads and rank/num of chs before running the pipeline
    resting_state_pipeline = [["filter", {"l_freq": 1, "h_freq": 100, "method": "iir"}],
                              ["line_noise", {"freqs": (50, 100), "method": "iir"}],  # check method
                              ["ICA", {"n_components": num_chs,
                                       "ica_method": "fastica",
                                       "extended": False,
                                       "autoreject": False,
                                       "rejection_method": "manual"}],
                              ["resample", {"sfreq": 256}],
                              ["epoch", {"tmin": None, "tmax": None, "tstep": 30, "autoreject": True}],
                              # ["baseline", {"interval": (-0.2, 0)}],
                              ["", {}],
                              ["", {}],
                              ["", {}],
                              ["", {}],
                              ["", {}]
                              ]

    if pipeline_name == "makoto":
        return makoto_pipeline
    elif pipeline_name == "luck":
        return luck_pipeline
    elif pipeline_name == "resting":
        return resting_state_pipeline