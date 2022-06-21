import gams
from pathlib import Path
import os

def load_gdx_from_path(path: str = "AEA_Sandbox/OeM_Env/results/run_2010_2013.gdx" ):
    """
    return a the gams db based on the a relative path from project root
    :param path: relative path from content root (e.g. "AEA_Sandbox/OeM/OEM-Jan-Base.gdx")
    :return: gams gdx db file
    """
    project_root = Path(__file__).parent.parent.parent
    print("project_root was set to:", project_root)
    path = os.path.join(project_root, path)

    ws = gams.GamsWorkspace()
    gdx_db = ws.add_database_from_gdx(path)
    return gdx_db


def retun_symbols_of_gdx(gdx_db):
    """
    prints and retuns all domains for a list of symbols in given gdx file
    :param gdx_db: a gams gdx file
    :return: list of symbol names
    """
    symbol_names = []
    for symbol in gdx_db:
        symbol = symbol.name
        symbol_names.append(symbol)
    return symbol_names


def yield_domains_as_strings(gdx_db, symbol) -> list:
    """
    retrun the dimensions for a given symbol
    :param gdx_db: gams db
    :param symbol:
    :return: list of symbols
    """
    return gdx_db[symbol].get_domains_as_strings()


def list_all_entities_of_db(gdx_db):
    """
    gams gdx is an iterable of sizzles
    :param gdx_db:
    :return:
    """
    for x in gdx_db:
        entries_as_text = x.get_name(), x.text
        print(entries_as_text)
        yield entries_as_text


def get_symbol_overview(gdx_db, symbol):
    """
    :param gdx_db:
    :param symbol:
    :return:
    """
    print(symbol)
    print("\tname:      " + symbol, gdx_db[symbol].text)
    print("\trecords:   " + str(gdx_db[symbol].number_records))
    print("\tdimensions:" + str(gdx_db[symbol].domains_as_strings))
    print("---")


if __name__ == "__main__":
    # Perform some quick analysis of the gdx
    # the better way to get a feeling for the gdx is GAMS Studio
    my_gdx_db = load_gdx_from_path()
    print("Successfully loaded:", my_gdx_db.get_name())
    print(my_gdx_db.get_name(), "has", len(my_gdx_db), "symbols.")

    # Check 4 important symbols (these symbols are used for the TIMES - MEDA communication
    symbols = ("F_IN", "F_OUT", "PAR_CAPL", "PAR_PASTI")
    for symbol in symbols:
        get_symbol_overview(my_gdx_db, symbol)


    print("fin")