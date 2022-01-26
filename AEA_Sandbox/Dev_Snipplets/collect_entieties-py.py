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


def list_all_entities_of_db(db):
    """
    gams db is an iterable of sizzles
    :param db:
    :return:
    """
    for x in db:
        # print(x.get_name(), x.text)
        yield x.get_name()

if __name__ == "__main__":
    db_path = "AEA_Sandbox/OeM/OEM-Jan-Base.gdx"
    gdx_db = load_gdx_from_path(db_path)

    # list_all_entities_of_db(gdx_db)
    # switch for development
    names = list(list_all_entities_of_db(gdx_db))
    if False:
        df = pd.DataFrame([[x.key(3), x.key(4)] for x in gdx_db["VAR_FLO"]], columns=['processes', 'commodities'])
        df.to_pickle("process_commodity_map.pickle")
    df = pd.read_pickle("process_commodity_map.pickle")
    df.drop_duplicates(inplace=True)
    print(df)

    print("Number of unique processes:", len(df['processes'].str.slice(3).unique()))
    print("Number of unique commodities:", len(df['commodities'].unique()))
    print("Number of unique process-commodity combinations:", len((df['processes'] + df['commodities']).unique()))
    print(sorted(df["commodities"].str.slice(stop=3).unique()))


    # look for descriptions in the symbols of gdx_file.
    # found no useful information
    idk = df["processes"].str.slice(stop=3).unique()
    for i in idk:
        print(i)
        if i in names:
            print("\t", i, gdx_db.get_symbol(i).text)