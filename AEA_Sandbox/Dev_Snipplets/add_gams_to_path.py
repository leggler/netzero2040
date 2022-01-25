import gams
from pathlib import Path
import os
from gams.workspace import GamsException
# print(help(gams))

def load_gdx_from_path(path:str):
    """
    return a the gams db based on the a realative path from project root
    :param path: relative path from content root (e.g. "AEA_Sandbox/OeM/OEM-Jan-Base.gdx")
    :return: gams gdx db file
    """
    project_root = Path(__file__).parent.parent.parent
    path = os.path.join(project_root, "AEA_Sandbox/OeM/OEM-Jan-Base.gdx")
    ws = gams.GamsWorkspace()
    gdx_db = ws.add_database_from_gdx(path)
    return gdx_db

"VAR_FLO; PRC: EGRdELC00, COM: ELCELC; TS; WN,WD,TN, TD, SN, SD"

parameter = [
    "VAR_FLO",
    "PRC",
    "COM",
    "TS",
    "WN",
    "WD",
    "TN",
    "SN",
    "SD"]
def list_all_entities_of_db(db):
    for x in db:
        print(x.get_name(), x.text)



def read_entity(entity_name):
    try:
        print("\t" + gdx_db[entity_name].text)
        print("\t" + str(gdx_db[entity_name].number_records))
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


if __name__ == "__main__":
    db_path = "AEA_Sandbox/OeM/OEM-Jan-Base.gdx"
    gdx_db = load_gdx_from_path(db_path)
    # list all entities
    list_all_entities_of_db(gdx_db)

    #look for entities of interest
    for entity in parameter:
        print(entity)
        read_entity(entity_name=entity)
        print()
    print(help(gdx_db))
