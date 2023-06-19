import json
import requests
from django.views.decorators.csrf import csrf_exempt

# Read the JSON file and parse its contents
with open('region.json') as file:
    data = json.load(file)


# Construct the headers with the CSRF token
headers = {
    "X-CSRFToken": "HCKQhM9Cybn9IpVrLi4J4KrtzH6c3PHI",
    "Content-Type": "application/json" 
}

for region in data:
    # Extract the relevant data from the parsed JSON object
    id = int(region['id'])
    name = region['region_name']
    polygon = ""
    # Convert the data types of the extracted values if necessary
    if 'bbox' in region:
        if region['bbox']['type'] == 'Polygon':
            polygon_list = region['bbox']['coordinates'][0]
            for coordinates in polygon_list:
                polygon += str(coordinates[0]) + "," + str(coordinates[1]) + " "

    # Construct the GraphQL mutation query with the converted values
    mutation = '''
        mutation {
            createRegion(id: %s, name: "%s", polygon: "%s") {
                region{
                    id
                    name
                    polygon
                }
            }
     }
    ''' % (id, name, polygon)

    # Send the mutation request to the GraphQL server
    response = requests.post('http://127.0.0.1:8000/alerts/graphql', json={'query': mutation})

    try:
        result = response.text
        # Process the response JSON data here
        print(result)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e}")
