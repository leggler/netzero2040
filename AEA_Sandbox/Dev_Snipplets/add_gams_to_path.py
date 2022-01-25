import gams

# print(help(gams))

ws = gams.GamsWorkspace()
path = r"C:\Users\lzw\PycharmProjects\netzero2040\zwiebs_test_suite\BasicModel.gdx"
db2 = ws.add_database_from_gdx(path)

plants = ["Seattle", "San-Diego"]
markets = ["New-York", "Chicago", "Topeka"]
capacity = {"Seattle": 350.0, "San-Diego": 600.0}
demand = {"New-York": 325.0, "Chicago": 300.0, "Topeka": 275.0}
distance = {("Seattle", "New-York"): 2.5,
            ("Seattle", "Chicago"): 1.7,
            ("Seattle", "Topeka"): 1.8,
            ("San-Diego", "New-York"): 2.5,
            ("San-Diego", "Chicago"): 1.8,
            ("San-Diego", "Topeka"): 1.4
            }

db = ws. add_database()


i = db.add_set("i", 1, "canning plants")

"""for p in plants:
    i.add_record(p)

for x in db:
    print(x.get_name())

a = db.add_parameter_dc("a", [i], "capacity of plant i in cases")
for p in plants:
    a.add_record(p).value = capacity[p]
"""


for x in db2:
    if "PAR_" == x.get_name()[:4]:

        #print(x.get_name(), x.text)
        pass
print(db2["PAR_FLO"].text, db2["PAR_FLO"].get_dimension(), db2["PAR_FLO"].domains_as_strings,db2["PAR_FLO"].number_records)
print(db2["PAR_FLO"].__dir__())
#print(help(db2["PAR_FLO"]))
print(db2["PAR_FLO"].number_records)
"""
for x in db2["PAR_FLO"]:
    print(x.value)
    print(x.keys)
    #print(help(x))
    break
"""
# print(ws.__dir__())