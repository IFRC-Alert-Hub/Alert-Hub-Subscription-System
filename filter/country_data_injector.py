import json
import requests
from django.views.decorators.csrf import csrf_exempt

# Read the JSON file and parse its contents
with open('country.json') as file:
    data = json.load(file)


# Construct the headers with the CSRF token
headers = {
    "X-CSRFToken": "HCKQhM9Cybn9IpVrLi4J4KrtzH6c3PHI",
    "Content-Type": "application/json"
}

for country in data:
    # Extract the relevant data from the parsed JSON object
    id = int(country['id'])
    #Negative one indicates that the region id is none
    if country['region'] != None:
        region_id = int(country['region'])

    name = country['name']
    society_name = country['society_name']
    polygon = ""
    # Convert the data types of the extracted values if necessary
    if 'bbox' in country and country['bbox'] != None:
        if country['bbox']['type'] == 'Polygon':
            polygon_list = country['bbox']['coordinates'][0]
            for coordinates in polygon_list:
                polygon += str(coordinates[0]) + "," + str(coordinates[1]) + " "
    centroid = ""
    if 'centroid' in country and country['centroid'] != None:
        if country['centroid']['type'] == 'Point':
            coordinates = country['centroid']['coordinates']
            centroid += str(coordinates[0]) + "," + str(coordinates[1])

    if region_id == None:
        mutation = '''
            mutation {
                createCountry(id: %s, name: "%s", societyName: "%s", polygon: "%s", centroid: "%s") {
                    country{
                        id
                        name
                        polygon
                    }
                }
            }
        ''' % (id, name, society_name, polygon, centroid)
    else:
        # Construct the GraphQL mutation query with the converted values
        mutation = '''
            mutation {
                createCountry(id: %s, regionId: %s, name: "%s", societyName: "%s", polygon: "%s", centroid: "%s") {
                    country{
                        id
                        name
                        polygon
                    }
                }
            }
        ''' % (id, region_id, name, society_name, polygon, centroid)

    # Send the mutation request to the GraphQL server
    response = requests.post('http://127.0.0.1:8000/alerts/graphql', json={'query': mutation})

    try:
        result = response.text
        # Process the response JSON data here
        print(result)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
