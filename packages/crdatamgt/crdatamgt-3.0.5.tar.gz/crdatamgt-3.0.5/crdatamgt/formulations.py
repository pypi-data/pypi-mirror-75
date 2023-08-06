import os

import pandas as pd
import simplelogging
from toolz import interleave
from xlsxwriter.exceptions import FileCreateError

from crdatamgt.helpers import (
    data_extraction,
    workbook_load_path,
    rename_dictionary,
    log_format,
)

formulation_log = simplelogging.get_logger(
    file_name="formulation.log", console=False, file_format=log_format("simple")
)


def formulation_read(wb, header=False):
    p_header, p_formulation = data_extraction(wb, "Formulations", header)
    p_formulation.columns = map(str.lower, p_formulation.columns)
    formulation_id = p_formulation.get("formulation id")
    p_formulation.rename(columns=rename_dictionary(), inplace=True)
    p_formulation = p_formulation.drop(columns="formulation id", errors="ignore").apply(
        pd.to_numeric, errors="coerce"
    )
    p_formulation["formulation id"] = formulation_id

    return [p_formulation, [p_header, p_formulation]][header]


def tests_read(wb, header=False):
    p_header, p_tests_data = data_extraction(wb, "Tests", header)
    p_tests_data.columns = map(str.lower, p_tests_data.columns)
    return [p_tests_data, [p_header, p_tests_data]][header]


def formulation_load(path, write=False):
    wb = workbook_load_path(path, write)
    formulas = formulation_read(wb)
    return formulas


def update_formulation_table(new_data, formulation_path):
    """
    This entire bit of code will become difficult to maintain. The entire concept of formulation flexibility should be
    revisited

    :param formulation_path: Excel data to load
    :param new_data: New data from project
    :return: All formulas for all topics multi-dimensional
    """
    if new_data.dropna(how="all").empty:
        return pd.DataFrame()
    new_data = force_numeric_append_objects(new_data, ["test"])

    data_path = os.path.join(formulation_path, "Formulation table.xlsx")
    writer = pd.ExcelWriter(data_path, engine="openpyxl")
    writer.book = workbook_load_path(formulation_path, True)
    formulation_wb = writer.book

    sheet_formulation = "Formulations"
    sheet_tests = "Tests"

    formulation_header, old_formula_data = formulation_read(formulation_wb, True)
    test_header, old_tests = tests_read(formulation_wb, True)

    formulations_data = hash_formulation(new_data)

    updated_data = formulations_data.merge(old_formula_data, how="outer").dropna(
        how="all"
    )

    updated_formulations = updated_data.drop(columns="test", errors="ignore")
    updated_formulations.mask(updated_formulations.eq("None")).dropna(how="all")
    updated_formulations = updated_formulations.drop_duplicates()
    updated_formulations = updated_formulations.dropna(how="all")

    updated_tests = old_tests.merge(
        updated_data.get(["test", "formulation id"]), how="outer"
    )

    updated_tests = test_setup(updated_tests)
    updated_tests.reset_index(inplace=True)
    replace_sheet(
        formulation_wb,
        sheet_formulation,
        writer,
        formulation_header,
        updated_formulations.set_index("formulation id"),
    )
    replace_sheet(
        formulation_wb,
        sheet_tests,
        writer,
        test_header,
        updated_tests.set_index("formulation id"),
    )

    try:
        writer.save()
    except PermissionError or FileCreateError:
        print("Formulation File is open")
        pass
    try:
        writer.close()
    except PermissionError or FileCreateError:
        pass


def test_setup(updated_tests):
    test_group = updated_tests.groupby("test")
    sentient = test_group.apply(lambda x: grfun(x))
    updated_tests = updated_tests.merge(sentient, how="outer")
    updated_tests = updated_tests.drop(columns="test", errors="ignore")
    updated_tests = updated_tests.mask(updated_tests.eq("None")).dropna(how="all")
    updated_tests = updated_tests.groupby("formulation id").count()
    updated_tests = updated_tests.mask(updated_tests.ne(0), "x").mask(
        updated_tests.eq(0, "")
    )
    return updated_tests


def hash_formulation(formulation_frame, col=None, new_col=None, major_only=False):
    if col is None:
        col = ["test"]
    if new_col is None:
        new_col = "formulation id"

    def ex(fr, major_only):
        if fr.sum() > 100:
            return "WARNING FORMULATION ABOVE 100%"
        totals = fr[0 < fr]
        major = totals[totals > 10]
        minor = totals[fr < 10]

        if major_only:
            from numpy import round as rnd

            major = major.apply(lambda x: rnd(x, -1))
        major_names = [m[:2].upper() for m in major.index if m]
        minor_names = [m[:2].lower() for m in minor.index if m]

        major_formula = [
            f"{name}{int(value)}" for name, value in zip(major_names, major.values)
        ]
        minor_formula = [
            f"{name}{value}" for name, value in zip(minor_names, minor.values)
        ]
        minor_names_without_acid_or_nicotine = [
            f"{m.split(' ')[0]} {value}%"
            for m, value in zip(minor.index, minor.values)
            if (m and m != "nicotine")
        ]
        if major_only:
            formula = "".join(major_formula)
            if minor_names_without_acid_or_nicotine:
                formula += "-" + "-".join(
                    [not_acid for not_acid in minor_names_without_acid_or_nicotine]
                )

        else:
            formula = "".join(major_formula + minor_formula)
        return formula or ""

    formulation_frame = formulation_frame.dropna(how="all")
    formulation_frame[new_col] = formulation_frame.drop(
        columns=col, errors="ignore"
    ).apply(lambda x: ex(x, major_only), axis=1)
    formulation_frame = formulation_frame[formulation_frame[new_col] != ""]

    return formulation_frame


def force_numeric_append_objects(new_data, frames_to_append):
    new_data.columns = map(str.lower, new_data.columns)
    new_data.rename(columns=rename_dictionary(), inplace=True)
    forced_numeric = (
        pd.DataFrame(new_data.drop(columns=frames_to_append, errors="ignore"))
        .astype(float)
        .fillna(0.0)
    )
    new_data = pd.concat([forced_numeric, new_data.get(frames_to_append)], axis=1)
    return new_data


def formulations_for_log_file(updated_data):
    if updated_data.dropna(how="all").empty:
        return pd.DataFrame()

    updated_data.columns = map(str.lower, updated_data.columns)
    updated_data.rename(columns=rename_dictionary(), inplace=True)
    data = updated_data.drop(columns=["test", "units", "formulation"], errors="ignore")
    data = data.dropna(how="all", subset=data.columns.difference(["topic id"]))
    data = hash_formulation(
        data, col=["topic id"], new_col="formulation group", major_only=True
    )
    data = hash_formulation(data, col=["topic id", "formulation group"])

    data_no_ID = data.drop(
        columns=["formulation id", "formulation group"], errors="ignore"
    )

    max_formulation = (
        data_no_ID.groupby(["topic id"])
        .max()
        .rename(columns={x: f"{x} Max" for x in data_no_ID.columns})
    )
    min_formulation = (
        data_no_ID.groupby(["topic id"])
        .min()
        .rename(columns={x: f"{x} Min" for x in data_no_ID.columns})
    )
    formulation_min_max = pd.concat([max_formulation, min_formulation], axis=1)[
        list(interleave([max_formulation, min_formulation]))
    ]

    topic_frames = data.groupby("topic id")
    for id, topic in topic_frames:
        list_id = [d for d in topic.get("formulation id") if d]
        string_id = ";".join([str(y) for y in list_id])

        list_formula_group = list(set(d for d in topic.get("formulation group") if d))
        if len(list_formula_group) == 1:
            string_formula_group = ";".join([str(y) for y in list_formula_group])
            formulation_min_max.loc[id, "formulation group"] = string_formula_group
        else:
            formulation_min_max.loc[
                id, "formulation group"
            ] = "Multiple Formulations Groups"

        formulation_min_max.loc[id, "formulation id"] = string_id

    formulation_return = formulation_min_max.reset_index().rename(
        columns={"topic id": "Topic ID"}
    )
    return formulation_return


def check_bad_data(data):
    topics = data.groupby("topic")
    for k, v in topics.items():
        if (
            not v.drop(columns=["test", "topic id"], errors="ignore")
            .dropna(how="all")
            .empty
        ):
            if (
                v.drop(columns=["formulation", "test", "topic id"], errors="ignore")
                .dropna(how="all")
                .empty
            ):
                formulation_log.info(
                    f"Formulation information is missing in Topic ID:  <<{v.index.values}>>"
                )


def grfun(gr):
    if not gr.empty:
        x = list(set(gr["test"].values))
        gr.loc[gr["test"] != None, x[0].lower()] = "x"
        return gr


def replace_sheet(wb, sheet, writer, header, data):
    idx = wb.sheetnames.index(sheet)
    wb.remove(wb.worksheets[idx])
    header.to_excel(writer, sheet, index=False, header=False)
    data.drop(
        columns=["test", "formulation", "units", "topic id"], errors="ignore"
    ).to_excel(writer, sheet, startrow=header.shape[0], startcol=0, index=True)
