import graphene
from graphene_django import DjangoObjectType
from .models import alert
import datetime
import requests


#This function will return a string that represents a single match query term


class Alert(DjangoObjectType):
    class Meta:
        model = alert
        fields = ["category", "event", "urgency", "severity", "certainty", "effective", "senderName",
                  "headline", "description", "instruction", "areaDesc", "polygon", "geocode_name", "geocode_value",
                  "processed_time"]


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
    filtered_alerts = graphene.List(Alert, filter_string=graphene.Argument(type_=graphene.String))

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
        for key, value in filter_map.items():
            if key in FILTER_KEYWORDS:
                match_query.append(generate_filtering_elastic_search_query_string(key, value))
            elif key == "hours_before":
                hour_before = int(value)
            else:
                print("Error: The Filter Contains Unrecongnised String")
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

        print(query)
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
                alert_body = alert["_source"]["AlertBody"]
                if type(alert_body["info"]["category"]) == list:
                    category = ' '.join(alert_body["info"]["category"])

                elif alert_body["info"]["category"] is not None:
                    category = alert_body["info"]["category"]
                else:
                    category = "None"

                if alert_body["info"]["event"] is not None:
                    event = alert_body["info"]["event"]
                else:
                    event = "None"

                if alert_body["info"]["urgency"] is not None:
                    urgency = alert_body["info"]["urgency"]
                else:
                    urgency = "None"

                if alert_body["info"]["severity"] is not None:
                    severity = alert_body["info"]["severity"]
                else:
                    severity = "None"

                if alert_body["info"]["certainty"] is not None:
                    certainty = alert_body["info"]["certainty"]
                else:
                    certainty = "None"

                effective = "None"
                if "effective" in alert_body["info"]:
                    if alert_body["info"]["effective"] is not None:
                        effective = alert_body["info"]["effective"]

                if alert_body["info"]["senderName"] is not None:
                    senderName = alert_body["info"]["senderName"]
                else:
                    senderName = "None"

                if alert_body["info"]["headline"] is not None:
                    headline = alert_body["info"]["headline"]
                else:
                    headline = "None"

                if alert_body["info"]["description"] is not None:
                    description = alert_body["info"]["description"]
                else:
                    description = "None"

                instruction = "None"
                if "instruction" in alert_body["info"]:
                    if alert_body["info"]["instruction"] is not None:
                        instruction = alert_body["info"]["instruction"]

                areaDesc = "None"
                if "areaDesc" in alert_body["info"]["area"]:
                    if alert_body["info"]["area"]["areaDesc"] is not None:
                        areaDesc = alert_body["info"]["area"]["areaDesc"]

                polygon = "None"
                if "polygon" in alert_body["info"]["area"]:
                    if alert_body["info"]["area"]["polygon"] is not None:
                        polygon = alert_body["info"]["area"]["polygon"]

                geocode_name = "None"
                if "geocode_name" in alert_body["info"]["area"]:
                    if alert_body["info"]["area"]["geocode_name"] is not None:
                        geocode_name = alert_body["info"]["area"]["geocode_name"]

                geocode_value = "None"
                if "geocode_value" in alert_body["info"]["area"]:
                    if alert_body["info"]["area"]["geocode_value"] is not None:
                        geocode_value = alert_body["info"]["area"]["geocode_value"]
                filtered_alerts.append(Alert(category=category, event=event, urgency=urgency, severity=severity,
                      certainty=certainty, effective=effective, senderName=senderName,
                      headline=headline, description=description, instruction=instruction,
                      areaDesc=areaDesc, polygon=polygon, geocode_name=geocode_name, geocode_value=geocode_value,
                      processed_time=datetime.datetime.now()))
            return filtered_alerts

        else:
            return f"Search request failed with status code: {response.status_code}"



schema = graphene.Schema(query=Query)