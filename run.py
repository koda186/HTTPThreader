# HTTPServer is a simple subclass of socketserver.TCPServer,
# and does not use multiple threads or processes to handle requests.
# To add threading or forking, create a new class using the appropriate mix-in from socketserver.
# Each time the server receives a request, it starts a new thread or process to handle it:


import VehicleDispatch_Methods
import FleetManager
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import json
import Veh_Supply


# Threading allows for Concurrency here - it handles two ongoing threads at the same time.
# Python standard library alllows this by adding a mixin to the HTTPServer
# Think of a mixin as a helper class adding in extra behavior
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass


# BaseHTTPRequestHandler is intended to be extended to handle each protocol method (GET, POST ETC).
# To add threading you have to create a new class using the appropriate mix-in form socketserver ie. ThreadingMixIn
class Handler(BaseHTTPRequestHandler):

    # Any and all POST requests will reach here.
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type',
                         'application/json; charset=utf-8')
        self.end_headers()
        thread = threading.currentThread().getName()
        # Parsing and checking POST request path.

        print(self.path)
        path = VehicleDispatch_Methods.Methods.parsePostPath(self.path)
        print(path)

        if path == "/supply/requestv":

            # Path is valid. Parsing request.
            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)

            print('content length follows: ' + str(content_len))
            print('Postman post body equals: ' + str(post_body) + '\n')

            # Parse testroute post_body
            order_json = VehicleDispatch_Methods.Methods.getOrderJSON(post_body)
            print(order_json)

            # Gets order info needed from JSON dict
            order_id = VehicleDispatch_Methods.Methods.getOrderID(order_json)
            ptype = VehicleDispatch_Methods.Methods.getPayload(order_json)
            dloc = VehicleDispatch_Methods.Methods.getDeliveryLocation(order_json)
            ploc = VehicleDispatch_Methods.Methods.getPayloadLocation(order_json)
            username = VehicleDispatch_Methods.Methods.getUsername(order_json)

            # Send locations using google maps api, if valid will return status 200
            route_for_vehicle = VehicleDispatch_Methods.Methods.create_route(ploc, dloc)

            # Assign inactive vehicle to active status
            get_active_vehicle = FleetManager.Dispatch(thread, route_for_vehicle, order_id, ptype, username)
            assigned_veh_status_update, dispatch_request, route, order_id, ptype, username = get_active_vehicle.assign_inactive_vehicle()

            # Fetched route and returning it for testing purposes
            json_route = json.dumps(route_for_vehicle)
            json_assigned_veh_status_update = json.dumps("Vehicle with " + assigned_veh_status_update)

            # Json to byte
            self.wfile.write(json_route.encode(encoding='utf_8'))
            self.wfile.write(json_assigned_veh_status_update.encode(encoding='utf_8'))

            # Simulate vehicle traversing route
            dispatch_veh = Veh_Supply.Vehicle(dispatch_request, route, order_id, ptype, username)
            update = dispatch_veh.dispatch_assigned_vehicle()

            print(update)

        elif path == "/supply/testRoute":
            # Path is valid. Parsing request.
            content_len = int(self.headers['content-length'])
            post_body = self.rfile.read(content_len)

            print('content length follows: ' + str(content_len))
            print('Postman post body equals: ' + str(post_body) + '\n')

            # Parse testroute post_body
            order_json = VehicleDispatch_Methods.Methods.getOrderJSON(post_body)
            print(order_json)
            ploc = order_json.get("dloc")
            dloc = order_json.get("ploc")

            # Send locations using google maps api, if valid will return status 200
            route_for_vehicle = VehicleDispatch_Methods.Methods.create_route(ploc, dloc)

            # Fetched route and returning it for testing purposes
            json_route = json.dumps(route_for_vehicle)
            # Returning test-route status
            self.wfile.write(json_route.encode(encoding='utf_8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        thread = threading.currentThread().getName()

        print("Path is: " + self.path)
        path = VehicleDispatch_Methods.Methods.parseGetPath(self.path)

        if path == "/dispatchV/testDispatch":

            # Path is valid. Fetching Vehicle Info.
            route = "simulation_DB"
            order_id = 23
            ptype = "clothes"
            username = "AshleyNorris"
            dispatch_info_veh = FleetManager.Dispatch(thread, route, order_id, ptype, username)

            dispatch_thread, vin, location, destination, status = \
                dispatch_info_veh.get_vehicle_info()

            print(dispatch_thread + '\n' "Vin: " + vin + '\n'
                  "Location of Vehicle: " + location + '\n'
                  "Vehicle status: " + status + '\n'
                  "Vehicle destination: " + destination + '\n')

            dispatch_info = {
                'ThreadRequestNum,': dispatch_thread,
                'VIN,': vin,
                'Location,': location,
                'Status': status,
                'Destination': destination

            }

            # Fetched route and assigned vehicle VIN. Responding with dispatch info now.
            dispatch_string = json.dumps(dispatch_info)

            message = threading.currentThread().getName()
            self.wfile.write(b'\n')
            self.wfile.write(message.encode('utf-8'))
            self.wfile.write(b'\n')
            self.wfile.write(dispatch_string.encode(encoding='utf_8'))
            self.wfile.write(b'\n')

        else:
            self.send_response(400)
            self.wfile.write(b'Not a valid GET request path.\n\n')


if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 8080), Handler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

''' 
//--STARTING SERVER--//

#Run the server in the same way as the other examples.
$ python3 http_server_threads.py
$ python3 run.py

Starting server, use <Ctrl-C> to stop

//--OUTPUT--//

#Each time the server receives a request, it starts a new thread or process to handle it:

curl http://127.0.0.1:8080/dispatchV/testDispatch & curl http://127.0.0.1:8080/dispatchV/testDispatch
Thread-1
Thread-2...

curl http://127.0.0.1:8080/supply/requestv?orderID=3&ptype="clothes"&dloc="12709 La Paz Austin, TX"&ploc="9500 S IH 35 Frontage Rd Ste H, Austin"&username="bob2234"

'''
