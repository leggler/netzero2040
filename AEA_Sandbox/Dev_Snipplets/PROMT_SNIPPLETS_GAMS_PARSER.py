

# Start GAMS DB 
import gams
import pandas as pd
import os
root = os.getcwd()

# two example OeModels
path = os.path.join(root, "netzero2040\AEA_Sandbox\BasicModel\BasicModel.gdx")
path = os.path.join(root, "netzero2040\AEA_Sandbox\OeM\OEM-Jan-Base.gdx")

# load gdx_db
ws = gams.GamsWorkspace()
gdx_db = ws.add_database_from_gdx(path)


####### SYMBOL UTIL ########
gdx_db["VAR_FLO"].get_name() # get name of
gdx_db["VAR_FLO"].get_domains_as_strings() # get dimensions

print("Länge der DB:", len(gdx_db["VAR_FLO"]))

domains = gdx_db["VAR_FLO"].get_domains()
for domain in domains:
    print(domain, domain.text)

# expected domains of gdx_df["VAR_FLO"].domains
# ['R', 'ALLYEAR', 'ALLYEAR', 'P', 'C', 'S']
#   R ~         Regions
#   ALLYEAR ~   SOME YEAR # Todo find out diff between ALLYEAR and ALLYEAR
#   ALLYEAR ~   SOME YEAR # Todo find out
#   P ~         process
#   C ~         commodity
#   S ~         Timescale





###### TEST ########

# Test if ALLYEAR1 == ALLYEAR2
# FAILS
for x in gdx_db["VAR_FLO"]:
    if x.key(1) != x.key(2):
        print(x)

# Test if ALLYEAR1 == ALLYEAR2 for ELCELC
# PASSES
for x in gdx_db["VAR_FLO"]:
    if x.key(1) != x.key(2):
        if (x.key(3) == "EGRDELC00") and (x.key(3) == "ELCELC"):
            print(x)

####### END ########