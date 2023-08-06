import pandas as pd


def denuder(compiled, acquisition, results):
    import numpy as np

    np.seterr(divide="ignore", invalid="ignore")
    compiled = compiled.set_index("Topic ID")
    acquisition = pd.concat(acquisition, sort=False).set_index("Topic ID").sort_index()
    re = pd.concat(results, sort=False).set_index("Topic ID").sort_index()
    acquisition = acquisition.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    data_groups = acquisition.groupby("Ratio W/Wo - Topic comparison")
    cframes = []
    for id, frames in data_groups:
        if data_groups.groups.get(id).size == 2:
            index = frames.index
            denuder = re.loc[index][
                ~acquisition.loc[index]["Denuder type"].isin(["no"])
            ]
            not_denuder = re.loc[index][
                acquisition.loc[index]["Denuder type"].isin(["no"])
            ]
            calculated_frame = pd.DataFrame(
                columns=re.columns, data=denuder.values / not_denuder.values
            ).add_suffix(" Ratio Denuder/No Denuder")
            topics = "-".join(
                list(map(lambda x: str(x), [denuder.index[0], not_denuder.index[0]]))
            )
            calculated_frame["Ratio for Denuder Topic IDs"] = topics
            cframes.append(calculated_frame)
    cc = pd.concat(cframes)
    cc = cc.reset_index()
    cc = cc.drop(columns=["index"])
    for ind, frame in cc.iterrows():
        working_frame = pd.DataFrame(cc.iloc[ind]).transpose()
        topic_list = frame["Ratio for Denuder Topic IDs"].split("-")
        for id in topic_list:
            id = int(id)
            for key, value in working_frame.iteritems():
                compiled.loc[id, key] = value.values[0]
    compiled.reset_index(inplace=True)
    return compiled


def cross_topic(compiled, acquisition, results):
    compiled.loc[:, compiled.columns != "formulation id"] = compiled.applymap(
        lambda x: x.casefold() if isinstance(x, str) else x
    )
    results = pd.concat(results, sort=False).set_index("Topic ID").sort_index()
    results = results.applymap(lambda x: x.casefold() if isinstance(x, str) else x)
    acquisition = pd.concat(acquisition, sort=False).set_index("Topic ID").sort_index()
    acquisition = acquisition.applymap(
        lambda x: x.casefold() if isinstance(x, str) else x
    )
    acquisition["Aerosol Genrator"] = acquisition["Aerosol Genrator"].str.replace(
        r"\bnebulyzer\b", "nebulizer"
    )
    acquisition_duplicates = acquisition[
        acquisition.duplicated(
            subset=[
                "Flow (L/min)",
                "Aerosol Genrator",
                "Volume trapped (L)",
                "Denuder type",
            ],
            keep=False,
        )
    ]
    compiled = compiled.set_index("Topic ID")
    compiled_acq_duplicates = compiled.loc[acquisition_duplicates.index]
    compiled_acq_form_duplicates = (
        compiled_acq_duplicates.groupby(["Denuder type", "formulation id"])
        .filter(lambda x: x.shape[0] >= 2)
        .groupby(["Denuder type", "formulation id"])
    )

    stats = compiled_acq_form_duplicates[results.columns].aggregate(
        ["sem", "count", "mean", "var", "std", confidenceInterval]
    )

    rename_dictionary = {b: b.split(" ")[0] for b in stats.columns.levels[0]}
    stats = stats.rename(columns=rename_dictionary, level=0)
    single_index = [" ".join(col).strip() for col in stats.columns.values]
    stats.columns = single_index
    stats = stats.reset_index()
    return stats


# returns confidence interval of mean
def confidenceInterval(series, conf=0.95):
    import scipy.stats as st
    from numpy import nan

    mean = series.mean()
    sem = series.sem()
    t = st.t.ppf((1 + conf) / 2.0, series.size - 1)
    interval = t * sem
    plus = mean + interval if (mean + interval) > 0 else 0
    minus = mean - interval if (mean - interval) > 0 else 0
    return [plus, minus]
