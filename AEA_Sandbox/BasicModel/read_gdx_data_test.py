import gdxpds
import glob


print(glob.glob("*.gdx"))

print(gdxpds.read_gdx.to_dataframes("Test/BasicModel.gdx", gams_dir=None))