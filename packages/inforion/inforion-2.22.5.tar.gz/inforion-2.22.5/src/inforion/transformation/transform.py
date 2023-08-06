# Transformation of Staging Data into M3 format via mapping file
import datetime
import decimal
import logging
from functools import partial
from multiprocessing import Pool

import numpy as np
import pandas as pd

# from logger import get_logger


def parallelize_tranformation(
    mappingfile, mainsheet, stagingdata, outputfile=None, n_cores=4
):
    # Read the file from given location
    xls = pd.ExcelFile(mappingfile)

    # to read all sheets to a map
    sheet_to_df_map = {}
    for sheet_name in xls.sheet_names:
        sheet_to_df_map[sheet_name] = xls.parse(sheet_name)

    main_cache = getMainSheetCache(sheet_to_df_map, mainsheet)
    tabs_cache = getTabsMappingCache(sheet_to_df_map, main_cache)

    df_split = np.array_split(stagingdata, n_cores)
    func = partial(transform_data, sheet_to_df_map, mainsheet, main_cache, tabs_cache)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()

    if outputfile is not None:
        logging.info("Save to file: " + outputfile)
        writer = pd.ExcelWriter(outputfile, engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Log Output", index=False)
        writer.save()

    return df


def getMainSheetCache(sheet_to_df_map, mainsheet):
    mapping_cache = []

    for index, row in sheet_to_df_map[mainsheet].iterrows():
        if index >= 9:
            row = row.replace(np.nan, "", regex=True)

            map = {}
            map["API_FIELD"] = row[15]

            if row[33] and not row[33] is np.nan:
                map["SOURCE"] = row[33]
            else:
                map["SOURCE"] = None

            map["FUNC_TYPE"] = row[36].strip().lower()

            map["FUNC_VAL"] = row[37]
            map["FUNC_ARG"] = row[38]

            mapping_cache.append(map)

    return mapping_cache


def getTabsMappingCache(sheet_to_df_map, mapping_cache):
    mapping_sheets_cache = {}

    for map in mapping_cache:
        if map["FUNC_TYPE"] == "tbl":
            index_key = 1
            key_cols_count = 0
            index = 0
            tab_key = map["FUNC_VAL"].strip()
            tab_sub_keys = map["FUNC_ARG"].split("|")

            tab = {}
            tab[str(map["API_FIELD"])] = {}
            for sub_val in tab_sub_keys:
                if "#:" in sub_val:
                    index_key = int(sub_val[2:])
                else:
                    key_cols_count = key_cols_count + 1

            index_key = key_cols_count + index_key - 1
            for i, val in sheet_to_df_map[tab_key].iterrows():
                multi_val = ""
                if i >= 7:
                    if str(val[0]) == "nan":
                        val[0] = ""
                    if key_cols_count > 1:
                        for sub_val in tab_sub_keys:
                            if "#:" not in sub_val:
                                if multi_val == "":
                                    multi_val = str(val[index])
                                else:
                                    multi_val = multi_val + "_" + str(val[index])
                                index + 1
                        tab[str(map["API_FIELD"])][multi_val] = str(val[index_key])
                    else:
                        tab[str(map["API_FIELD"])][str(val[0])] = str(
                            val[int(index_key)]
                        )

            if tab_key not in mapping_sheets_cache:
                mapping_sheets_cache[tab_key] = tab
            else:
                mapping_sheets_cache[tab_key].update(tab)

    return mapping_sheets_cache


def transform_data(_sheet_to_df_map, _mainsheet, sheet_cache, tabs_cache, stagingdata):
    rows_list = []

    for _, tb_row in stagingdata.iterrows():
        row_dict = {}

        for map in sheet_cache:

            if map["SOURCE"]:
                source = clean(map["SOURCE"])
                if not source in tb_row:
                    raise TransformationError(
                        "Field '{}' mentioned in mapping sheet is not found.".format(
                            source
                        )
                    )
                row_dict[map["API_FIELD"]] = str(tb_row[source])
            else:
                if map["FUNC_TYPE"] == "tbl":
                    if map["FUNC_ARG"] and not map["FUNC_ARG"] is np.nan:
                        db_val = ""
                        tab = tabs_cache[map["FUNC_VAL"]]
                        sub_keys = map["FUNC_ARG"].split("|")
                        for sub_val in sub_keys:
                            if "#:" not in sub_val:
                                sub_val = clean(sub_val)

                                if not sub_val in tb_row:
                                    raise TransformationError(
                                        "Field '{}' mentioned in mapping sheet is not found.".format(
                                            sub_val
                                        )
                                    )

                                if db_val == "":
                                    db_val = str(tb_row[sub_val])
                                else:
                                    db_val = db_val + "_" + str(tb_row[sub_val])
                        if db_val in tab[map["API_FIELD"]]:
                            row_dict[map["API_FIELD"]] = str(
                                tab[map["API_FIELD"]][db_val]
                            )
                        elif "*" in tab[map["API_FIELD"]]:
                            row_dict[map["API_FIELD"]] = str(tab[map["API_FIELD"]]["*"])
                        else:
                            row_dict[map["API_FIELD"]] = str(db_val)
                elif map["FUNC_TYPE"] == "func":
                    if map["FUNC_VAL"].strip().lower() == "div":
                        data_values = map["FUNC_ARG"].split("|")
                        with decimal.localcontext() as ctx:
                            if data_values[2] != "":
                                ctx.prec = int(data_values[2])
                            division = decimal.Decimal(
                                tb_row[data_values[0]]
                            ) / decimal.Decimal(data_values[1])
                    row_dict[map["API_FIELD"]] = division
                elif map["FUNC_TYPE"] == "const":
                    if isinstance(map["FUNC_VAL"], datetime.datetime):
                        val = map["FUNC_VAL"].strftime("%Y%m%d")
                        row_dict[map["API_FIELD"]] = str(val)
                    else:
                        row_dict[map["API_FIELD"]] = str(map["FUNC_VAL"])

        rows_list.append(row_dict)

    df = pd.DataFrame(rows_list).replace("nan", "", regex=True)

    return df


def clean(string):
    str = string
    if str.startswith("["):
        str = str[1:]

    if str.endswith("]"):
        str = str[:-1]
    return str


class TransformationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
