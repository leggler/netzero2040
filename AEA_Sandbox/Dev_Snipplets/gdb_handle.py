import gams
from pathlib import Path
import os
import pyam
import pandas as pd

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
    try:
        print("\t" + gdx_db[entity_name].text)
        print("\t" + str(gdx_db[entity_name].number_records))
        print("\t" + str(gdx_db[entity_name].domains_as_strings))
    except GamsException as e:
        print(e)


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


def generate_pandas_dataframe(symbol: str, commodity_filter: str, process_filter: str):
    """

    :param symbol:
    :param commodity_filter:
    :param process_filter:
    :return:
    """

    regions = []
    years = []
    processes = []
    commodities = []
    time_scales = []
    levels = []
    variables = []
    units = []

    for x in gdx_db["VAR_FLO"]:
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

            # Todo get Variable name
            variables.append(f"NONE|Electricity|{process}")
            units.append("GJ")

    df = pd.DataFrame({
        "region": regions,
        "variable": variables,
        "unit": units,
        "year": years,
        "value": levels,
        "time_scale": time_scales
    })

    return df


if __name__ == "__main__":
    db_path = "AEA_Sandbox/OeM/OEM-Jan-Base.gdx"
    gdx_db = load_gdx_from_path(db_path)

    # switch this on to retrigger generate df otherwise load from pickle
    # do this if you changed something in generate_pandas_dataframe
    reload = False
    if reload:
        df = generate_pandas_dataframe(symbol="VAR_FLO", process_filter="EGRDELC00", commodity_filter="ELCELC")
        df.to_pickle("VAR_FLO_dev.pickle")
    else:
        print("WARING: Reload gdx_db was set to:", reload)

    df = pd.read_pickle("VAR_FLO_dev.pickle")
    df["model"] = "OeM"
    df["scenario"] = "OEM-Jan-Base"
    print(df)
    df_sum = df.groupby(["model", "scenario", "region", "variable", "unit", "year"]).sum()
    print(df_sum.reset_index())
    df_piv = pd.pivot_table(data=df_sum, columns=["year"], values="value",
                            index=["model", "scenario", "region", "variable", "unit"])
    print(df_piv)
    df_piv.to_csv("ELCELC_export_DE.csv", sep=";", decimal=",")
    df_piv.to_csv("ELCELC_export_EN.csv")


    # print(pyam.IamDataFrame(df_sum))
