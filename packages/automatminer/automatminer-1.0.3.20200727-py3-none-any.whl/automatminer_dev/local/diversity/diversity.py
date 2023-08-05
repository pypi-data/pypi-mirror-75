import os
import sys
import pandas as pd
import warnings
import numpy as np
from pymatgen import Element
from matminer.featurizers.composition import ElementProperty
from matminer.utils.data import MagpieData
import pprint
import math
from pymatgen import Composition, Structure
from matminer.featurizers.structure import SiteStatsFingerprint
from matminer.featurizers.site import OPSiteFingerprint, CrystalNNFingerprint
from scipy.special import expit
from collections import Iterable

from icecream import ic

# from automatminer import Aut

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)

base = "/Users/ardunn/alex/lbl/projects/automatminer/automatminer/automatminer_dev/testing/datasets/"
# df = pd.read_pickle(os.path.join(base, "mp_e_form.pickle.gz"))

ep_src = MagpieData()
ep_props = ep_src.all_elemental_props

epp = ep_props.keys()


def mad(data, axis=None):
    return np.mean(np.absolute(data - np.mean(data, axis)), axis)


scaler = {}
mins = {}
for prop in epp:
    is_str = [isinstance(v, str) for v in ep_props[prop].values()]
    is_iterable = [isinstance(v, (list, tuple)) for v in ep_props[prop].values()]

    if not any(is_str) and not any(is_iterable):
        non_nan_numeric = []
        for v in ep_props[prop].values():
            try:
                if not math.isnan(v):
                    non_nan_numeric.append(v)
            except TypeError:
                pass

        scaler[prop] = max(non_nan_numeric) - min(non_nan_numeric)
        mins[prop] = min(non_nan_numeric)
        # scaler[prop] = mad(non_nan_numeric, axis=0)
        # scaler[prop] = np.std(non_nan_numeric, axis=0)

valid_props = list(scaler.keys())

nonan_feats = [
    "Number",
    "MendeleevNumber",
    "AtomicWeight",
    "MeltingT",
    "Column",
    "Row",
    "CovalentRadius",
    "Electronegativity",
    "NsValence",
    "NpValence",
    "NdValence",
    "NfValence",
    "NValence",
    "NsUnfilled",
    "NpUnfilled",
    "NdUnfilled",
    "NfUnfilled",
    "NUnfilled",
    "GSvolume_pa",
    "GSbandgap",
    "GSmagmom",
]

# ep = ElementProperty(data_source=ep_src, features=nonan_feats, stats=["mean"])
# df["composition"] = compositions
# df = ep.featurize_dataframe(df, "composition")


def d_c(compositions):
    ep = ElementProperty(data_source=ep_src, features=nonan_feats, stats=["mean"])
    features = np.asarray(ep.featurize_many(compositions, ignore_errors=True))
    mask = ~np.isnan(features).any(axis=1)
    features_nonan = features[mask]
    n_samples_original = features.shape[0]
    n_samples_nonan = features_nonan.shape[0]
    percentage_nan = (n_samples_original - n_samples_nonan) / n_samples_original
    nan_thresh = 0.05
    samples_thresh = 1
    if percentage_nan > nan_thresh:
        raise ValueError(
            "Percentage of nan values is {}, which is more than the threshold ({}%).".format(
                percentage_nan, nan_thresh * 100
            )
        )
    elif n_samples_nonan < samples_thresh:
        raise ValueError(
            "Number of samples with no nan values is {}, which is less than the threshold ({}).".format(
                n_samples_nonan, samples_thresh
            )
        )
    fscales = np.asarray([scaler[f.split(" ")[-1]] for f in ep.feature_labels()])
    fmins = np.asarray([mins[f.split(" ")[-1]] for f in ep.feature_labels()])
    features_scaled = np.asarray(
        [
            np.divide(features_nonan[i, :] - fmins, fscales)
            for i in range(features_nonan.shape[0])
        ]
    )

    # return np.mean(np.std(features_scaled, axis=0))
    avg_feature = np.mean(features_scaled, axis=0)
    distances = [
        np.linalg.norm(features_scaled[i, :] - avg_feature)
        for i in range(features_scaled.shape[0])
    ]
    return np.mean(distances)

    # scaled_mean_distance = np.mean(distances)/np.sqrt(features_scaled.shape[1])
    # return scaled_mean_distance
    # return 1 - np.exp(-10.0 * scaled_mean_distance)


def d_s(structures):
    site_featurizer = CrystalNNFingerprint.from_preset("ops", cation_anion=False)
    # site_featurizer = OPSiteFingerprint()
    ssfp = SiteStatsFingerprint(
        site_featurizer=site_featurizer, stats=("mean", "std_dev")
    )
    features = np.asarray(ssfp.featurize_many(structures, ignore_errors=True))

    mask = ~np.isnan(features).any(axis=1)
    features_nonan = features[mask]
    n_samples_original = features.shape[0]
    n_samples_nonan = features_nonan.shape[0]
    percentage_nan = (n_samples_original - n_samples_nonan) / n_samples_original
    nan_thresh = 0.05
    samples_thresh = 1
    if percentage_nan > nan_thresh:
        raise ValueError(
            "Percentage of nan values is {}, which is more than the threshold ({}%).".format(
                percentage_nan, nan_thresh * 100
            )
        )
    elif n_samples_nonan < samples_thresh:
        raise ValueError(
            "Number of samples with no nan values is {}, which is less than the threshold ({}).".format(
                n_samples_nonan, samples_thresh
            )
        )

    # return np.mean(np.std(features_nonan, axis=0))

    avg_feature = np.mean(features_nonan, axis=0)
    distances = [
        np.linalg.norm(features_nonan[i, :] - avg_feature)
        for i in range(features_nonan.shape[0])
    ]
    return np.mean(distances)

    # scaled_mean_distance = np.mean(distances)/np.sqrt(features_nonan.shape[1])
    # return scaled_mean_distance
    # return 1 - np.exp(-20.0 * scaled_mean_distance)


if __name__ == "__main__":
    # site_featurizer = CrystalNNFingerprint.from_preset("ops", cation_anion=False)
    # site_featurizer = OPSiteFingerprint()
    # ssfp = SiteStatsFingerprint(site_featurizer=site_featurizer,
    #                             stats=("mean",))
    # print(ssfp.feature_labels())
    # raise ValueError

    test_df_diverse_composition = [
        Composition("AlMnO"),
        Composition("C"),
        Composition("LrMgHg"),
    ]
    test_df_diverse_structure = [
        Structure.from_file("/Users/ardunn/Downloads/" + f)
        for f in ["mp-87.cif", "mp-8085.cif", "mp-702.cif"]
    ]
    test_df_diverse = pd.DataFrame(
        {
            "composition": test_df_diverse_composition,
            "structure": test_df_diverse_structure,
        }
    )

    test_df_same_composition = [Composition("AlMn")] * 3
    test_df_same_structure = [
        Structure.from_file("/Users/ardunn/Downloads/mp-8085.cif")
    ] * 3
    test_df_same = pd.DataFrame(
        {"composition": test_df_same_composition, "structure": test_df_same_structure}
    )

    test_df_similar_structure = [
        Structure.from_file("/Users/ardunn/Downloads/" + f)
        for f in [
            "perovskite_mp-8418.cif",
            "perovskite_mp-9529.cif",
            "perovskite_mp-9440.cif",
        ]
    ]
    test_df_comp_of_similar_strcutures = [
        s.composition for s in test_df_similar_structure
    ]
    test_df_similar = pd.DataFrame(
        {
            "composition": test_df_comp_of_similar_strcutures,
            "structure": test_df_similar_structure,
        }
    )

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        np.set_printoptions(threshold=sys.maxsize)

        structure_on = True
        # dsets = ["mp_e_form", "mp_gap"]
        dsets = [
            "castelli",
            "phonons",
            "steels_yield",
            "dielectric",
            "elasticity_K_VRH",
            "expt_gap",
            "glass",
            "jdft2d",
            "mp_e_form",
            "mp_gap",
        ]
        dset_names = [d + ".pickle.gz" for d in dsets]

        for dset in dset_names:
            df = pd.read_pickle(os.path.join(base, dset))
            if df.shape[0] > 1000:
                df = df.sample(1000)

            # for dset, df in {"diverse": test_df_diverse, "same": test_df_same, "similar": test_df_similar}.items():
            if "structure" in df.columns:
                compositions = [s.composition for s in df["structure"]]
                structures = df["structure"]
            else:
                compositions = [Composition(f) for f in df["composition"]]
                structures = None

            print("d_c {}: {}".format(dset, d_c(compositions)))
            if structure_on and structures is not None:
                print("d_s {}: {}".format(dset, d_s(structures)))
