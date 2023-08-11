import json
import csv

# ## Transform data to a csv file
# # id: districtName (GID_1)
# # name: name of administrative level (NAME_1)
# # country: foreign key (country iso3)
# # polygon: polygon string

# input_file_path = '../TestData/world.geojson'
input_file_path = "../TestData/countries/AFG/afg.geojson"

# Load JSON data from the file
with open(input_file_path, "r") as input_file:
    data = json.load(input_file)

admin1_data = []
for item in data['features']:
    admin1_item = dict()
    admin1_item['id'] = item['properties']['GID_1']
    admin1_item['name'] = item['properties']['NAME_1']
    admin1_item['country'] = item['properties']['GID_0']
    admin1_item['polygon'] = item['geometry']['coordinates']
    admin1_data.append(admin1_item)

output_file_path = "../TestData/countries/AFG/afg.csv"
with open(output_file_path, "x", newline="") as output_file:
    fieldnames = ["id", "name", "country", "polygon"]
    writer = csv.DictWriter(output_file,
                            fieldnames=fieldnames)

    # Write the header (field names)
    writer.writeheader()

    # Write the data rows
    for row in admin1_data:
        writer.writerow(row)
