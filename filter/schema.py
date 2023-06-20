import graphene
from graphene_django import DjangoObjectType
from graphene import String, Int
from .models import Alert, AlertInfo, Country, Region
import datetime
import requests
import secrets
from .views import compare_polygon
from django.db.models import Q

#This function will return a string that represents a single match query term

#TO DO:
#Cicile
#Remove filerted alerts based on id
#Filter by polygon
#Compare Expire Date
#Show alerts based on Language Preference
#Polygon Overlap
#Security: Allowed csrf

#Admin:
#Verify signature





class AlertInformationType(DjangoObjectType):
    class Meta:
        model = AlertInfo
        fields = ["category", "event", "urgency", "severity", "certainty", "effective", "senderName",
                  "headline", "description", "instruction", "areaDesc", "polygon", "geocode_name", "geocode_value",
                  "alert"]

class AlertType(DjangoObjectType):
    information = graphene.List(AlertInformationType)
    class Meta:
        model = Alert
        fields = ["hash_id", "processed_time"]

    def resolve_information(self, info):
        return self.information

class RegionType(DjangoObjectType):
    class Meta:
        model = Region
        fields = ["id", "name", "polygon"]

class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        fields = ["region_id", "id", "name", "society_name", "polygon", "centroid"]



class CreateRegion(graphene.Mutation):
    class Arguments:
        id = Int(required=True)
        name = String(required=True)
        polygon = String(required = True)

    region = graphene.Field(RegionType)

    def mutate(self, info, id, name, polygon):
        region = Region(id=id, name=name, polygon = polygon)
        region.save()
        return CreateRegion(region=region)

class CreateCountry(graphene.Mutation):
    class Arguments:
        id = Int(required=True)
        region_id = Int()
        name = String(required=True)
        society_name = String(required=True)
        polygon = String(required = True)
        centroid = String(required = True)

    country = graphene.Field(CountryType)

    def mutate(self, info, id, name, society_name, polygon, centroid, region_id=None):
        if region_id:
            country = Country(id=id, name=name, society_name= society_name, region_id=Region.objects.get(id=region_id), polygon = polygon, centroid=centroid)
        else:
            country = Country(id=id, name=name, society_name=society_name, region_id=None,
                              polygon=polygon, centroid=centroid)
        country.save()
        return CreateCountry(country=country)

class Mutation(graphene.ObjectType):
    create_region = CreateRegion.Field()
    create_country = CreateCountry.Field()

def generate_filtering_elastic_search_query_string(key, value):
    search_string = {
        "match": {
            "AlertBody.info." + key: {
                "query": value
            }
        }
    }
    return search_string

class Query(graphene.ObjectType):
    filtered_alerts = graphene.List(AlertType, filter_string=graphene.Argument(type_=graphene.String))

    def resolve_filtered_alerts(root, info, filter_string):
        # Define the host of elastic search
        host = "http://13.81.29.108:9200"
        index = 'alerts'
        # Move the filter conditions into map pairs
        filter_map = dict()
        filters = filter_string.split(",")
        for filter in filters:
            splitted_string = filter.strip().split(" = ")
            # Optimisation will decrease readability, my goal here is to show how the code works.
            key = splitted_string[0].strip()
            value = splitted_string[1].strip()
            filter_map[key] = value

        # These filtering keyword will be applied as direct search in the query
        FILTER_KEYWORDS = ["category", "event", "urgency",
                           "severity", "certainty", "senderName", "headline", "description", "instruction"]

        # By default, fetch alerts before three hours
        current_time = datetime.datetime.now()
        hour_before = 3

        # Match query will store all the query strings
        match_query = []
        polygons = []
        for key, value in filter_map.items():
            if key in FILTER_KEYWORDS:
                match_query.append(generate_filtering_elastic_search_query_string(key, value))
            elif key == "hours_before":
                hour_before = int(value)
            elif key == "region":
                matching_region = Region.objects.get(name=value)
                if matching_region == None:
                    return "The region name" + str(value) + "you provided is not identified."
                polygons.append(matching_region.polygon)
            elif key == "country":
                matching_countries = Country.objects.filter(Q(name__iexact=value) | Q(society_name__iexact=value))
                if len(matching_countries) == 0:
                    return "The country name" + str(value) + "you provided is not identified."
                for matching_country in matching_countries:
                    polygons.append(matching_country.polygon)
            else:
                return "Error: The Filter Contains Unrecongnised String"
        # Append a query section that querys evtTimestamp of the alert
        date_string = current_time - datetime.timedelta(hours=hour_before)
        date_query = {
            "range": {
                "evtTimestamp": {
                    "gte": date_string.isoformat()
                }
            }
        }
        match_query.append(date_query)
        # The holistic search to be performed to elastic search:
        query = {
            "query": {
                "bool": {
                    "must": [
                        match_query
                    ]
                }
            },
            "size": 10000
        }

        # Set the Content-Type header to application/json
        headers = {
            "Content-Type": "application/json"
        }
        url = f'{host}/{index}/_search'
        response = requests.post(url, json=query, headers=headers)
        # Process the search results
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            number_of_hits = data["hits"]["total"]["value"]
            alerts = data["hits"]["hits"]
            filtered_alerts = []


            # Fetch the information of alerts and encapsulate these information into alert instance
            for alert in alerts:
                new_alert = AlertType(hash_id = secrets.token_hex(16))
                alert_body = alert["_source"]["AlertBody"]
                # It is quite confused that the info field can be both list or just an element
                # Here I convert non-list element into a list.


                if not isinstance(alert_body["info"], list):
                    alert_body["info"] = [alert_body["info"]]
                informations = []
                for alert_info in alert_body["info"]:
                    #Check if two polygons intersect
                    alert_polygon = "None"
                    # Only if there is at least one alert whose polygon intersects with the specified region, record that region
                    # Otherwise skip the processing.
                    continue_loop = True
                    #If the filter does not apply regional search, just record the polygon
                    if len(polygons) == 0:
                        if "polygon" in alert_info["area"]:
                            if alert_info["area"]["polygon"] is not None:
                                alert_polygon = alert_info["area"]["polygon"]
                                continue_loop = False
                    # If the filter applies regional search, compare the polygon of the alerts
                    # If they do not intersect, then the alert is not relevant and should be removed.
                    if len(polygons) != 0:
                        if "polygon" in alert_info["area"]:
                            if alert_info["area"]["polygon"] is not None:
                                alert_polygon = alert_info["area"]["polygon"]
                                #If there is at least one relevant alert that intersects with the region
                                #Then record that alert
                                for polygon in polygons:
                                    if compare_polygon(alert_polygon, polygon):
                                        continue_loop = False
                                        break
                            #If the polygon field to be compared is none, then stop processing this alert.
                            else:
                                continue
                    #If the alert is not falling into any of specified region, then skip processing this alert.
                    if continue_loop:
                        continue


                    if type(alert_info["category"]) == list:
                        category = ' '.join(alert_info["category"])
                    elif alert_info["category"] is not None:
                        category = alert_info["category"]
                    else:
                        category = "None"

                    if alert_info["event"] is not None:
                        event = alert_info["event"]
                    else:
                        event = "None"

                    if alert_info["urgency"] is not None:
                        urgency = alert_info["urgency"]
                    else:
                        urgency = "None"

                    if alert_info["severity"] is not None:
                        severity = alert_info["severity"]
                    else:
                        severity = "None"

                    if alert_info["certainty"] is not None:
                        certainty = alert_info["certainty"]
                    else:
                        certainty = "None"

                    effective = "None"
                    if "effective" in alert_info:
                        if alert_info["effective"] is not None:
                            effective = alert_info["effective"]

                    if alert_info["senderName"] is not None:
                        senderName = alert_info["senderName"]
                    else:
                        senderName = "None"

                    if alert_info["headline"] is not None:
                        headline = alert_info["headline"]
                    else:
                        headline = "None"

                    if alert_info["description"] is not None:
                        description = alert_info["description"]
                    else:
                        description = "None"

                    instruction = "None"
                    if "instruction" in alert_info:
                        if alert_info["instruction"] is not None:
                            instruction = alert_info["instruction"]

                    areaDesc = "None"
                    if "areaDesc" in alert_info["area"]:
                        if alert_info["area"]["areaDesc"] is not None:
                            areaDesc = alert_info["area"]["areaDesc"]



                    geocode_name = "None"
                    if "geocode_name" in alert_info["area"]:
                        if alert_info["area"]["geocode_name"] is not None:
                            geocode_name = alert_info["area"]["geocode_name"]

                    geocode_value = "None"
                    if "geocode_value" in alert_info["area"]:
                        if alert_info["area"]["geocode_value"] is not None:
                            geocode_value = alert_info["area"]["geocode_value"]

                    informations.append(AlertInformationType(category=category, event=event, urgency=urgency, severity=severity,
                      certainty=certainty, effective=effective, senderName=senderName,
                      headline=headline, description=description, instruction=instruction,
                      areaDesc=areaDesc, polygon=alert_polygon, geocode_name=geocode_name, geocode_value=geocode_value))
                new_alert.information = informations
                filtered_alerts.append(new_alert)
            return filtered_alerts

        else:
            return f"Search request failed with status code: {response.status_code}"



schema = graphene.Schema(query=Query, mutation=Mutation)