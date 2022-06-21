"""

TIMES-MEDEA INTERFACE-FILE:
    This file is a structured file. It provides all the information
    to translate TIMES results to an pyam DataFrame.

"""
import warnings

import pandas as pd
import numpy as np

import pyam
import netzero2040.AEA_Sandbox.Dev_Snipplets.file_handle as fh

# ############### SET UP ####################
# manipulate pandas print for better vision
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

# set the parameter(symbol) names for the process
# this script was designed to perform the tasks only for the given parameter
# ["F_IN", "F_OUT", "PAR_PASTI", "PAR_CAPL"]
translation_symbols = ["F_IN", "F_OUT", "PAR_PASTI", "PAR_CAPL"]
path_to_gdx = "AEA_Sandbox/OeM_Env/results/run_2010_2020.gdx"
path_to_times_medea_interface_setup = r"G:\_2021\21.035_NetZero2040\05_Modellierung\04_Model coupling-concepts\Interface_times_medea.csv"
setup_model = "TEST_OEM"
setup_scenario = "TEST_DEV_SCEN"
setup_yearfilter = 2020


# for development reasons set the to False
setup_reload_files = True
# #############################################

def load_file(path=path_to_gdx):
    """
    retrun the gdx from a given path
    :param path:
    :return:
    """
    return fh.load_gdx_from_path(path=path)


def prepare_dataframe_for_export(symbols: list,
                                 gdx,
                                 year_filter: int=setup_yearfilter,
                                 reload: bool=setup_reload_files):

    path_to_dev_pickle = "raw_symbol_df.p"
    reload = reload
    if reload == False:
        warnings.warn("Loading Symbols DF from pickle in prepare_dataframe_for_export")
        df = pd.read_pickle(path_to_dev_pickle)
        return df

    dfs = pd.DataFrame()

    generate_filter_year = {
        "F_IN": "T",
        "F_OUT": "T",
        "PAR_CAPL": "YEAR",
        "PAR_PASTI": "T",
    }

    for symbol in symbols:
        df = make_df_of_symbol(gdx, symbol)
        df["symbol"] = symbol
        df["filter_year"] = df[generate_filter_year[symbol]].copy()
        df["filter_year"] = pd.to_numeric(df["filter_year"])
        dfs = dfs.append(df)

    dfs = dfs[dfs["filter_year"]==year_filter]
    dfs.to_pickle(path_to_dev_pickle)
    return dfs

def _get_specific_columns_and_symbol_types(symbol:str):
    """
    returns the symbol_type specific column names.
    the column names are later used within the group-by function to aggregate the two different types with one function.
    The Capacities of PAR_CAPL (PAR_PASTI) do not have a commodity (C) therefore this dimension has to be excluded during
    aggregation.
    :param symbol: "F_IN" or "PAR_CAPL"
    :return: columns, symbol_type
    """
    # Fixme: test if we really need the symbol_type (may be obsolete)
    columns_finouts = ["R", "filter_year", "P", "C", "variable", "unit", "symbol_type"]
    columns_capas = ["R", "filter_year", "P", "variable", "unit", "symbol_type"]

    if symbol == "F_IN":
        columns = columns_finouts
        symbol_type = "FLOW"

    elif symbol == "PAR_CAPL":
        columns = columns_capas
        symbol_type = "CAPA"

    return columns, symbol_type


def _filter_gdx_dataFrame(gdx_df,
                          symbol:str,
                          process:str,
                          commodity:str):
    """
    performs 2-3 filter on given gdx dataFrame based on symbol, process and (commodity)

        prepare filter based on TIMES MEDEA Interface
        F_IN and F_OUT, and "PAR_CAPL" and "PAR_PASTI" will be aggregated later
        installed capacities do not have a c parameter -> filter has to be conditional

        ! ALSO Fixes problems with regex -> if there are no wildcards: filter should not be treated as regex
    :param gdx_df: gdx_df
    :param symbol: F_IN or PAR_CAPL
    :param process: TIMES - acronym for "PROCESS" (P)   may include wildcards
    :param commodity: TIMES - acronym for "COMMODITY" (C)   may include wildcards
    :return: filtered gdx_dataFrame
    """

    if symbol == "F_IN":
        symbol_filter = gdx_df["symbol"].isin(("F_IN", "F_OUT"))

    elif symbol == "PAR_CAPL":
        symbol_filter = gdx_df["symbol"].isin(("PAR_CAPL", "PAR_PASTI"))
    else:
        msg = f"unknown symbol: {symbol}"
        raise ValueError(msg)


    process = process.replace("??", "..")

    process_filter = gdx_df["P"].str.contains(process)
    combined_filter = np.logical_and(process_filter, symbol_filter)

    # installed capacities do not have a c parameter -> filter has to be conditional
    if not (pd.isna(commodity)):
        commodity_has_wildcards = ("?" in commodity or "*" in commodity)
        if commodity_has_wildcards:
            # todo check functionality
            commodity = commodity.replace("??", "..")
            commodity_filter = gdx_df["C"].str.contains(commodity)
        else:
            commodity_filter = gdx_df["C"] == commodity

        combined_filter = np.logical_and(combined_filter, commodity_filter)

    gdx_df_filtered = gdx_df[combined_filter].copy()
    return gdx_df_filtered


def clean_the_export_collector(dirty_export_collector):

    clean_export_collector = dirty_export_collector.copy()

    clean_export_collector.drop(['P', 'C', "symbol_type"], axis=1, inplace=True)
    clean_export_collector = clean_export_collector.groupby(["R", "filter_year", "variable", "unit", "model", "scenario"], as_index=False).sum()

    # rename columns
    pyam_column_names = {
        "R": "region",              # Region of the value (AUT)
        "variable": "variable",     # variable name (divided by the | operator)
        "P": "process",             # (x) process (Times)
        "C": "commodity",           # (x) commodity (Times)
        "unit": "unit",             # unit of the value (e.g. TJ, kunits)
        "filter_year": "year",      # reference year (do not confuse with the vintageing)
        "model": "model",           # model name (OEM)
        "scenario": "scenario",     # scenario name probably todo: Do we need a distinction between different runs of a single scenario
        "value": "value"            # the value itself
    }

    clean_export_collector.columns = [pyam_column_names[col] for col in clean_export_collector.columns]
    return clean_export_collector

def prepare_files_for_standard_export(gdx,
                                      symbols:list,
                                      model:str=setup_model,
                                      scenario:str=setup_scenario,
                                      year_filter:int=setup_yearfilter):
    """
    1. prepare DF
    2. load TIMES MEDEA Interface-File
    3. iterate over TIMES MEDEA Interface
        3.1 collect translation variables
        3.2 perform symbol_type specific manipulations
        3.3 generate symbol_type specific column header (needed for aggregation (group by) 
        3.4 filtering -> selecting the right process, commodity symbol combinations
                (Capacities do not have a commodity value)
        
    
    :param gdx: 
    :param symbols: 
    :return: 
    """""
    gdx_df = prepare_dataframe_for_export(gdx=gdx,
                                          symbols=symbols,
                                          year_filter=year_filter)

    interface_meta = load_TIMES_MEDEA_INTERFACE_file()

    # initialize empty collector
    raw_export_collector = pd.DataFrame()

    for _, row in interface_meta.iterrows():
        # collect data from TIMES - MEDEA Interface File

        symbol = row["GDX.ATTRIBUTE"]
        process = row["GDX.PRC"]
        commodity = row["GDX.COM"]
        variable_name = row["PYAM.Variable"]
        unit = row["PYAM.UNIT"]

        if symbol not in ("F_IN", "PAR_CAPL"):
            """
            Everything but F_IN and PAR_CAPL lead to any error. We do this in oder to avoid double counting.
            There is a reason behind this!
            """
            msg = f"unknown symbols {symbol}"
            raise KeyError(msg)

        #  columns and symbol type are necessary for this process
        gdx_df_filtered = _filter_gdx_dataFrame(gdx_df=gdx_df,
                                                symbol=symbol,
                                                process=process,
                                                commodity=commodity)

        columns, symbol_type = _get_specific_columns_and_symbol_types(symbol=symbol)

        gdx_df_filtered["symbol_type"] = symbol_type
        gdx_df_filtered["unit"] = unit
        gdx_df_filtered["variable"] = variable_name

        # calculate mean of timescales and generate a new df

        aggregated_and_filtered_gdx_df = gdx_df_filtered.groupby(columns, as_index=False).sum()

        aggregated_and_filtered_gdx_df["model"] = model
        aggregated_and_filtered_gdx_df["scenario"] = scenario

        raw_export_collector = raw_export_collector.append(aggregated_and_filtered_gdx_df)


    clean_export_collector = clean_the_export_collector(raw_export_collector)

    # load prepared data into pyam format
    glorious_pyam_df = pyam.IamDataFrame(clean_export_collector)

    # save output
    # todo make function that saves the files according to a scheme
    # times_medea_exchange_<SCENARIO>_<YEAR>_<TRY>.csv
    # times_medea_exchange_<SCENARIO>_<YEAR>_<TRY>.p  <- pickle it is
    import os
    os.makedirs("Archive", exist_ok=True)
    os.makedirs("Exchange", exist_ok=True)

    raw_export_collector.to_csv(f"Archive//times_medea_exchange_{scenario}_{year_filter}_raw_input.csv", sep=";", decimal=",")
    clean_export_collector.to_csv(f"Archive//times_medea_exchange_{scenario}_{year_filter}_clean_input.csv", sep=";", decimal=",")
    glorious_pyam_df.to_csv(f"Exchange//times_medea_exchange_{scenario}_{year_filter}_pyam.csv", sep=";", decimal=",")


def make_df_of_symbol(gdx, symbol_name: str):
    print("making data frame for:", symbol_name)
    gdx_sym = gdx.get_symbol(symbol_name)
    columns = gdx_sym.get_domains_as_strings()
    output_dict = {"value": []}
    columns_table = []

    for nr, column_name in enumerate(columns):
        output_dict[column_name] = []
        columns_table.append((nr, column_name))

    for entry in gdx_sym:
        output_dict["value"].append(entry.value)

        for nr, column in columns_table:
            output_dict[column].append(entry.key(nr))

    df = pd.DataFrame(output_dict)
    return df


def load_TIMES_MEDEA_INTERFACE_file(path=path_to_times_medea_interface_setup):
    """
    Load the "TIMES - MEDEA Interface" file and perform some cleaning steps.
    - delete empty rows (used to structure the file)
    - neglect READ = False rows

    :param path: (Pathlike to the path of the "TIMES - MEDEA Interface" file
    :return: pd.Dataframe()
    """
    interface_meta = pd.read_csv(path, sep=";", decimal=",")
    # the READ colum provides a boolean weather to include the row into the export
    interface_meta = interface_meta[interface_meta["READ"]==True]
    # filter empty rows in the file (empyt rows help us to structure the file)
    interface_meta.dropna(axis=1, how="all", inplace=True)
    return interface_meta


def show_case_errors():
    # 1 ############################################
    # todo results gdx do not look as expected
    #   - domains names are not the same (ALLYEAR, T and YEAR)
    #   - OEM-Jan-Base.gdx has multiple sets of the symbols
    #   - leads to errors for different files
    symbols = ["F_IN", "F_OUT", "PAR_PASTI", "PAR_CAPL", ]
    gdx = load_file("AEA_Sandbox/OeM_Env/results/run_2010_2020.gdx")
    fh.yield_domains_as_strings(gdx, symbols)

    gdx = load_file("AEA_Sandbox/OeM/OEM-Jan-Base.gdx")
    fh.yield_domains_as_strings(gdx, symbols)


    # 2 #############################################


if __name__ == "__main__":
    gdx = load_file()
    prepare_files_for_standard_export(gdx, symbols=translation_symbols)
    if setup_reload_files == False:
        warnings.warn("Loading Symbols DF from pickle in prepare_dataframe_for_export")


