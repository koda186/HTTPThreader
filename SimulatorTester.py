import time
import json
import requests


class Simulator(object):

    # init method or constructor
    def __init__(self, dispatch_request, route, vin):
        self.dispatch_request = dispatch_request
        self.route = route
        leg_counter = 0
        leg_route_eta = 0
        leg_route_distance = 0
        complete_route_distance = 0
        complete_route_eta = 0
        step_eta_total = 0
        calculated_eta_to_destination = 0
        route_step_eta = " "
        eta_duration = " "
        veh_lat = " "
        veh_lng = " "
        veh_loc = " "
        # simulator route vars
        self.vin = vin
        self.origin = ""
        self.dloc = ""
        self.json_route = route
        # calculated vars
        self.eta_duration = eta_duration
        self.calculated_eta_to_destination = calculated_eta_to_destination
        self.step_eta_total = step_eta_total
        self.route_complete = False
        # complete route vars
        self.complete_route_eta = complete_route_eta
        self.complete_route_distance = complete_route_distance
        # leg vars
        self.leg_counter = leg_counter
        self.leg_route_eta = leg_route_eta
        self.leg_route_distance = leg_route_distance
        # step vars
        self.route_step_eta = route_step_eta
        # veh location vars
        self.veh_lat = veh_lat
        self.veh_lng = veh_lng
        self.vehicle_location = veh_loc

    # -----------------------------------------Vehicle functions----------------------------------------------

    # get route from the dispatch API response for vehicle simulation
    def get_dispatched_vehicle_route_steps(self):
        # Count legs to get item pickup location
        leg_counter = self.leg_counter
        json_response = self.json_route

        # JSON_response comes from the database dispatch api request
        for route in json_response['routes']:
            # ---------------Print Vehicle simulator route updates------------------------
            Simulator.print_simulator_updates(self)
            # Vehicle sends route total distance and total eta to Dispatch if vehicle assigned to route
            '''if self.vin != "NO VEHICLE ASSIGNED":
                Simulator.update_dispatch_total_eta_distance(self)'''

            for leg in route['legs']:
                leg_counter += 1
                self.leg_route_eta = (leg['duration']['text'])
                self.leg_route_distance = (leg['distance']['text'])
                if leg_counter == 1:
                    print('First Leg of trip (Origin to Warehouse(Payload Pickup)) ETA: ' + \
                          str(self.leg_route_eta) + ' and Distance: ' + \
                          Simulator.send_leg_distance(self) + '\n' + 'Vehicle: ' + self.vin + \
                          ' En Route' + '\n\n')
                else:
                    print('Vehicle Receiving Payload -- Vehicle Enroute: Second leg of trip (Warehouse to Destination(Delivery Address)) ETA: ' \
                          + str(self.leg_route_eta)
                          + ' and Distance: ' + str(self.leg_route_distance))
                    # simulate vehicle stopped for item pickup from warehouse
                    time.sleep(1)
                    print('Vehicle: ' + self.vin + ' En Route' + '\n\n')
                for step in leg['steps']:
                    self.eta_duration = str(step['duration']['text'])
                    self.dloc = (step['end_location'])
                    self.origin = (step['start_location'])
                    # update vehicle location
                    self.veh_lat = str(step['end_location']['lat'])
                    self.veh_lng = str(step['end_location']['lng'])
                    time.sleep(2)

                    # Print route to console to simulate vehicle traversing route
                    Simulator.print_dispatched_vehicle_route(self)
                    # send real time updates and confirmation route ended  to dispatch if vehicle assigned to route:
                    '''if self.vin != "NO VEHICLE ASSIGNED":
                        #Simulator.update_dispatch(self)'''


    # get total distance from origin to destination
    def get_V_Complete_Route_Distance(self):
        json_route = self.json_route
        if json_route['status'] == 'NOT_FOUND':
            print("Please enter a valid delivery address!\n")
        else:
            # JSON_response comes from the database dispatch api request
            for route in json_route['routes']:
                for leg in route['legs']:
                    route_distance = (leg['distance']['text'])
                    route_distance = route_distance.replace(',', '')  # remove comma separation
                    distance = float(route_distance.split()[0])
                    self.complete_route_distance += distance
                    self.complete_route_distance = float(format(self.complete_route_distance, '.2f'))
            if self.complete_route_distance == 0:
                raise Exception('Error: Vehicle has not received route!')
            return self.complete_route_distance

    # get vehicle location during route simulation for dispatch
    def get_V_location(self):
        veh_lat = self.veh_lat
        veh_lng = self.veh_lng
        veh_vin = self.vin

        veh_location = {
            'vin': veh_vin,
            'lat': veh_lat,
            'long': veh_lng
        }

        return veh_location

    # get total eta from origin to destination
    def get_V_total_Route_ETA(self):
        json_response = self.json_route
        if json_response['status'] == 'NOT_FOUND':
            print("Please enter a valid delivery address!\n")
        else:
            # JSON_response comes from the database dispatch api request
            for route in json_response['routes']:
                for leg in route['legs']:
                    for step in leg['steps']:
                        self.route_step_eta = (step['duration']['text'])
                        route_step_eta = self.route_step_eta
                        step_eta = int(route_step_eta.split()[0])
                        self.complete_route_eta += step_eta
                        self.complete_route_eta = int(format(self.complete_route_eta))
            if self.complete_route_eta == 0:
                raise Exception('Error: Vehicle has not received route!')
            return self.complete_route_eta

    # Calculate the real time eta for vehicle based on location(step) in route
    def get_V_real_time_eta(self):
        step_eta = int(self.eta_duration.split()[0])
        self.step_eta_total += step_eta
        vehicle_step_eta_total = self.step_eta_total
        self.calculated_eta_to_destination = self.complete_route_eta - vehicle_step_eta_total
        return self.calculated_eta_to_destination

    # Vehicle sends route total distance and total eta to Dispatch
    def update_dispatch_total_eta_distance(self):
        # ---------------Vehicle sends route total distance to Dispatch---------------
        Simulator.send_V_Complete_Route_Distance(self)
        # --------------Vehicle sends total route eta to Dispatch -------------------
        Simulator.send_V_Complete_Route_ETA(self)

    # send real time updates and confirmation route ended  to dispatch
    def update_dispatch(self):
        # --------------Vehicle sends location update to Dispatch---------------
        Vehicle.send_V_location_update(self)
        # --------------Vehicle sends real time eta update to Dispatch---------------
        Vehicle.send_real_time_eta(self)
        # --------------Vehicle sends "is route complete" comfirmation to Dispatch---------------
        Vehicle.send_dispatch_route_ended(self)

    # --------------------------Vehicle - Pycharm Console updates:-----------------------------------------------

    # Printing for Simulator Tester via pycharm console
    def print_simulator_updates(self):
        veh_vin = self.vin
        print('\n\n' + 'You chose Destination Address: ' + str(Simulator.reverse_geocode(self)))
        print('Vehicle Dispatched: VIN of Vehicle IN SERVICE: ' + veh_vin)
        print('Route Calculated: Distance of Trip: ' + str(Simulator.get_V_Complete_Route_Distance(self)) + ' miles')
        print('ETA to destination: ' + str(Simulator.get_V_total_Route_ETA(self)) + ' minutes')

    # Printing for Simulator Tester via pycharm console
    # Simulated vehicle taking route steps: origin, ploc=Payload pickup location, dloc=destination
    def print_dispatched_vehicle_route(self):
        origin = self.origin
        dloc = self.dloc
        veh_vin = self.vin
        # print route steps
        print('Inside Dispatch -- VEHICLE DISPATCH REPORT FOLLOWS: ' + '\n'
              + 'CURRENT vehicle VIN: ' + veh_vin + '\n' + 'Vehicle origin: ' + str(origin)
              + ' TRAVELLING to next step of Vehicle destination: ' + str(dloc)
              + '\n' + 'Updated Vehicle location in Dispatch: ' + str(Simulator.get_V_location(self))
              + '\n' + 'Vehicle Real Time ETA to destination: ' + str(Simulator.get_V_real_time_eta(self)) + ' minutes away'
              + '\n' + 'Vehicle Reports Route Complete: ' + str(Simulator.is_V_route_complete(self))
              + '\n\n')
        if Simulator.is_V_route_complete(self):
            print('Vehicle Arrived at Destination: Dispatch confirmation sent')
        else:
            print('Vehicle: ' + veh_vin + ' En Route')

    # get address from route that google maps api auto-corrected from user input
    def reverse_geocode(self):
        # Count legs to get item pickup location
        leg_counter = 0
        json_response = self.json_route
        # test to see if the request was valid
        if json_response['status'] == 'NOT_FOUND':
            print("Please enter a valid delivery address!\n")
        else:
            for route in json_response['routes']:
                for leg in route['legs']:
                    leg_counter += 1
                    end_address = (leg['end_address'])
                    if leg_counter == 2:
                        return str(end_address)

    # ----------------------------Vehicle - Send Vehicle Updates:----------------------------------------
    # get each leg of route distance
    # legs for "RENT'D AND Farm to Home" are "Origin to Payload pickup" and "Payload pickup to destination"
    def send_leg_distance(self):
        leg_route_distance = self.leg_route_distance
        leg_route_distance = json.dumps(leg_route_distance)
        return leg_route_distance

    # get each leg of route eta
    # legs for "RENT'D AND Farm to Home" are "Origin to Payload pickup" and "Payload pickup to destination"
    def send_leg_eta(self):
        leg_route_eta = self.leg_route_eta
        leg_route_eta = json.dumps(leg_route_eta)
        return leg_route_eta

    # checks is Vehicle route complete;true or false
    def is_V_route_complete(self):
        route_completed = self.route_complete
        real_time_eta = self.calculated_eta_to_destination
        if real_time_eta == 0:
            route_completed = True
        return route_completed

    # send Vin of Vehicle with location updates during route simulation for dispatch
    def send_V_location_update(self):
        vehicle_location = Simulator.get_V_location(self)
        url = "https://localhost:8080/"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(vehicle_location), headers=headers)

    # send (total) complete route eta for dispatch
    def send_V_Complete_Route_ETA(self):
        complete_route_eta = self.complete_route_eta
        veh_vin = self.vin

        total_eta = {
            'vin': veh_vin,
            'compETA': str(complete_route_eta)
        }

        url = "https://localhost:8080/"
        # complete_route_eta = self.complete_route_eta
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(total_eta), headers=headers)

    # send complete route distance for dispatch
    def send_V_Complete_Route_Distance(self):
        complete_route_distance = self.complete_route_distance

        total_distance = {
            'distance': str(complete_route_distance)
        }

        url = "https://localhost:8080/"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(total_distance), headers=headers)

