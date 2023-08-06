from collections import defaultdict
from crdatamgt.helpers import workbook_load_path, data_extraction
import pandas as pd


def load_topic(path):
    print(path)
    wb = workbook_load_path(path)
    return wb


def read_topic(wb):
    df_dictionary = defaultdict()
    for sheet in wb.sheetnames:
        if sheet == "Formulations":
            name_sheet = "Formulation"
        else:
            name_sheet = sheet
        df_dictionary[name_sheet] = data_extraction(wb, sheet)
    if "Results" in df_dictionary.keys():
        column_names = df_dictionary["Results"].columns.values
        if "Replicate" in column_names or "Replicate #" in column_names:
            df_dictionary["Results"].rename(
                columns={"Replicate #": "Replicate"}, inplace=True
            )
            df_dictionary["Results"] = (
                pd.DataFrame(
                    df_dictionary["Results"].set_index("Replicate").mean().round(2)
                )
                .transpose()
                .add_suffix(" Average")
            )

    return df_dictionary
