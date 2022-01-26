import gams
from pathlib import Path
import os

import pandas as pd

from gams.workspace import GamsException
# print(help(gams))

def load_gdx_from_path(path:str):
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
        "WN",   # Winter Night
        "WD",   # Winter Day
        "TN",   # Transition Night
        "TD",   # Transition Day
        "SN",   # Summer Night
        "SD",   # Summer Day
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
        #print(domain)
        if "EGRDELC00" == domain.keys[3].upper():
            print("\t", domain)
            # print(domain._symbol.__dict__)
            # print(domain._symbol)
        if "ELCELC" == domain.keys[3].upper():
            print("\t", domain)

def generate_dataframe():
    regions = []
    years = []
    processes = []
    commodities = []
    time_scales = []
    levels = []
    model_names = []
    variables = []
    units = []
    for x in gdx_db["VAR_FLO"]:
        # print(x.keys)
        REG  = x.key(0)
        YEAR = x.key(1)
        P = x.key(3)
        C = x.key(4)
        S = x.key(5)
        level = x.level

        if C == "ELCELC" and P == "EGRDELC00":

            regions.append(REG)
            years.append(YEAR)
            processes.append(P)
            commodities.append(C)
            time_scales.append(S)
            levels.append(level)

            #Todo get Variable name
            variables.append(f"NONE|Electricity|{P}")
            units .append("GWH")

    df = pd.DataFrame({
        "Region": regions,
        "Variable": variables,
        "Unit": units,
        "Year": years,
        "Value":levels,
        "time_scale":time_scales
    })

    df["Model"] = "OEModel"
    df["Scenario"] = "BasicModel"
    return df

if __name__ == "__main__":
    db_path = "AEA_Sandbox/OeM/OEM-Jan-Base.gdx"
    gdx_db = load_gdx_from_path(db_path)
    # PRC ~ processes
    # C ~ commodities
    # easy_filter_by_xx(gdx_db)
    # print(gdx_db["VAR_FLO"].get_domains_as_strings())
    # print(dir(gdx_db["VAR_FLO"]))
    # print(gdx_db["VAR_FLO"])


    print("Länge der DB:", len(gdx_db["VAR_FLO"]))
    domains = gdx_db["VAR_FLO"].get_domains()
    for domain in domains:
        print(domain.text)

    # switch this on to retrigger generate df otherwise load from pickle
    if False:
        df = generate_dataframe()

        df.to_pickle("VAR_FLO_dev.pickle")

    df = pd.read_pickle("VAR_FLO_dev.pickle")
    print(df)
    df_sum = df.groupby(["Model", "Scenario", "Region", "Variable", "Unit", "Year"]).sum()
    print(df_sum.reset_index())
    df_piv = pd.pivot_table(data=df_sum, columns=["Year"],values="Value", index = ["Model", "Scenario", "Region", "Variable", "Unit"] )
    print(df_piv)
    df_piv.to_csv("ELCELC_export_DE.csv", sep=";", decimal=",")
    df_piv.to_csv("ELCELC_export_EN.csv")
    quit()

    # list all entities
    # list_all_entities_of_db(gdx_db)

    #look for entities of interest
    for entity in parameter:
        print(entity)
        read_entity(entity_name=entity)
        print()

def get_variable_name(oem_name):
    if oem_name == "ealskjf":
        netzero_name = "Electricity"
    else:
        raise ValueError
    return netzero_name

 #   [{"model":"", "scenaro": "", "region":"", "variable":"", "unit":"", "values" [}]}]

