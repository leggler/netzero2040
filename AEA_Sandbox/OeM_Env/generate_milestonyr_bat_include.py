"""
Gernate a bat file that can be included in the x_run.dd file
The file will be included based on the name
    netzero2040\AEA_Sandbox\OeM_Env\Input\milestonyr_0.aea

so simply change this file  to manipulate the years

there is a template @ netzero2040\AEA_Sandbox\OeM_Env\Input\milestonyr_template.aea
"""


def generate_bat_string(start=2010, end=2040, step=1, list=[]):
    if list == []:
        years = range(start, end+step, step)

    batfile_string = "SET MILESTONYR / "
    for year in years:
        batfile_string += str(year) + ", "
    batfile_string = batfile_string[:-2]
    batfile_string += " /;"

    return batfile_string


def write_aea_file(bat_text):
    file_name = "Input\milestonyr_0.aea"
    with open(file_name, "w") as aea_file:
        aea_file.write(bat_text)

    return file_name

def generate_bat_file(start=2010, end=2040, step=1, list=[]):
    bat_string = generate_bat_string(start=start, end=end, step=step, list=list)
    file_name = write_aea_file(bat_string)
    return file_name

if __name__ == "__main__":
    print(generate_bat_file())
    print(generate_bat_file(start=2010, end=2013, step=2))
    # test_generate_bat_file()