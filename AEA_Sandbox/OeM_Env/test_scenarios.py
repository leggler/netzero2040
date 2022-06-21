from generate_milestonyr_bat_include import generate_bat_file
def test_generate_bat_file():
    s = "SET MILESTONYR / 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 /;"
    assert s == generate_bat_file(start=2010, end=2025)