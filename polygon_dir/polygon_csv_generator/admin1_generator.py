import geopandas as gpd

## Transform data to a csv file
# id: districtName (GID_1)
# admin1Name: name of that administrative region (NAME_1)
# country: foreign key (country iso3)
# polygon: polygon string

file_path = '/Users/chenyuechen/Documents/TestData/world/world.geojson'
# file_path = '/Users/chenyuechen/Documents/TestData/countries/AFG/afg.geojson'
gdf = gpd.read_file(file_path)

print("hello world")
