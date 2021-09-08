from urllib import parse
import random
import FleetManager
import json
import requests


# Print statements are made within the API methods to aid in debugging
# with the use of the command console.
class Methods:

    @staticmethod
    def parsePostPath(path):
        print('Inside parsePostPath:' + '\n')

        path_parse = parse.urlparse(path)
        i = 0
        while path_parse[i]:
            print('Result of path parse at i: ' + path_parse[i] + ' ' + i.__str__() + '\n')
            i += 1
        path = path_parse[2]
        print('Path of url: ' + path + '\n\n')
        if path != "/supply/requestv" and path != "/supply/testRoute":
            raise Exception("Not a valid POST request path.")
        else:
            print("Path is valid!")
        return path

    @staticmethod
    def parseGetPath(path):
        print('Inside parseGetPath:')

        path_parse = parse.urlparse(path)
        i = 0
        while path_parse[i]:
            print('Result of path parse at i: ' + path_parse[i] + ' ' + i.__str__() + '\n')
            i += 1
        path = path_parse[2]
        print('Path of url: ' + path + '\n\n')
        if path != "/dispatchV/testDispatch":
            raise Exception("Not a valid GET request path.")
        return path

    # Handles Post Request data
    @staticmethod
    def getOrderJSON(post_body):

        post_dict = json.loads(post_body)
        print(post_dict)
        order_id = post_dict.get("orderID")
        ptype = post_dict.get("ptype")
        dloc = post_dict.get("dloc")
        ploc = post_dict.get("ploc")
        username = post_dict.get("username")

        print(order_id)
        print(ptype)
        print(dloc)
        print(ploc)
        print(username)

        return post_dict

    # ----------------------Parses Data so we can send to Dispatch---------------------------
    # Returns Delivery Location stored in JSON dict
    @staticmethod
    def getOrderID(json):
        print('Inside getOrderID:' + '\n')
        orderID = json.get("orderID")

        if not isinstance(orderID, int):
            raise Exception("orderID must be an int.")

        print('Order ID: ' + str(orderID) + '\n\n')
        return orderID

    # Gets payload type from JSON dict
    # Only accepts a value of 'veg' or 'clothes'
    @staticmethod
    def getPayload(json):
        print('Inside getPayload:' + '\n')
        # Get ptype from json dict
        ptype = json.get("ptype")

        if ptype != "veg" and ptype != "clothes":
            raise Exception("Not a valid parameter for vehicle request.")

        print('Payload type: ' + ptype + '\n\n')
        return ptype

    # Returns Delivery Location stored in JSON dict
    @staticmethod
    def getDeliveryLocation(json):
        print('Inside getDeliveryLocation:' + '\n')
        dloc = json.get("dloc")
        print('Delivery location: ' + dloc + '\n\n')
        return dloc

    # Returns Payload Location stored in JSON dict
    @staticmethod
    def getPayloadLocation(json):
        print('Inside getPayloadLocation:' + '\n')
        ploc = json.get("ploc")
        print('Payload location: ' + ploc + '\n\n')
        return ploc

    # Returns Payload Location stored in JSON dict
    @staticmethod
    def getUsername(json):
        print('Inside getUsername:' + '\n')
        username = json.get("username")
        print('Username: ' + username + '\n\n')
        return username

    # ----------Creating Route from order details to send to Dispatch - Google Maps API ----------------------------
    @staticmethod
    def create_route(ploc, dloc):
        print('Inside createRoute:' + '\n')
        http = 'https://maps.googleapis.com/maps/api/directions/json?'

        params = dict(
            # origin is where the vehicle is currently located
            origin="2704 East 22nd St, Austin, TX, 78722",
            destination=dloc,
            waypoints=ploc,
            key='AIzaSyBTZWJKRnWJPgEBj9VyjFfzWTxl5sEPLkQ'
        )

        # IMPORT REQUESTS VS REQUEST LOOKUP!!!
        data = requests.get(url=http, params=params)

        binary = data.content
        route = json.loads(binary)

        if route.get('status') == "OK":
            print("Route Status: 200")
        else:
            print('INVALID ADDRESS ENTERED!')
        return route
