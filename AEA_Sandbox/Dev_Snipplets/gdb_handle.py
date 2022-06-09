import gams
from pathlib import Path
import os
import pyam
import pandas as pd
import numpy as np

from gams.workspace import GamsException


# print(help(gams))

def load_gdx_from_path(path: str):
    """
    return a the gams db based on the a realative path from project root
    :param path: relative path from content root (e.g. "AEA_Sandbox/OeM/OEM-Jan-Base.gdx")
    :return: gams gdx db file
    """
    project_root = Path(__file__).parent.parent.parent
    # todo make "path" useful
    path = os.path.join(project_root, "AEA_Sandbox/OeM/OEM-Jan-Base.gdx")
    path = os.path.join(project_root, "AEA_Sandbox/OeM_Env/results/run_2010_2013.gdx")
    # todo @leggler error handling or file name check or smth
    ws = gams.GamsWorkspace()
    gdx_db = ws.add_database_from_gdx(path)


    return gdx_db


# Note from Martin:
"VAR_FLO; PRC: EGRDELC00, COM: ELCELC; TS; WN,WD,TN, TD, SN, SD"

parameter = [
    "VAR_FLO",
    "PRC",
    "COM",
    "TS",
    "WN",  # Winter Night
    "WD",  # Winter Day
    "TN",  # Transition Night
    "TD",  # Transition Day
    "SN",  # Summer Night
    "SD",  # Summer Day
    #
    "R",
    "ALLYEAR",
    "P",
    "C",
    "S"
]


def list_all_entities_of_db(db):
    """
    gams db is an iterable of sizzles
    :param db:
    :return:
    """
    for x in db:
        print(x.get_name(), x.text)


def read_entity(entity_name):
        print("\t" + gdx_db[entity_name].text)
        print("\t" + str(gdx_db[entity_name].number_records))
        print("\t" + str(gdx_db[entity_name].domains_as_strings))



###### HELPERS #######
#     # print(gdx_db["PAR_FLO"].text, gdx_db["PAR_FLO"].get_dimension(), gdx_db["PAR_FLO"].domains_as_strings,gdx_db["PAR_FLO"].number_records)
#     # print(gdx_db["PAR_FLO"].__dir__())
#     #print(help(db2["PAR_FLO"]))
# for x in db2["PAR_FLO"]:
#     print(x.value)
#     print(x.keys)
#     #print(help(x))
#     break
# [print(x) for x in gdx_db.__dir__()]
# print(help(gdx_db))

def easy_filter_by_xx(gdx_db):
    domains = gdx_db["VAR_FLO"]
    for domain in domains:
        # print(domain)
        if "EGRDELC00" == domain.keys[3].upper():
            print("\t", domain)
            # print(domain._symbol.__dict__)
            # print(domain._symbol)
        if "ELCELC" == domain.keys[3].upper():
            print("\t", domain)

def generate_full_pandas_dataframe_var_flow(symbol: str,
                                            model: str,
                                            scenario: str,
                                            unit: str = "TJ"
                                            ):
    regions = []
    years = []
    processes = []
    commodities = []
    time_scales = []
    levels = []
    variables = []
    units = []

    for x in gdx_db.get_symbol(symbol_identifier=symbol):
        # print(x)
        #  todo check if there is a better way to filter x.marginal
        if x.marginal != 0:
            continue

        region = x.key(0)
        year = x.key(1)
        process = x.key(3)
        commodity = x.key(4)
        timescale = x.key(5)
        level = x.level


        regions.append(region)
        years.append(year)
        processes.append(process)
        commodities.append(commodity)
        time_scales.append(timescale)
        levels.append(level)

        variables.append(f"{model}|????|{process}")
        units.append(unit)

    df = pd.DataFrame({
        "region": regions,
        "variable": variables,
        "process": processes,
        "commodity": commodities,
        "unit": units,
        "year": years,
        "value": levels,
        "time_scale": time_scales
    })
    df["model"] = model
    df["scenario"] = scenario
    return df

def generate_full_pandas_dataframe_PAR_CAPL(symbol: str,
                                            model: str,
                                            scenario: str,
                                            unit: str = "GJ"
                                            ):
    regions = []
    years = []
    processes = []
    value = []
    units = []

    for x in gdx_db.get_symbol(symbol_identifier=symbol):
        print(x)

        region = x.key(0)
        year = x.key(1)
        level = x.value

    return



def generate_pandas_dataframe(
        symbol: str,
        fuel: str,
        commodity_filter: str,
        process_filter: str,
        model: str,
        scenario: str

                              ):
    """

    :param symbol:
    :param fuel:
    :param commodity_filter:
    :param process_filter:
    :param model:
    :param scenario:
    :return:
    """
    # setup collectors
    regions = []
    years = []
    processes = []
    commodities = []
    time_scales = []
    levels = []
    variables = []
    units = []

    for x in gdx_db.get_symbol(symbol_identifier=symbol):
        process = x.key(3)
        commodity = x.key(4)

        # Test if the entry confirms(?) the filter
        if commodity == commodity_filter and process == process_filter:
            region = x.key(0)
            year = x.key(1)
            timescale = x.key(5)
            level = x.level

            regions.append(region)
            years.append(year)
            processes.append(process)
            commodities.append(commodity)
            time_scales.append(timescale)
            levels.append(level)

            variables.append(f"{model}|{fuel}|{process}")
            units.append("GJ")

    df = pd.DataFrame({
        "region": regions,
        "variable": variables,
        "unit": units,
        "year": years,
        "value": levels,
        "time_scale": time_scales
    })
    df["model"] = model
    df["scenario"] = scenario

    return df

def collect_all_combinations_of_symbol(symbol, gdx_file):
    """

    :param symbol:
    :return:
    """
    ps = []
    cs = []
    for entry in gdx_file.get_symbol(symbol_identifier=symbol):
        ps.append(entry.key(3))
        cs.append(entry.key(4))
    df = pd.DataFrame({"process": ps, "commodities": cs})
    df.drop_duplicates().to_clipboard()
    print(df.drop_duplicates())
    df[["process"]].drop_duplicates().to_csv("unique_processes.csv", sep=";")
    df[["commodities"]].drop_duplicates().to_csv("unique_commodities.csv", sep=";")


if __name__ == "__main__":
    db_path = "AEA_Sandbox/OeM/OEM-Jan-Base.gdx"
    db_path = r"AEA_Sandbox/OeM_Env/results/run_2010_2013.gdx"

    model = "OeM"
    scenario = Path(db_path).name
    print("Scenario:", scenario)

    # switch this on to retrigger generate df otherwise load from pickle
    # do this if you changed something in generate_pandas_dataframe

    gdx_db = load_gdx_from_path(db_path)
    collect_all_combinations_of_symbol(symbol="VAR_FLO", gdx_file=gdx_db)
    exit()
    reload = True
    if reload:
        gdx_db = load_gdx_from_path(db_path)
        print("-" * 100)
        generate_full_pandas_dataframe_PAR_CAPL(symbol="PAR_CAPL",
                                                model="OeM",
                                                scenario=scenario)
        print("-" * 100)


        df = generate_full_pandas_dataframe_var_flow(symbol="VAR_FLO",
                                                     model="OeM",
                                                     scenario=scenario

                                                     )



        df.to_pickle("VAR_FLO_dev.pickle")
    else:
        df = pd.read_pickle("VAR_FLO_dev.pickle")
        print("WARING: Reload gdx_db was set to:", reload)






    interface_meta = pd.read_csv("Interface_times_medea.csv", sep=";", decimal=",")
    for _,row in interface_meta.iterrows():
        # print(row)
        symbol = row.ATTRIBUTE
        process = row.PRC
        commodity = row.COM

        print(process, commodity)


        process_filter = df["process"].str.contains(process)
        commodity_filter = df["commodity"].str.contains(commodity)
        combined_filter = np.logical_and(process_filter, commodity_filter)
        df_t = df[combined_filter]


        print(df_t)
    df = pd.read_pickle("VAR_FLO_dev.pickle")
    print(df)


    """
    df_sum = df.groupby(["model", "scenario", "region", "variable", "unit", "year"]).sum()
    print(df_sum.reset_index())
    df_piv = pd.pivot_table(data=df_sum, columns=["year"], values="value",
                            index=["model", "scenario", "region", "variable", "unit"])

    
    print(df_piv)
    df_piv.to_csv("ELCELC_export_DE.csv", sep=";", decimal=",")
    df_piv.to_csv("ELCELC_export_EN.csv")

    """
    print("fin")